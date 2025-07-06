"""
Quantum Computing Exercises - Part 1: Basics

This script contains foundational exercises for learning quantum computing with Qiskit.

Learning Objectives:
- Understand quantum circuits and qubits
- Learn basic quantum gates
- Practice creating and visualizing quantum circuits
- Understand quantum measurements

Prerequisites:
- Basic understanding of linear algebra
- Python programming basics
- Qiskit installation
"""

# Import required libraries
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import transpile
from qiskit.visualization import plot_histogram, circuit_drawer
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

# Set up the simulator
simulator = AerSimulator()

def setup_environment():
    """Setup and verify Qiskit installation"""
    print("Qiskit setup complete!")
    print("Available backend:", simulator)
    return simulator

def exercise_1():
    """
    Exercise 1: Your First Quantum Circuit
    
    Task: Create a simple quantum circuit with one qubit and measure it.
    
    Instructions:
    1. Create a quantum circuit with 1 qubit and 1 classical bit
    2. Add a measurement operation
    3. Visualize the circuit
    4. Run the circuit 1000 times and plot the results
    """
    print("\n=== Exercise 1: Your First Quantum Circuit ===")
    
    # Create quantum circuit
    qc = QuantumCircuit(1, 1)
    
    # Add measurement
    qc.measure(0, 0)
    
    # Visualize the circuit
    print("Circuit diagram:")
    print(qc.draw())
    
    # Run the circuit
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    
    # Plot results
    print(f"Results: {counts}")
    
    # Discussion
    print("\n--- Discussion ---")
    print("What do you observe?")
    print("- The qubit starts in |0⟩ state by default")
    print("- We should get 100% |0⟩ measurements")
    print(f"- Actual results: {counts}")
    
    return qc, counts

def exercise_2():
    """
    Exercise 2: The X Gate (Quantum NOT)
    
    Task: Apply an X gate to flip a qubit from |0⟩ to |1⟩.
    
    Instructions:
    1. Create a quantum circuit with 1 qubit and 1 classical bit
    2. Apply an X gate to the qubit
    3. Measure the qubit
    4. Run the circuit and observe the results
    """
    print("\n=== Exercise 2: The X Gate (Quantum NOT) ===")
    
    # Create quantum circuit
    qc = QuantumCircuit(1, 1)
    
    # Apply X gate
    qc.x(0)
    
    # Add measurement
    qc.measure(0, 0)
    
    # Visualize and run
    print("Circuit with X gate:")
    print(qc.draw())
    
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    
    print(f"Results: {counts}")
    print("Expected: 100% |1⟩ (state '1')")
    
    return qc, counts

def exercise_3():
    """
    Exercise 3: Creating Superposition with Hadamard Gate
    
    Task: Use the Hadamard gate to create a superposition state.
    
    Instructions:
    1. Create a quantum circuit with 1 qubit and 1 classical bit
    2. Apply a Hadamard (H) gate to create superposition
    3. Measure the qubit
    4. Run the circuit multiple times and observe the probabilistic results
    """
    print("\n=== Exercise 3: Creating Superposition with Hadamard Gate ===")
    
    qc = QuantumCircuit(1, 1)
    
    # Apply Hadamard gate
    qc.h(0)
    
    # Measure
    qc.measure(0, 0)
    
    print("Circuit with Hadamard gate:")
    print(qc.draw())
    
    # Run the circuit
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    
    print(f"Results: {counts}")
    
    print("\n--- Understanding Superposition ---")
    print("The Hadamard gate creates the state: |+⟩ = (|0⟩ + |1⟩)/√2")
    print("This means 50% probability of measuring |0⟩ and 50% probability of measuring |1⟩")
    
    return qc, counts

