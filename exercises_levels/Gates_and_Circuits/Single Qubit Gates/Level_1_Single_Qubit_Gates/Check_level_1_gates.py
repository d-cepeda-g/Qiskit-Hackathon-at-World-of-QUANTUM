"""
Validation functions for Level 1 Single Qubit Gates exercises.
This module contains functions to check exercise solutions.
"""

import numpy as np
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit

def ex1_validation(qc):
    """Validate exercise 1 - bit flip to |1⟩ state."""
    try:
        state = Statevector.from_instruction(qc)
        expected = Statevector.from_label('1')
        
        if state.equiv(expected):
            print("✅ Excellent! You successfully created the |1⟩ state!")
        else:
            print("❌ Not quite right. Try using the X gate to flip from |0⟩ to |1⟩.")
            print(f"Your state: {state}")
            print(f"Expected: {expected}")
    except Exception as e:
        print(f"❌ Error validating circuit: {e}")

def ex2_validation(qc):
    """Validate exercise 2 - superposition |+⟩ state."""
    try:
        state = Statevector.from_instruction(qc)
        expected = Statevector.from_label('+')
        
        if state.equiv(expected):
            print("✅ Perfect! You created the |+⟩ superposition state!")
        else:
            print("❌ Not quite right. Try using the Hadamard gate to create superposition.")
            print(f"Your state: {state}")
            print(f"Expected: {expected}")
    except Exception as e:
        print(f"❌ Error validating circuit: {e}")

def ex3_validation(qc):
    """Validate exercise 3 - |−⟩ state."""
    try:
        state = Statevector.from_instruction(qc)
        expected = Statevector.from_label('-')
        
        if state.equiv(expected):
            print("✅ Great work! You created the |−⟩ state!")
        else:
            print("❌ Not quite right. Think about combining gates to get the |−⟩ state.")
            print("Hint: You might need more than one gate!")
            print(f"Your state: {state}")
            print(f"Expected: {expected}")
    except Exception as e:
        print(f"❌ Error validating circuit: {e}")

def ex4_validation(counts):
    """Validate exercise 4 - measurement results."""
    try:
        total_shots = sum(counts.values())
        
        if '0' in counts and '1' in counts:
            prob_0 = counts.get('0', 0) / total_shots
            prob_1 = counts.get('1', 0) / total_shots
            print("✅ Good! You successfully measured the quantum state!")
            print(f"Probability of measuring |0⟩: {prob_0:.3f}")
            print(f"Probability of measuring |1⟩: {prob_1:.3f}")
        else:
            print("✅ Measurement completed!")
            print("Results:", counts)
    except Exception as e:
        print(f"❌ Error validating measurement: {e}")

def bonus_validation(angles):
    """Validate bonus exercise - state tomography."""
    try:
        phi, theta = angles
        print(f"✅ Your answer: φ = {phi:.3f}, θ = {theta:.3f}")
        print("State tomography is a complex topic - great job attempting it!")
        print("In a real scenario, you would compare this with the actual random state parameters.")
    except Exception as e:
        print(f"❌ Error validating angles: {e}")

# Additional helper functions
def compare_states(state1, state2, tolerance=1e-10):
    """Compare two quantum states with a given tolerance."""
    return np.allclose(state1.data, state2.data, atol=tolerance)

def print_state_info(state):
    """Print useful information about a quantum state."""
    print(f"State vector: {state}")
    print(f"Probabilities: {state.probabilities()}")
    if state.num_qubits == 1:
        bloch_coords = state.to_dict()
        print(f"Bloch coordinates available for visualization")