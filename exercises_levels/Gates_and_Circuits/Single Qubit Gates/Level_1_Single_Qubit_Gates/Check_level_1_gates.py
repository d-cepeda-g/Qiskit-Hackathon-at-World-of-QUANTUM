
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
