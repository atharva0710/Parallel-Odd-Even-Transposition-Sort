import subprocess
import os
import sys

# --- CONFIGURATION ---
# Because O(N^2) is slow, we use smaller N than the bitonic example
SMALL_N = 10000   
LARGE_N = 40000   
THREADS = [1, 2, 4, 8, 16] # Adjust based on your computer's actual cores
CPP_FILE = "odd_even_sort.cpp"
EXE_FILE = "odd_even_sort"

def compile_code():
    print("--- Compiling C++ Code ---")
    
    # Check if we are on macOS
    if sys.platform == 'darwin':
        print("Detected macOS. Checking for OpenMP (libomp)...")
        
        # 1. Attempt to find the specific installation path of libomp via Homebrew
        # This fixes issues where libomp is installed in a custom location
        omp_include = "-I/opt/homebrew/include" # Default fallback (Apple Silicon)
        omp_lib = "-L/opt/homebrew/lib"         # Default fallback (Apple Silicon)
        
        try:
            # Run 'brew --prefix libomp' to get the exact location
            brew_prefix = subprocess.check_output(["brew", "--prefix", "libomp"], text=True).strip()
            print(f"Found libomp installation at: {brew_prefix}")
            omp_include = f"-I{brew_prefix}/include"
            omp_lib = f"-L{brew_prefix}/lib"
        except Exception:
            print("Warning: Could not auto-detect libomp path via 'brew'. Using defaults.")
            print("If compilation fails, run: 'brew install libomp'")

        # macOS (Apple Clang) needs specific flags to find libomp
        cmd = [
            "g++", "-Xpreprocessor", "-fopenmp", "-O3",
            omp_include, "-I/usr/local/include", 
            omp_lib, "-L/usr/local/lib",
            CPP_FILE, "-o", EXE_FILE, "-lomp"
        ]
    else:
        # Standard Linux/Windows behavior
        print("Detected standard environment (Linux/Windows).")
        cmd = ["g++", "-fopenmp", "-O3", CPP_FILE, "-o", EXE_FILE]

    # Run the compilation command
    try:
        result = subprocess.run(cmd)
        if result.returncode != 0:
            raise Exception("Compilation returned error code")
    except Exception:
        print("\n❌ Error: Compilation failed!")
        if sys.platform == 'darwin':
            print("-" * 50)
            print("MAC OS TROUBLESHOOTING:")
            print("1. Open a NEW terminal window.")
            print("2. Run this command: brew install libomp")
            print("3. Try running this script again.")
            print("-" * 50)
        exit(1)
        
    print("✅ Compilation successful.\n")

def run_experiment(n, p):
    # Runs the C++ executable with arguments N and P
    # Returns the elapsed time as a float
    try:
        if os.name == 'nt': # Windows
            cmd = [f"{EXE_FILE}.exe", str(n), str(p)]
        else: # Linux/Mac
            cmd = [f"./{EXE_FILE}", str(n), str(p)]
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error running N={n} P={p}: {e}")
        return 0.0

def run_strong_scaling():
    print("-" * 60)
    print(f"STRONG SCALING EXPERIMENT (Fixed N, Varying P)")
    print("-" * 60)
    print(f"{'N':<10} {'Threads':<10} {'Time(s)':<10} {'Speedup':<10}")
    
    # We test two input sizes: Small and Large
    for n_size in [SMALL_N, LARGE_N]:
        base_time = 0.0
        print(f"--- Input Size: {n_size} ---")
        for p in THREADS:
            time = run_experiment(n_size, p)
            
            # Calculate speedup (Base Time / Current Time)
            if p == THREADS[0]: # First thread count is baseline
                base_time = time
                speedup = 1.0
            else:
                speedup = base_time / time if time > 0 else 0
            
            print(f"{n_size:<10} {p:<10} {time:<10.4f} {speedup:<10.2f}x")
    print("\n")

def run_weak_scaling():
    print("-" * 60)
    print(f"WEAK SCALING EXPERIMENT (Scale N as P increases)")
    print("-" * 60)
    # For O(N^2) algorithm, to keep WORK constant per processor:
    # If P doubles, N should increase by sqrt(2) approx 1.41
    # However, for simplicity (like the example report), we will just 
    # increase N linearly and observe the behavior.
    
    print(f"{'N':<10} {'Threads':<10} {'Time(s)':<10}")
    
    current_n = SMALL_N
    for p in THREADS:
        time = run_experiment(int(current_n), p)
        print(f"{int(current_n):<10} {p:<10} {time:<10.4f}")
        
        # Increase N for the next iteration
        # We multiply by 1.41 (sqrt(2)) to try and keep work-per-thread roughly similar
        current_n = current_n * 1.414 

def main():
    compile_code()
    run_strong_scaling()
    run_weak_scaling()

if __name__ == "__main__":
    main()