"""
Quantum Computing Exercises - Part 2: Quantum Algorithms

This script contains exercises for learning quantum algorithms with Qiskit.

Learning Objectives:
- Implement and understand quantum algorithms
- Learn quantum oracle concepts
- Explore quantum speedup
- Practice quantum phase estimation and amplitude amplification

Prerequisites:
- Completion of Part 1: Basics
- Understanding of quantum gates and circuits
- Basic linear algebra and complex numbers
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram, circuit_drawer
from qiskit.quantum_info import Statevector, Operator
from qiskit_aer import AerSimulator
from math import pi, sqrt, asin

# Set up the simulator
simulator = AerSimulator()

def deutsch_jozsa_algorithm():
    """
    Exercise 1: Deutsch-Jozsa Algorithm
    
    The Deutsch-Jozsa algorithm determines if a function is constant or balanced
    with just one quantum query, compared to classical computers that need
    up to 2^(n-1) + 1 queries.
    
    We'll implement both constant and balanced functions.
    """
    print("\n=== Exercise 1: Deutsch-Jozsa Algorithm ===")
    
    def create_constant_oracle(n_qubits, output):
        """Create an oracle for a constant function (always 0 or always 1)"""
        oracle = QuantumCircuit(n_qubits + 1)
        
        if output == 1:
            # If function is constant 1, flip the ancilla qubit
            oracle.x(n_qubits)
        
        oracle.name = f"Constant {output} Oracle"
        return oracle
    
    def create_balanced_oracle(n_qubits):
        """Create an oracle for a balanced function (half 0s, half 1s)"""
        oracle = QuantumCircuit(n_qubits + 1)
        
        # Example balanced function: f(x) = x[0] XOR x[1] for 2-qubit input
        if n_qubits == 2:
            oracle.cx(0, 2)  # CNOT between first input qubit and ancilla
            oracle.cx(1, 2)  # CNOT between second input qubit and ancilla
        elif n_qubits == 1:
            oracle.cx(0, 1)  # Simple copy function for 1 qubit
        
        oracle.name = "Balanced Oracle"
        return oracle
    
    def deutsch_jozsa_circuit(oracle, n_qubits):
        """Create the full Deutsch-Jozsa circuit"""
        qc = QuantumCircuit(n_qubits + 1, n_qubits)
        
        # Initialize ancilla qubit in |1⟩
        qc.x(n_qubits)
        
        # Put all qubits in superposition
        for i in range(n_qubits + 1):
            qc.h(i)
        
        # Apply oracle
        qc.append(oracle, range(n_qubits + 1))
        
        # Apply Hadamard to input qubits
        for i in range(n_qubits):
            qc.h(i)
        
        # Measure input qubits
        qc.measure(range(n_qubits), range(n_qubits))
        
        return qc
    
    # Test with 2-qubit functions
    n_qubits = 2
    
    print(f"Testing Deutsch-Jozsa algorithm with {n_qubits}-qubit functions")
    
    # Test constant function (output = 0)
    oracle_const0 = create_constant_oracle(n_qubits, 0)
    qc_const0 = deutsch_jozsa_circuit(oracle_const0, n_qubits)
    
    print("\nConstant function (always 0):")
    print(qc_const0.draw())
    
    job = simulator.run(qc_const0, shots=1000)
    counts_const0 = job.result().get_counts(qc_const0)
    print(f"Results: {counts_const0}")
    
    # Test constant function (output = 1)
    oracle_const1 = create_constant_oracle(n_qubits, 1)
    qc_const1 = deutsch_jozsa_circuit(oracle_const1, n_qubits)
    
    print("\nConstant function (always 1):")
    job = simulator.run(qc_const1, shots=1000)
    counts_const1 = job.result().get_counts(qc_const1)
    print(f"Results: {counts_const1}")
    
    # Test balanced function
    oracle_balanced = create_balanced_oracle(n_qubits)
    qc_balanced = deutsch_jozsa_circuit(oracle_balanced, n_qubits)
    
    print("\nBalanced function:")
    job = simulator.run(qc_balanced, shots=1000)
    counts_balanced = job.result().get_counts(qc_balanced)
    print(f"Results: {counts_balanced}")
    
    print("\n--- Algorithm Analysis ---")
    print("Deutsch-Jozsa Algorithm Results:")
    print("- Constant functions: All measurements give '00' (all zeros)")
    print("- Balanced functions: At least one measurement gives non-zero")
    print("- Quantum speedup: 1 query vs exponential classical queries!")
    
    return counts_const0, counts_const1, counts_balanced

def grovers_algorithm():
    """
    Exercise 2: Grover's Search Algorithm
    
    Grover's algorithm provides quadratic speedup for searching unsorted databases.
    It finds a marked item in O(√N) iterations instead of classical O(N).
    
    We'll implement a simple 2-qubit version searching for the state |11⟩.
    """
    print("\n=== Exercise 2: Grover's Search Algorithm ===")
    
    def create_oracle_11():
        """Oracle that marks the state |11⟩"""
        oracle = QuantumCircuit(2)
        
        # Oracle flips phase of |11⟩
        oracle.cz(0, 1)  # Controlled-Z gate
        
        oracle.name = "Oracle |11⟩"
        return oracle
    
    def create_diffuser(n_qubits):
        """Amplitude amplification diffuser (inversion about average)"""
        diffuser = QuantumCircuit(n_qubits)
        
        # Apply Hadamard gates
        for i in range(n_qubits):
            diffuser.h(i)
        
        # Apply X gates
        for i in range(n_qubits):
            diffuser.x(i)
        
        # Multi-controlled Z gate (flips |00...0⟩)
        if n_qubits == 2:
            diffuser.cz(0, 1)
        
        # Apply X gates
        for i in range(n_qubits):
            diffuser.x(i)
        
        # Apply Hadamard gates
        for i in range(n_qubits):
            diffuser.h(i)
        
        diffuser.name = "Diffuser"
        return diffuser
    
    def grovers_circuit(n_iterations=1):
        """Create Grover's algorithm circuit"""
        qc = QuantumCircuit(2, 2)
        
        # Initialize in superposition
        qc.h([0, 1])
        
        # Apply Grover iterations
        oracle = create_oracle_11()
        diffuser = create_diffuser(2)
        
        for i in range(n_iterations):
            # Apply oracle
            qc.append(oracle, [0, 1])
            
            # Apply diffuser
            qc.append(diffuser, [0, 1])
        
        # Measure
        qc.measure([0, 1], [0, 1])
        
        return qc
    
    # Test different numbers of iterations
    print("Grover's algorithm searching for |11⟩ state")
    print("Database size: 4 states (2 qubits)")
    print("Optimal iterations: π/4 * √4 ≈ 1.57 ≈ 1-2 iterations")
    
    for iterations in [0, 1, 2, 3]:
        qc = grovers_circuit(iterations)
        
        print(f"\nWith {iterations} Grover iteration(s):")
        if iterations <= 1:
            print(qc.draw())
        
        job = simulator.run(qc, shots=1000)
        counts = job.result().get_counts(qc)
        print(f"Results: {counts}")
        
        # Calculate probability of finding the target
        target_prob = counts.get('11', 0) / 1000
        print(f"Probability of finding |11⟩: {target_prob:.3f}")
    
    print("\n--- Algorithm Analysis ---")
    print("Grover's Algorithm Results:")
    print("- 0 iterations: 25% probability (random search)")
    print("- 1 iteration: ~100% probability (optimal for 4-item database)")
    print("- 2+ iterations: Probability decreases (over-rotation)")
    print("- Classical search: Would need on average 2-3 queries")

