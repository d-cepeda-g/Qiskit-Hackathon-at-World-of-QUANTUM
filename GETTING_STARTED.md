# Qiskit Hackathon MVP - Getting Started

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
