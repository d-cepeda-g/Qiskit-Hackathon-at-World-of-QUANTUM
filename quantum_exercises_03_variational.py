"""
Quantum Computing Exercises - Part 3: Variational Quantum Algorithms

This script contains exercises for learning variational quantum algorithms and 
quantum machine learning with Qiskit.

Learning Objectives:
- Understand variational quantum algorithms
- Implement VQE (Variational Quantum Eigensolver)
- Learn QAOA (Quantum Approximate Optimization Algorithm)
- Explore quantum machine learning concepts
- Practice quantum feature maps and variational circuits

Prerequisites:
- Completion of Parts 1 and 2
- Understanding of optimization concepts
- Basic machine learning knowledge
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram, circuit_drawer
from qiskit.quantum_info import Statevector, Operator, SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit.primitives import Estimator, Sampler
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# Set up the simulator
simulator = AerSimulator()
estimator = Estimator()
sampler = Sampler()

def variational_quantum_eigensolver():
    """
    Exercise 1: Variational Quantum Eigensolver (VQE)
    
    VQE finds the ground state energy of a Hamiltonian using a variational
    quantum circuit. This is one of the most important near-term quantum algorithms.
    
    We'll find the ground state of H = Z⊗Z (two-qubit Ising model).
    """
    print("\n=== Exercise 1: Variational Quantum Eigensolver (VQE) ===")
    
    def create_ansatz(theta):
        """Create a simple ansatz circuit"""
        qc = QuantumCircuit(2)
        
        # Initial layer
        qc.ry(theta[0], 0)
        qc.ry(theta[1], 1)
        
        # Entangling layer
        qc.cx(0, 1)
        
        # Second variational layer
        qc.ry(theta[2], 0)
        qc.ry(theta[3], 1)
        
        return qc
    
    def cost_function(theta, hamiltonian):
        """Cost function for VQE"""
        ansatz = create_ansatz(theta)
        
        # Estimate expectation value
        job = estimator.run(ansatz, hamiltonian)
        result = job.result()
        energy = result.values[0]
        
        return energy
    
    # Define Hamiltonian: H = Z⊗Z
    hamiltonian = SparsePauliOp.from_list([("ZZ", 1.0)])
    
    print("Hamiltonian: H = Z⊗Z")
    print("Theoretical ground state: |00⟩ or |11⟩ with energy = 1")
    print("Theoretical excited state: |01⟩ or |10⟩ with energy = -1")
    
    # Random initial parameters
    np.random.seed(42)
    initial_theta = np.random.random(4) * 2 * np.pi
    
    print(f"\nInitial parameters: {initial_theta}")
    
    # Run VQE optimization
    print("\nRunning VQE optimization...")
    result = minimize(cost_function, initial_theta, args=(hamiltonian,), 
                     method='COBYLA', options={'maxiter': 100})
    
    print(f"Optimization converged: {result.success}")
    print(f"Final energy: {result.fun:.6f}")
    print(f"Optimal parameters: {result.x}")
    
    # Create and analyze the optimal circuit
    optimal_circuit = create_ansatz(result.x)
    print("\nOptimal ansatz circuit:")
    print(optimal_circuit.draw())
    
    # Get the final state
    final_state = Statevector.from_instruction(optimal_circuit)
    print(f"\nFinal state probabilities: {final_state.probabilities()}")
    
    return result, optimal_circuit

def quantum_approximate_optimization():
    """
    Exercise 2: Quantum Approximate Optimization Algorithm (QAOA)
    
    QAOA solves combinatorial optimization problems by alternating between
    problem and mixer Hamiltonians. We'll solve a simple Max-Cut problem.
    """
    print("\n=== Exercise 2: Quantum Approximate Optimization Algorithm (QAOA) ===")
    
    def create_qaoa_circuit(gamma, beta, p_layers=1):
        """Create QAOA circuit for Max-Cut on triangle graph"""
        qc = QuantumCircuit(3)
        
        # Initial superposition
        qc.h([0, 1, 2])
        
        for p in range(p_layers):
            # Problem Hamiltonian: maximize cuts
            # Apply exp(-i*gamma*H_C) where H_C = 0.5*(1-Z_i*Z_j) for each edge
            
            # Edge (0,1)
            qc.rzz(2*gamma[p], 0, 1)
            
            # Edge (1,2)
            qc.rzz(2*gamma[p], 1, 2)
            
            # Edge (0,2)
            qc.rzz(2*gamma[p], 0, 2)
            
            # Mixer Hamiltonian: apply exp(-i*beta*H_M) where H_M = X_0 + X_1 + X_2
            qc.rx(2*beta[p], 0)
            qc.rx(2*beta[p], 1)
            qc.rx(2*beta[p], 2)
        
        return qc
    
    def evaluate_maxcut(bitstring):
        """Evaluate Max-Cut objective for triangle graph"""
        # Count cuts: edges are (0,1), (1,2), (0,2)
        cuts = 0
        cuts += int(bitstring[0]) ^ int(bitstring[1])  # Edge (0,1)
        cuts += int(bitstring[1]) ^ int(bitstring[2])  # Edge (1,2)
        cuts += int(bitstring[0]) ^ int(bitstring[2])  # Edge (0,2)
        return cuts
    
    def qaoa_cost_function(params, p_layers=1):
        """QAOA cost function"""
        mid = len(params) // 2
        gamma = params[:mid]
        beta = params[mid:]
        
        qc = create_qaoa_circuit(gamma, beta, p_layers)
        qc.measure_all()
        
        # Run circuit
        job = sampler.run(qc, shots=1000)
        result = job.result()
        counts = result.quasi_dists[0]
        
        # Calculate expectation value of cuts
        total_cuts = 0
        total_shots = 0
        
        for bitstring, prob in counts.items():
            # Convert integer to binary string
            binary = format(bitstring, '03b')
            cuts = evaluate_maxcut(binary)
            total_cuts += cuts * prob * 1000
            total_shots += prob * 1000
        
        avg_cuts = total_cuts / total_shots if total_shots > 0 else 0
        
        # We want to maximize cuts, so minimize negative cuts
        return -avg_cuts
    
    print("Max-Cut problem on triangle graph")
    print("Graph edges: (0,1), (1,2), (0,2)")
    print("Goal: Find partition that maximizes cuts")
    print("Optimal solution: 2 cuts (e.g., partition {0} vs {1,2})")
    
    # Test different QAOA depths
    for p_layers in [1, 2]:
        print(f"\n--- QAOA with p = {p_layers} layers ---")
        
        # Random initial parameters
        np.random.seed(42)
        initial_params = np.random.random(2 * p_layers) * np.pi
        
        print(f"Initial parameters: {initial_params}")
        
        # Optimize
        result = minimize(qaoa_cost_function, initial_params, args=(p_layers,),
                         method='COBYLA', options={'maxiter': 50})
        
        print(f"Optimization converged: {result.success}")
        print(f"Best objective (negative cuts): {result.fun:.4f}")
        print(f"Expected cuts: {-result.fun:.4f}")
        print(f"Optimal parameters: {result.x}")
        
        # Analyze final solution
        mid = len(result.x) // 2
        gamma_opt = result.x[:mid]
        beta_opt = result.x[mid:]
        
        final_circuit = create_qaoa_circuit(gamma_opt, beta_opt, p_layers)
        if p_layers == 1:
            print("\nOptimal QAOA circuit:")
            print(final_circuit.draw())

def quantum_feature_map():
    """
    Exercise 3: Quantum Feature Maps
    
    Feature maps encode classical data into quantum states for quantum
    machine learning. We'll explore different encoding strategies.
    """
    print("\n=== Exercise 3: Quantum Feature Maps ===")
    
    def angle_encoding(data):
        """Encode data as rotation angles"""
        n_qubits = len(data)
        qc = QuantumCircuit(n_qubits)
        
        for i, x in enumerate(data):
            qc.ry(x, i)
        
        qc.name = "Angle Encoding"
        return qc
    
    def amplitude_encoding(data):
        """Encode data as amplitudes (simplified version)"""
        # Normalize data
        norm = np.linalg.norm(data)
        if norm > 0:
            data = data / norm
        
        n_qubits = int(np.ceil(np.log2(len(data))))
        qc = QuantumCircuit(n_qubits)
        
        # Simple amplitude encoding using initialize
        # (In practice, this would be decomposed into gates)
        qc.initialize(data, range(n_qubits))
        
        qc.name = "Amplitude Encoding"
        return qc
    
    def pauli_feature_map(data, repetitions=2):
        """Create Pauli feature map with entanglement"""
        n_qubits = len(data)
        qc = QuantumCircuit(n_qubits)
        
        for rep in range(repetitions):
            # Apply Hadamard gates
            qc.h(range(n_qubits))
            
            # Single-qubit rotations
            for i, x in enumerate(data):
                qc.rz(2 * x, i)
            
            # Entangling gates
            for i in range(n_qubits - 1):
                qc.cx(i, i + 1)
                qc.rz(2 * data[i] * data[i + 1], i + 1)
                qc.cx(i, i + 1)
        
        qc.name = f"Pauli Feature Map (r={repetitions})"
        return qc
    
    # Test different feature maps with sample data
    sample_data = np.array([0.5, 1.2, -0.8])
    
    print("Sample data:", sample_data)
    
    # Angle encoding
    angle_map = angle_encoding(sample_data)
    print(f"\nAngle encoding:")
    print(angle_map.draw())
    
    angle_state = Statevector.from_instruction(angle_map)
    print(f"State probabilities: {angle_state.probabilities()}")
    
    # Amplitude encoding
    amp_data = np.array([0.6, 0.8, 0.0, 0.0])  # 4 elements for 2 qubits
    amp_map = amplitude_encoding(amp_data)
    print(f"\nAmplitude encoding (data: {amp_data}):")
    print(amp_map.draw())
    
    # Pauli feature map
    pauli_map = pauli_feature_map(sample_data[:2])  # Use 2 qubits for simplicity
    print(f"\nPauli feature map:")
    print(pauli_map.draw())
    
    pauli_state = Statevector.from_instruction(pauli_map)
    print(f"State probabilities: {pauli_state.probabilities()}")

def variational_classifier():
    """
    Exercise 4: Variational Quantum Classifier
    
    Implement a simple quantum classifier using variational circuits.
    We'll classify 2D points into two classes.
    """
    print("\n=== Exercise 4: Variational Quantum Classifier ===")
    
    def create_feature_map(x):
        """Create feature map for 2D input"""
        qc = QuantumCircuit(2)
        qc.h([0, 1])
        qc.rz(x[0], 0)
        qc.rz(x[1], 1)
        qc.cx(0, 1)
        qc.rz(x[0] * x[1], 1)
        qc.cx(0, 1)
        return qc
    
    def create_variational_circuit(theta):
        """Create variational ansatz"""
        qc = QuantumCircuit(2)
        qc.ry(theta[0], 0)
        qc.ry(theta[1], 1)
        qc.cx(0, 1)
        qc.ry(theta[2], 0)
        qc.ry(theta[3], 1)
        return qc
    
    def quantum_classifier(x, theta):
        """Complete quantum classifier circuit"""
        # Combine feature map and variational circuit
        feature_map = create_feature_map(x)
        var_circuit = create_variational_circuit(theta)
        
        full_circuit = QuantumCircuit(2, 1)
        full_circuit.compose(feature_map, inplace=True)
        full_circuit.compose(var_circuit, inplace=True)
        
        # Measure first qubit for classification
        full_circuit.measure(0, 0)
        
        return full_circuit
    
    # Generate synthetic training data
    np.random.seed(42)
    n_samples = 20
    
    # Class 0: points around (0, 0)
    class_0 = np.random.normal(0, 0.5, (n_samples//2, 2))
    labels_0 = np.zeros(n_samples//2)
    
    # Class 1: points around (1, 1)
    class_1 = np.random.normal(1, 0.5, (n_samples//2, 2))
    labels_1 = np.ones(n_samples//2)
    
    # Combine data
    X_train = np.vstack([class_0, class_1])
    y_train = np.hstack([labels_0, labels_1])
    
    print(f"Training data: {n_samples} samples, 2 features, 2 classes")
    
    def cost_function(theta):
        """Classification cost function"""
        total_loss = 0
        
        for i, (x, y) in enumerate(zip(X_train, y_train)):
            qc = quantum_classifier(x, theta)
            
            # Run circuit
            job = sampler.run(qc, shots=1000)
            result = job.result()
            counts = result.quasi_dists[0]
            
            # Get probability of measuring |1⟩
            prob_1 = counts.get(1, 0.0)
            
            # Binary cross-entropy loss
            epsilon = 1e-7  # Avoid log(0)
            prob_1 = max(min(prob_1, 1-epsilon), epsilon)
            
            if y == 1:
                loss = -np.log(prob_1)
            else:
                loss = -np.log(1 - prob_1)
            
            total_loss += loss
        
        return total_loss / len(X_train)
    
    # Train the classifier
    print("\nTraining quantum classifier...")
    initial_theta = np.random.random(4) * 2 * np.pi
    
    result = minimize(cost_function, initial_theta, method='COBYLA', 
                     options={'maxiter': 50})
    
    print(f"Training completed. Final loss: {result.fun:.4f}")
    print(f"Optimal parameters: {result.x}")
    
    # Test the classifier
    print("\n--- Testing classifier ---")
    test_points = [
        ([0, 0], 0),    # Should be class 0
        ([1, 1], 1),    # Should be class 1
        ([0.5, 0.5], None)  # Unknown
    ]
    
    for point, true_label in test_points:
        qc = quantum_classifier(point, result.x)
        job = sampler.run(qc, shots=1000)
        result_test = job.result()
        counts = result_test.quasi_dists[0]
        
        prob_1 = counts.get(1, 0.0)
        predicted = 1 if prob_1 > 0.5 else 0
        
        print(f"Point {point}: P(class 1) = {prob_1:.3f}, "
              f"Predicted: {predicted}, True: {true_label}")

def quantum_neural_network():
    """
    Exercise 5: Quantum Neural Network
    
    Implement a simple quantum neural network for function approximation.
    """
    print("\n=== Exercise 5: Quantum Neural Network ===")
    
    def qnn_layer(theta, n_qubits):
        """Single layer of quantum neural network"""
        qc = QuantumCircuit(n_qubits)
        
        # Rotation layer
        for i in range(n_qubits):
            qc.ry(theta[i], i)
        
        # Entangling layer
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)
        
        return qc
    
    def quantum_neural_network_circuit(x, theta, n_qubits=3, n_layers=2):
        """Complete QNN circuit"""
        qc = QuantumCircuit(n_qubits)
        
        # Input encoding
        for i in range(min(len(x), n_qubits)):
            qc.ry(x[i], i)
        
        # QNN layers
        param_idx = 0
        for layer in range(n_layers):
            layer_params = theta[param_idx:param_idx + n_qubits]
            qnn_layer_circuit = qnn_layer(layer_params, n_qubits)
            qc.compose(qnn_layer_circuit, inplace=True)
            param_idx += n_qubits
        
        return qc
    
    # Target function: f(x) = sin(πx)
    def target_function(x):
        return np.sin(np.pi * x)
    
    # Generate training data
    n_train = 10
    x_train = np.linspace(0, 1, n_train)
    y_train = target_function(x_train)
    
    print(f"Training QNN to approximate f(x) = sin(πx)")
    print(f"Training data: {n_train} points in [0, 1]")
    
    n_qubits = 3
    n_layers = 2
    n_params = n_qubits * n_layers
    
    def qnn_cost_function(theta):
        """QNN cost function"""
        total_loss = 0
        
        for i, (x, y_true) in enumerate(zip(x_train, y_train)):
            # Create QNN circuit
            qc = quantum_neural_network_circuit([x], theta, n_qubits, n_layers)
            
            # Measure expectation value of Z_0 as output
            z_observable = SparsePauliOp.from_list([("Z" + "I"*(n_qubits-1), 1.0)])
            
            job = estimator.run(qc, z_observable)
            result = job.result()
            y_pred = result.values[0]
            
            # Mean squared error
            loss = (y_pred - y_true) ** 2
            total_loss += loss
        
        return total_loss / len(x_train)
    
    # Train QNN
    print("\nTraining QNN...")
    initial_theta = np.random.random(n_params) * 2 * np.pi
    
    result = minimize(qnn_cost_function, initial_theta, method='COBYLA',
                     options={'maxiter': 100})
    
    print(f"Training completed. Final MSE: {result.fun:.6f}")
    
    # Test QNN
    print("\n--- Testing QNN ---")
    x_test = np.array([0.2, 0.5, 0.8])
    
    for x in x_test:
        qc = quantum_neural_network_circuit([x], result.x, n_qubits, n_layers)
        z_observable = SparsePauliOp.from_list([("Z" + "I"*(n_qubits-1), 1.0)])
        
        job = estimator.run(qc, z_observable)
        result_test = job.result()
        y_pred = result_test.values[0]
        y_true = target_function(x)
        
        print(f"x = {x:.1f}: QNN = {y_pred:.3f}, True = {y_true:.3f}, "
              f"Error = {abs(y_pred - y_true):.3f}")

def main():
    """Run all variational quantum algorithm exercises"""
    print("QUANTUM COMPUTING EXERCISES - PART 3: VARIATIONAL ALGORITHMS")
    print("=" * 70)
    
    # Run all exercises
    try:
        variational_quantum_eigensolver()
        quantum_approximate_optimization()
        quantum_feature_map()
        variational_classifier()
        quantum_neural_network()
    except Exception as e:
        print(f"Note: Some exercises may require additional setup. Error: {e}")
        print("This is normal in a simulated environment.")
    
    print("\n" + "=" * 70)
    print("SUMMARY: VARIATIONAL QUANTUM ALGORITHMS")
    print("=" * 70)
    
    print("\nAlgorithms covered:")
    print("1. VQE: Find ground state energies of quantum systems")
    print("2. QAOA: Solve combinatorial optimization problems")
    print("3. Feature Maps: Encode classical data into quantum states")
    print("4. Quantum Classifiers: Use variational circuits for machine learning")
    print("5. Quantum Neural Networks: Function approximation with quantum circuits")
    
    print("\nKey concepts:")
    print("- Variational circuits and parameter optimization")
    print("- Hybrid quantum-classical algorithms")
    print("- Quantum machine learning")
    print("- Feature encoding strategies")
    print("- Near-term quantum applications")
    
    print("\nNear-term applications:")
    print("- Quantum chemistry and materials science")
    print("- Combinatorial optimization")
    print("- Machine learning and pattern recognition")
    print("- Financial modeling")
    print("- Drug discovery")

if __name__ == "__main__":
    main()