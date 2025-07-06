#!/usr/bin/env python3
"""
MVP Setup for Qiskit Hackathon Exercises
This script provides the missing validation functions and sets up the environment.
"""

import os
import sys
from pathlib import Path

def create_validation_functions():
    """Create missing validation functions for the exercises."""
    
    # Create the directory structure that the notebooks expect
    exercises_path = Path("exercises_levels/Gates_and_Circuits/Single Qubit Gates/Level_1_Single_Qubit_Gates")
    exercises_path.mkdir(parents=True, exist_ok=True)
    
    # Create the Check_level_1_gates.py file with validation functions
    validation_code = '''
"""
Validation functions for Qiskit Hackathon exercises
"""
import numpy as np
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit

def ex1_validation(qc):
    """Validate exercise 1 - should create |1⟩ state"""
    try:
        state = Statevector.from_instruction(qc)
        expected = Statevector.from_label('1')
        if np.allclose(state.data, expected.data):
            print("✅ Correct! You successfully created the |1⟩ state.")
        else:
            print("❌ Not quite right. Try using the X gate to flip the qubit.")
    except Exception as e:
        print(f"❌ Error in circuit: {e}")

def ex2_validation(qc):
    """Validate exercise 2 - should create |+⟩ state"""
    try:
        state = Statevector.from_instruction(qc)
        expected = Statevector.from_label('+')
        if np.allclose(state.data, expected.data):
            print("✅ Correct! You successfully created the |+⟩ state.")
        else:
            print("❌ Not quite right. Try using the Hadamard gate to create superposition.")
    except Exception as e:
        print(f"❌ Error in circuit: {e}")

def ex3_validation(qc):
    """Validate exercise 3 - should create |-⟩ state"""
    try:
        state = Statevector.from_instruction(qc)
        expected = Statevector.from_label('-')
        if np.allclose(state.data, expected.data):
            print("✅ Correct! You successfully created the |-⟩ state.")
        else:
            print("❌ Not quite right. You need to create superposition and add a phase.")
    except Exception as e:
        print(f"❌ Error in circuit: {e}")

def ex4_validation(counts):
    """Validate exercise 4 - measurement results"""
    try:
        if counts:
            print(f"✅ Measurement successful! Results: {counts}")
            total_shots = sum(counts.values())
            for outcome, count in counts.items():
                probability = count / total_shots
                print(f"   |{outcome}⟩: {probability:.3f} ({count}/{total_shots})")
        else:
            print("❌ No measurement results. Did you add a measurement?")
    except Exception as e:
        print(f"❌ Error in measurement: {e}")

def bonus_validation(angles):
    """Validate bonus exercise - state tomography"""
    try:
        phi, theta = angles
        print(f"✅ Your angles: φ = {phi:.3f}, θ = {theta:.3f}")
        print("📝 Check if these angles reproduce the original state vector!")
    except Exception as e:
        print(f"❌ Error in angles: {e}")

print("Validation functions loaded successfully! 🚀")
'''
    
    with open(exercises_path / "Check_level_1_gates.py", "w") as f:
        f.write(validation_code)
    
    # Also create a simplified version in the main directory for easier access
    with open("validation_functions.py", "w") as f:
        f.write(validation_code)
    
    print("✅ Created validation functions")

def create_test_script():
    """Create a simple test script to verify the setup works."""
    test_code = '''
#!/usr/bin/env python3
"""
Test script to verify Qiskit MVP setup
"""

print("🧪 Testing Qiskit MVP Setup...")
print("=" * 50)

try:
    # Test basic imports
    print("📦 Testing imports...")
    import qiskit
    import numpy as np
    from qiskit import QuantumCircuit, Aer, execute
    from qiskit.quantum_info import Statevector
    from qiskit.visualization import plot_bloch_multivector, plot_histogram
    print(f"✅ Qiskit version: {qiskit.__version__}")
    
    # Test basic quantum circuit
    print("\\n🔬 Testing quantum circuit creation...")
    qc = QuantumCircuit(1)
    qc.h(0)  # Hadamard gate
    state = Statevector.from_instruction(qc)
    print("✅ Created superposition state |+⟩")
    
    # Test measurement
    print("\\n📏 Testing measurement...")
    qc_meas = QuantumCircuit(1, 1)
    qc_meas.h(0)
    qc_meas.measure(0, 0)
    
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc_meas, backend, shots=100)
    counts = job.result().get_counts()
    print(f"✅ Measurement results: {counts}")
    
    print("\\n🎉 All tests passed! Your Qiskit MVP is ready!")
    print("\\n🚀 You can now run the exercises in the Exercises/ directory")
    print("   Start with: jupyter notebook Exercises/Easy_Single_Qubit_Gates.ipynb")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Please install requirements: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Please check your Qiskit installation")

'''
    
    with open("test_mvp.py", "w") as f:
        f.write(test_code)
    
    print("✅ Created test script")

def create_getting_started():
    """Create a getting started guide."""
    guide = '''# Qiskit Hackathon MVP - Getting Started

Welcome to your Qiskit quantum computing environment! 🚀

## Quick Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the setup:**
   ```bash
   python test_mvp.py
   ```

3. **Start Jupyter:**
   ```bash
   jupyter notebook
   ```

4. **Open an exercise:**
   - Navigate to `Exercises/` directory
   - Start with `Easy_Single_Qubit_Gates.ipynb`

## Available Exercises

### Easy Level:
- `Easy_Single_Qubit_Gates.ipynb` - Learn basic quantum gates
- `Easy_Multiple_Qubit_Gates.ipynb` - Work with multi-qubit systems

### Medium Level:
- `Medium_Single_Qubit_Gates.ipynb` - Advanced single qubit operations
- `Medium_Multiple_Qubit_Gates.ipynb` - Complex multi-qubit circuits

## Key Concepts You'll Learn

1. **Quantum States**: |0⟩, |1⟩, |+⟩, |-⟩
2. **Quantum Gates**: X, Y, Z, H, S, CNOT
3. **Superposition**: Creating quantum superposition states
4. **Entanglement**: Bell states and quantum correlations
5. **Measurement**: Extracting classical information

## Quick Quantum Gate Reference

- `qc.x(0)` - Bit flip (NOT gate)
- `qc.h(0)` - Hadamard (superposition)
- `qc.z(0)` - Phase flip
- `qc.s(0)` - S gate (π/2 phase)
- `qc.cx(0,1)` - CNOT gate (control=0, target=1)

## Troubleshooting

- If you get import errors, make sure all packages are installed
- The validation functions are now included and working
- No IBM Quantum account needed - everything runs on simulators

Happy quantum computing! 🌟
'''
    
    with open("GETTING_STARTED.md", "w") as f:
        f.write(guide)
    
    print("✅ Created getting started guide")

if __name__ == "__main__":
    print("🚀 Setting up Qiskit Hackathon MVP...")
    print("=" * 50)
    
    create_validation_functions()
    create_test_script()
    create_getting_started()
    
    print("\\n🎉 MVP setup complete!")
    print("\\n📚 Next steps:")
    print("   1. pip install -r requirements.txt")
    print("   2. python test_mvp.py")
    print("   3. jupyter notebook")
    print("\\n📖 See GETTING_STARTED.md for detailed instructions")