def exercise_4():
    """
    Exercise 4: Two-Qubit Circuits and CNOT Gate
    
    Task: Create a two-qubit circuit and explore the CNOT gate.
    
    Instructions:
    1. Create a circuit with 2 qubits and 2 classical bits
    2. Apply different combinations of gates
    3. Use the CNOT gate to create entanglement
    4. Compare results for different initial states
    """
    print("\n=== Exercise 4: Two-Qubit Circuits and CNOT Gate ===")
    
    def cnot_basic():
        """CNOT with control qubit in |0⟩"""
        qc = QuantumCircuit(2, 2)
        
        # Apply CNOT (control=0, target=1)
        qc.cx(0, 1)
        
        # Measure both qubits
        qc.measure([0, 1], [0, 1])
        
        print("CNOT with control in |0⟩:")
        print(qc.draw())
        
        job = simulator.run(qc, shots=1000)
        counts = job.result().get_counts(qc)
        print(f"Results: {counts}")
        
        return counts
    
    def cnot_with_x():
        """CNOT with control qubit in |1⟩"""
        qc = QuantumCircuit(2, 2)
        
        # Put control qubit in |1⟩
        qc.x(0)
        
        # Apply CNOT
        qc.cx(0, 1)
        
        # Measure
        qc.measure([0, 1], [0, 1])
        
        print("\nCNOT with control in |1⟩:")
        print(qc.draw())
        
        job = simulator.run(qc, shots=1000)
        counts = job.result().get_counts(qc)
        print(f"Results: {counts}")
        
        return counts
    
    # Run both versions
    counts_a = cnot_basic()
    counts_b = cnot_with_x()
    
    print("\n--- CNOT Gate Analysis ---")
    print("CNOT gate: flips target qubit if control qubit is |1⟩")
    print(f"Control |0⟩: {counts_a}")
    print(f"Control |1⟩: {counts_b}")
    
    return counts_a, counts_b

def exercise_5():
    """
    Exercise 5: Creating a Bell State (Entanglement)
    
    Task: Create a Bell state - one of the most important quantum states showing entanglement.
    
    Instructions:
    1. Start with two qubits in |00⟩
    2. Apply Hadamard to the first qubit
    3. Apply CNOT with first qubit as control
    4. Measure and analyze the results
    """
    print("\n=== Exercise 5: Creating a Bell State (Entanglement) ===")
    
    qc = QuantumCircuit(2, 2)
    
    # Step 1: Apply Hadamard to first qubit
    qc.h(0)
    
    # Step 2: Apply CNOT
    qc.cx(0, 1)
    
    # Add barrier for visualization
    qc.barrier()
    
    # Measure
    qc.measure([0, 1], [0, 1])
    
    print("Bell State Circuit:")
    print(qc.draw())
    
    # Run the circuit
    job = simulator.run(qc, shots=1000)
    counts = job.result().get_counts(qc)
    
    print(f"Results: {counts}")
    
    print("\n--- Understanding Bell States ---")
    print("The Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2 shows perfect correlation:")
    print("- When you measure the first qubit as |0⟩, the second is always |0⟩")
    print("- When you measure the first qubit as |1⟩, the second is always |1⟩")
    print("- This is quantum entanglement!")
    print("- Notice: You only get '00' and '11' outcomes, never '01' or '10'")
    
    return qc, counts

def exercise_6():
    """
    Exercise 6: Quantum State Visualization
    
    Task: Visualize quantum states without measurement using the statevector simulator.
    
    Instructions:
    1. Create circuits without measurement
    2. Use Statevector to see the quantum state
    3. Visualize states using different representations
    """
    print("\n=== Exercise 6: Quantum State Visualization ===")
    
    # Create different quantum states
    states = []
    labels = []
    
    # State 1: |0⟩
    qc1 = QuantumCircuit(1)
    state1 = Statevector.from_instruction(qc1)
    states.append(state1)
    labels.append("|0⟩")
    
    # State 2: |1⟩
    qc2 = QuantumCircuit(1)
    qc2.x(0)
    state2 = Statevector.from_instruction(qc2)
    states.append(state2)
    labels.append("|1⟩")
    
    # State 3: |+⟩ = (|0⟩ + |1⟩)/√2
    qc3 = QuantumCircuit(1)
    qc3.h(0)
    state3 = Statevector.from_instruction(qc3)
    states.append(state3)
    labels.append("|+⟩")
    
    # State 4: |-⟩ = (|0⟩ - |1⟩)/√2
    qc4 = QuantumCircuit(1)
    qc4.x(0)
    qc4.h(0)
    state4 = Statevector.from_instruction(qc4)
    states.append(state4)
    labels.append("|-⟩")
    
    # Print state vectors
    for i, (state, label) in enumerate(zip(states, labels)):
        print(f"\nState {label}:")
        print(f"Statevector: {state.data}")
        print(f"Probabilities: {state.probabilities()}")
    
    # Visualize Bell state
    print("\n--- Bell State Visualization ---")
    bell_qc = QuantumCircuit(2)
    bell_qc.h(0)
    bell_qc.cx(0, 1)
    
    bell_state = Statevector.from_instruction(bell_qc)
    print(f"Bell state vector: {bell_state.data}")
    print(f"Bell state probabilities: {bell_state.probabilities()}")
    print("Notice: Equal probability for |00⟩ and |11⟩, zero for |01⟩ and |10⟩")
    
    return states, bell_state

