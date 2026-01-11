# Parallel Odd-Even Transposition Sort

This project implements the **Odd-Even Transposition Sort** algorithm using C++ and OpenMP. It provides a comprehensive framework for automated benchmarking, performance analysis, and report generation.

---

## Project Structure

- **`odd_even_sort.cpp`**: Core C++ source file implementing the sorting algorithm with OpenMP parallelization and timing logic.
- **`Makefile`**: Build script configured to compile the source code with optimizations.
- **`run_project.py`**: Python automation script for executing benchmark suites (Strong and Weak scaling) and formatting results.
- **`report.tex`**: LaTeX template for generating the final performance analysis report.
- **`create_makefile.py`**: Configuration utility to generate system-specific Makefiles (particularly for macOS environments).

---

## Prerequisites

### 1. C++ Compiler & Build Tools

Ensure a C++17 compliant compiler and `make` are installed.

- **macOS**: Install via Xcode Command Line Tools: `xcode-select --install`.
- **Linux**: Install build-essential: `sudo apt install build-essential`.

### 2. OpenMP Library

OpenMP is required for parallel execution. Note that the default Apple Clang on macOS lacks OpenMP support.

- **macOS (Homebrew)**:
  ```bash
  brew install libomp
  ```

---

## Compilation

### Option A: Using Makefile (Recommended)

The provided Makefile uses C++17 and `-O3` optimizations.

```bash
make
```

If the build fails with "omp.h not found", regenerate the Makefile:

```bash
python3 create_makefile.py
make
```

### Option B: Manual Compilation (macOS)

```bash
g++ -std=c++17 -Xpreprocessor -fopenmp -O3 -Wall -I/opt/homebrew/include -L/opt/homebrew/lib -lomp -o odd_even_sort odd_even_sort.cpp
```

---

## Running Experiments

### Manual Verification

Run the executable with `<N>` (array size) and `<Threads>`:

```bash
./odd_even_sort 20000 4
```

**Expected Output:** `N=20000, P=4, Time=0.1234s [Check: Sorted OK]`

### Automated Benchmarking

Generate complete experimental data for the report:

```bash
python3 run_project.py
```

This produces results for:

1. **Strong Scaling**: Fixed $N$, varying thread count $P$.
2. **Weak Scaling**: $N$ scaled proportionally with $P$.

---

## Report Generation

1. Open **`report.tex`**.
2. Populate the tables in the **Experiments** section with data from `run_project.py`.
3. Compile to PDF:
   - **Overleaf**: Upload `report.tex`.
   - **Local**: Run `pdflatex report.tex`.

---

## Submission Checklist

- [ ] Run `make clean` to remove binaries.
- [ ] Verify `odd_even_sort.cpp`, `Makefile`, and `report.pdf` are present.
- [ ] Archive into `Project_YourName.zip`.

---

## Troubleshooting

- **`fatal error: 'omp.h' not found`**: Run `python3 create_makefile.py` to fix paths.
- **Speedup < 1.0**: Small input size ($N$) relative to thread count $P$ causes synchronization overhead.
- **`Array NOT sorted!`**: Indicates a race condition. Ensure `#pragma omp parallel for` is used with the default barriers.
