# Compiler
CXX = g++

# --- CONFIGURATION FLAGS ---

# OPTION 1: Standard Linux (Commented out for Mac)
# CXXFLAGS = -std=c++17 -fopenmp -O3 -Wall

# OPTION 2: macOS (Enabled)
# Uses -Xpreprocessor and points to the detected Homebrew path: /opt/homebrew/opt/libomp
CXXFLAGS = -std=c++17 -Xpreprocessor -fopenmp -O3 -Wall -I/opt/homebrew/opt/libomp/include -L/opt/homebrew/opt/libomp/lib -lomp

# ---------------------------

# Target executable name
TARGET = odd_even_sort

# Source file
SRC = odd_even_sort.cpp

# Default rule: "make" runs this
all: $(TARGET)

# Rule to link the program (Indented with TAB)
$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

# Rule to clean up files (Indented with TAB)
clean:
	rm -f $(TARGET)