def practice_problems():
    """
    Practice Problems
    
    Challenge yourself with these problems:
    """
    print("\n=== Practice Problems ===")
    
    # Problem 1: Custom probability distribution
    print("\nProblem 1: Create a circuit that produces exactly 25% |0⟩ and 75% |1⟩")
    print("Hint: Use rotation gates (ry gate)")
    
    qc = QuantumCircuit(1, 1)
    
    # For 75% |1⟩, we need |ψ⟩ = √0.25|0⟩ + √0.75|1⟩ = 0.5|0⟩ + √0.75|1⟩
    # This corresponds to θ where cos(θ/2) = 0.5, so θ/2 = π/3, θ = 2π/3
    theta = 2 * np.arccos(0.5)  # This gives approximately 2.094 radians
    qc.ry(theta, 0)
    qc.measure(0, 0)
    
    print("Solution circuit:")
    print(qc.draw())
    print(f"Rotation angle: {theta:.3f} radians = {np.degrees(theta):.1f} degrees")
    
    job = simulator.run(qc, shots=1000)
    counts = job.result().get_counts(qc)
    print(f"Results: {counts}")
    
    # Problem 2: Bell states overview
    print("\nProblem 2: The four Bell states")
    bell_states = [
        "Φ+ = (|00⟩ + |11⟩)/√2",
        "Φ- = (|00⟩ - |11⟩)/√2", 
        "Ψ+ = (|01⟩ + |10⟩)/√2",
        "Ψ- = (|01⟩ - |10⟩)/√2"
    ]
    
    print("Challenge: Try to create all four Bell states!")
    print("Hint: Use combinations of X, Z, H, and CNOT gates")
    for state in bell_states:
        print(f"  - {state}")

def main():
    """Run all exercises"""
    print("QUANTUM COMPUTING EXERCISES - PART 1: BASICS")
    print("=" * 50)
    
    # Setup
    setup_environment()
    
    # Run all exercises
    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
    exercise_5()
    exercise_6()
    practice_problems()
    
    print("\n" + "=" * 50)
    print("SUMMARY AND NEXT STEPS")
    print("=" * 50)
    
    print("\nWhat you've learned:")
    print("1. Basic quantum circuits - Creating and measuring qubits")
    print("2. Quantum gates - X, H, CNOT gates and their effects")
    print("3. Superposition - Creating probabilistic quantum states")
    print("4. Entanglement - Bell states and quantum correlations")
    print("5. State visualization - Understanding quantum states mathematically")
    
    print("\nKey concepts:")
    print("- Qubits can be in superposition of |0⟩ and |1⟩")
    print("- Measurement collapses the quantum state")
    print("- Entangled qubits show correlated behavior")
    print("- Quantum gates are unitary operations")
    
    print("\nNext topics to explore:")
    print("- Quantum algorithms (Grover's search, Shor's factoring)")
    print("- Quantum error correction")
    print("- Variational quantum algorithms")
    print("- Quantum machine learning")

if __name__ == "__main__":
    main()