def quantum_phase_estimation():
    """
    Exercise 3: Quantum Phase Estimation
    
    Quantum Phase Estimation (QPE) estimates the phase of an eigenvalue
    of a unitary operator. This is a key subroutine in many quantum algorithms.
    
    We'll estimate the phase of the T gate (phase gate with phase π/4).
    """
    print("\n=== Exercise 3: Quantum Phase Estimation ===")
    
    def create_qpe_circuit(n_counting_qubits, unitary_power):
        """Create quantum phase estimation circuit"""
        n_qubits = n_counting_qubits + 1
        qc = QuantumCircuit(n_qubits, n_counting_qubits)
        
        # Initialize eigenstate |1⟩ for T gate
        qc.x(n_counting_qubits)
        
        # Initialize counting qubits in superposition
        for i in range(n_counting_qubits):
            qc.h(i)
        
        # Apply controlled unitary operations
        for i in range(n_counting_qubits):
            # Apply U^(2^i) where U is the T gate
            for _ in range(2**i):
                qc.cp(pi/4, i, n_counting_qubits)  # Controlled phase gate
        
        # Apply inverse QFT to counting qubits
        for i in range(n_counting_qubits):
            qc.h(i)
            for j in range(i):
                qc.cp(-pi/2**(i-j), j, i)
        
        # Reverse the order of qubits (part of inverse QFT)
        for i in range(n_counting_qubits // 2):
            qc.swap(i, n_counting_qubits - 1 - i)
        
        # Measure counting qubits
        qc.measure(range(n_counting_qubits), range(n_counting_qubits))
        
        return qc
    
    # Test with different numbers of counting qubits
    print("Quantum Phase Estimation for T gate")
    print("T gate phase: π/4 radians = 0.25 * 2π = 1/8 in phase units")
    print("Expected binary representation: 0.001 (1/8 = 1/2³)")
    
    for n_counting in [3, 4]:
        qc = create_qpe_circuit(n_counting, 1)
        
        print(f"\nWith {n_counting} counting qubits:")
        if n_counting == 3:
            print(qc.draw())
        
        job = simulator.run(qc, shots=1000)
        counts = job.result().get_counts(qc)
        print(f"Results: {counts}")
        
        # Convert binary results to phase estimates
        print("Phase estimates:")
        for bitstring, count in counts.items():
            phase = int(bitstring, 2) / (2**n_counting)
            print(f"  {bitstring} → phase = {phase:.3f}, count = {count}")
    
    print("\n--- Algorithm Analysis ---")
    print("Quantum Phase Estimation Results:")
    print("- With 3 qubits: Should measure '001' (1/8) most frequently")
    print("- With 4 qubits: Should measure '0010' (2/16 = 1/8) most frequently")
    print("- Higher precision with more counting qubits")
    print("- Essential for Shor's algorithm and quantum simulation")

def quantum_fourier_transform():
    """
    Exercise 4: Quantum Fourier Transform
    
    The QFT is the quantum version of the discrete Fourier transform.
    It's used in many quantum algorithms including Shor's and QPE.
    """
    print("\n=== Exercise 4: Quantum Fourier Transform ===")
    
    def qft_circuit(n_qubits):
        """Create QFT circuit"""
        qc = QuantumCircuit(n_qubits)
        
        for i in range(n_qubits):
            qc.h(i)
            for j in range(i + 1, n_qubits):
                qc.cp(pi / 2**(j - i), j, i)
        
        # Reverse qubit order
        for i in range(n_qubits // 2):
            qc.swap(i, n_qubits - 1 - i)
        
        qc.name = "QFT"
        return qc
    
    def test_qft():
        """Test QFT on different input states"""
        n_qubits = 3
        
        # Test 1: Apply QFT to |000⟩
        qc1 = QuantumCircuit(n_qubits, n_qubits)
        qft = qft_circuit(n_qubits)
        qc1.append(qft, range(n_qubits))
        qc1.measure(range(n_qubits), range(n_qubits))
        
        print("QFT applied to |000⟩:")
        print(qc1.draw())
        
        job = simulator.run(qc1, shots=1000)
        counts1 = job.result().get_counts(qc1)
        print(f"Results: {counts1}")
        
        # Test 2: Apply QFT to |001⟩
        qc2 = QuantumCircuit(n_qubits, n_qubits)
        qc2.x(n_qubits - 1)  # Create |001⟩
        qc2.append(qft, range(n_qubits))
        qc2.measure(range(n_qubits), range(n_qubits))
        
        print("\nQFT applied to |001⟩:")
        
        job = simulator.run(qc2, shots=1000)
        counts2 = job.result().get_counts(qc2)
        print(f"Results: {counts2}")
        
        return counts1, counts2
    
    counts1, counts2 = test_qft()
    
    print("\n--- QFT Analysis ---")
    print("Quantum Fourier Transform Results:")
    print("- QFT of |000⟩: Uniform superposition (equal probabilities)")
    print("- QFT of |001⟩: Oscillating pattern based on frequency 1")
    print("- QFT maps computational basis to frequency basis")
    print("- Fundamental building block for many quantum algorithms")

def bernstein_vazirani_algorithm():
    """
    Exercise 5: Bernstein-Vazirani Algorithm
    
    This algorithm finds a hidden bit string with just one query,
    compared to n queries needed classically.
    """
    print("\n=== Exercise 5: Bernstein-Vazirani Algorithm ===")
    
    def create_bv_oracle(secret_string):
        """Create oracle for hidden bit string"""
        n = len(secret_string)
        oracle = QuantumCircuit(n + 1)
        
        for i, bit in enumerate(secret_string):
            if bit == '1':
                oracle.cx(i, n)
        
        oracle.name = f"BV Oracle ({secret_string})"
        return oracle
    
    def bernstein_vazirani_circuit(secret_string):
        """Create Bernstein-Vazirani circuit"""
        n = len(secret_string)
        qc = QuantumCircuit(n + 1, n)
        
        # Initialize ancilla in |1⟩
        qc.x(n)
        
        # Put all qubits in superposition
        for i in range(n + 1):
            qc.h(i)
        
        # Apply oracle
        oracle = create_bv_oracle(secret_string)
        qc.append(oracle, range(n + 1))
        
        # Apply Hadamard to input qubits
        for i in range(n):
            qc.h(i)
        
        # Measure input qubits
        qc.measure(range(n), range(n))
        
        return qc
    
    # Test with different secret strings
    secret_strings = ['101', '1011', '1101']
    
    for secret in secret_strings:
        print(f"\nTesting with secret string: {secret}")
        
        qc = bernstein_vazirani_circuit(secret)
        
        if len(secret) == 3:
            print(qc.draw())
        
        job = simulator.run(qc, shots=1000)
        counts = job.result().get_counts(qc)
        print(f"Results: {counts}")
        
        # The result should be the secret string
        most_frequent = max(counts, key=counts.get)
        print(f"Discovered secret: {most_frequent}")
        print(f"Correct: {most_frequent == secret}")
    
    print("\n--- Algorithm Analysis ---")
    print("Bernstein-Vazirani Algorithm Results:")
    print("- Finds hidden bit string with 100% success in 1 query")
    print("- Classical algorithms need n queries")
    print("- Demonstrates quantum parallelism")

def main():
    """Run all quantum algorithm exercises"""
    print("QUANTUM COMPUTING EXERCISES - PART 2: ALGORITHMS")
    print("=" * 60)
    
    # Run all exercises
    deutsch_jozsa_algorithm()
    grovers_algorithm()
    quantum_phase_estimation()
    quantum_fourier_transform()
    bernstein_vazirani_algorithm()
    
    print("\n" + "=" * 60)
    print("SUMMARY: QUANTUM ALGORITHMS")
    print("=" * 60)
    
    print("\nAlgorithms covered:")
    print("1. Deutsch-Jozsa: Exponential speedup for function properties")
    print("2. Grover's Search: Quadratic speedup for database search")
    print("3. Quantum Phase Estimation: Essential subroutine for many algorithms")
    print("4. Quantum Fourier Transform: Maps between computational and frequency bases")
    print("5. Bernstein-Vazirani: Linear speedup for hidden bit string problem")
    
    print("\nKey concepts:")
    print("- Quantum parallelism and interference")
    print("- Oracle-based algorithms")
    print("- Amplitude amplification")
    print("- Phase kickback")
    print("- Quantum speedup vs classical algorithms")
    
    print("\nNext steps:")
    print("- Implement Shor's factoring algorithm")
    print("- Study variational quantum eigensolvers (VQE)")
    print("- Explore quantum error correction")
    print("- Learn about quantum machine learning algorithms")

if __name__ == "__main__":
    main()