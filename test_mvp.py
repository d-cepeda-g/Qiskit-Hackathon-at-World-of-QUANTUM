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
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator
    from qiskit.quantum_info import Statevector
    from qiskit.visualization import plot_bloch_multivector, plot_histogram
    print(f"✅ Qiskit version: {qiskit.__version__}")
    
    # Test basic quantum circuit
    print("\n🔬 Testing quantum circuit creation...")
    qc = QuantumCircuit(1)
    qc.h(0)  # Hadamard gate
    state = Statevector.from_instruction(qc)
    print("✅ Created superposition state |+⟩")
    
    # Test measurement
    print("\n📏 Testing measurement...")
    qc_meas = QuantumCircuit(1, 1)
    qc_meas.h(0)
    qc_meas.measure(0, 0)
    
    backend = AerSimulator()
    transpiled_circuit = transpile(qc_meas, backend)
    job = backend.run(transpiled_circuit, shots=100)
    counts = job.result().get_counts()
    print(f"✅ Measurement results: {counts}")
    
    print("\n🎉 All tests passed! Your Qiskit MVP is ready!")
    print("\n🚀 You can now run the exercises in the Exercises/ directory")
    print("   Start with: jupyter notebook Exercises/Easy_Single_Qubit_Gates.ipynb")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Please install requirements: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Please check your Qiskit installation")

