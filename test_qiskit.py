#!/usr/bin/env python3
"""
Qiskit Installation Test Program
This program verifies that Qiskit is working correctly by creating and simulating a simple quantum circuit.
"""

import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def main():
    print("🔬 Testing Qiskit Installation")
    print(f"📦 Qiskit Version: {qiskit.__version__}")
    print("-" * 50)
    
    # Create a simple quantum circuit
    print("🔧 Creating a 2-qubit quantum circuit...")
    qc = QuantumCircuit(2, 2)
    
    # Add quantum gates
    qc.h(0)        # Hadamard gate on qubit 0 (creates superposition)
    qc.cx(0, 1)    # CNOT gate (creates entanglement)
    qc.measure_all()  # Measure all qubits
    
    print("✅ Quantum circuit created successfully!")
    print(f"🔍 Circuit depth: {qc.depth()}")
    print(f"🔍 Number of qubits: {qc.num_qubits}")
    print(f"🔍 Number of classical bits: {qc.num_clbits}")
    
    # Print the circuit
    print("\n📊 Quantum Circuit Diagram:")
    print(qc.draw(output='text'))
    
    # Simulate the circuit
    print("\n🖥️  Running simulation...")
    simulator = AerSimulator()
    
    # Transpile the circuit for the simulator
    transpiled_qc = transpile(qc, simulator)
    
    # Run the simulation
    job = simulator.run(transpiled_qc, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    print("📈 Simulation Results:")
    for state, count in counts.items():
        percentage = (count / 1024) * 100
        print(f"   |{state}⟩: {count} times ({percentage:.1f}%)")
    
    # Expected results for Bell state: roughly 50% |00⟩ and 50% |11⟩
    expected_states = ['00', '11']
    actual_states = list(counts.keys())
    
    print("\n🧪 Verification:")
    if set(actual_states).issubset(set(expected_states)):
        print("✅ Results match expected Bell state distribution!")
        print("   The qubits are properly entangled - measuring 00 or 11 only.")
    else:
        print("⚠️  Unexpected results - check circuit or simulation")
    
    print("\n🎉 Qiskit test completed successfully!")
    print("🚀 Ready for quantum computing development!")

if __name__ == "__main__":
    main()