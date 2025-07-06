#!/usr/bin/env python3
"""
🎨 Enhanced Visual Styling Demo for Quantum Computing
====================================================

This script demonstrates how to use the beautiful, modern styling
for quantum computing visualizations in your Qiskit exercises.

Run this script to see the difference between standard and enhanced visuals!
"""

# Standard imports
import numpy as np
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_bloch_multivector, plot_histogram
import matplotlib.pyplot as plt

# Import our enhanced styling
try:
    from quantum_visual_style import *
    print("🎨 Enhanced visual styling loaded successfully!")
    enhanced_available = True
except ImportError:
    print("❌ Enhanced styling not available. Using standard Qiskit visuals.")
    enhanced_available = False

def demo_bloch_sphere_enhancement():
    """Demonstrate enhanced Bloch sphere visualizations."""
    print("\n🌍 Creating Bloch Sphere Demonstrations...")
    
    # Create some interesting quantum states
    states = {
        "|0⟩": Statevector([1, 0]),
        "|1⟩": Statevector([0, 1]),
        "|+⟩": Statevector([1/np.sqrt(2), 1/np.sqrt(2)]),
        "|-⟩": Statevector([1/np.sqrt(2), -1/np.sqrt(2)]),
        "|i⟩": Statevector([1/np.sqrt(2), 1j/np.sqrt(2)])
    }
    
    for name, state in states.items():
        print(f"  • Visualizing {name} state...")
        
        if enhanced_available:
            # Use enhanced styling
            styled_bloch_sphere(state, f"Enhanced {name} State Visualization")
            plt.savefig(f'enhanced_{name.replace("|", "").replace("⟩", "")}_state.png', 
                       dpi=150, bbox_inches='tight')
            plt.show()
        else:
            # Standard visualization
            plot_bloch_multivector(state, title=f"Standard {name} State")
            plt.show()

def demo_measurement_histogram():
    """Demonstrate enhanced measurement result visualizations."""
    print("\n📊 Creating Measurement Histogram Demonstrations...")
    
    # Create a Bell state circuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Run simulation
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1000)
    counts = job.result().get_counts()
    
    print("  • Bell state measurement results:")
    print(f"    Counts: {counts}")
    
    if enhanced_available:
        # Use enhanced styling
        styled_histogram(counts, "🔬 Enhanced Bell State Measurements")
        plt.savefig('enhanced_bell_histogram.png', dpi=150, bbox_inches='tight')
        plt.show()
    else:
        # Standard visualization
        plot_histogram(counts, title="Standard Bell State Measurements")
        plt.show()

def demo_circuit_visualization():
    """Demonstrate enhanced circuit diagrams."""
    print("\n⚡ Creating Circuit Diagram Demonstrations...")
    
    # Create a more complex circuit
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.ry(np.pi/4, 1)
    qc.cx(0, 2)
    qc.measure_all()
    
    print("  • Complex quantum circuit with entanglement...")
    
    if enhanced_available:
        # Use enhanced styling
        circuit_fig = styled_circuit_drawer(qc, figsize=(14, 8))
        if hasattr(circuit_fig, 'savefig'):
            circuit_fig.savefig('enhanced_circuit.png', dpi=150, bbox_inches='tight')
        print("    ✨ Enhanced circuit diagram created!")
    else:
        # Standard visualization
        print("    📋 Standard circuit:")
        print(qc.draw())

def demo_comparison_plots():
    """Demonstrate state comparison visualizations."""
    if not enhanced_available:
        print("\n⚠️ State comparison plots require enhanced styling.")
        return
        
    print("\n🔄 Creating State Comparison Demonstrations...")
    
    # Create multiple related states
    states = [
        Statevector([1, 0]),  # |0⟩
        Statevector([0, 1]),  # |1⟩
        Statevector([1/np.sqrt(2), 1/np.sqrt(2)]),  # |+⟩
        Statevector([1/np.sqrt(2), -1/np.sqrt(2)])  # |-⟩
    ]
    labels = ["|0⟩", "|1⟩", "|+⟩", "|-⟩"]
    
    # Create comparison plot
    create_state_comparison_plot(states, labels, "🎯 Computational vs. Superposition States")
    plt.savefig('enhanced_state_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Create probability distribution
    probabilities = [0.5, 0.0, 0.0, 0.5]  # Bell state probabilities
    create_probability_distribution_plot(
        probabilities, 
        ['|00⟩', '|01⟩', '|10⟩', '|11⟩'], 
        "🎲 Bell State Probability Distribution"
    )
    plt.savefig('enhanced_probability_dist.png', dpi=150, bbox_inches='tight')
    plt.show()

def main():
    """Run all demonstrations."""
    print("=" * 60)
    print("🎨 ENHANCED VISUAL STYLING DEMONSTRATION")
    print("=" * 60)
    print("This demo shows the beautiful, modern styling capabilities")
    print("for quantum computing visualizations in Qiskit.")
    print("=" * 60)
    
    # Run demonstrations
    demo_bloch_sphere_enhancement()
    demo_measurement_histogram()
    demo_circuit_visualization()
    demo_comparison_plots()
    
    print("\n" + "=" * 60)
    print("✅ DEMONSTRATION COMPLETE!")
    print("=" * 60)
    
    if enhanced_available:
        print("🎉 All enhanced visualizations have been created!")
        print("📁 Check the generated PNG files for high-quality outputs.")
        print("\n💡 To use in your notebooks:")
        print("   • Replace 'plot_bloch_multivector()' with 'styled_bloch_sphere()'")
        print("   • Replace 'plot_histogram()' with 'styled_histogram()'")
        print("   • Use 'styled_circuit_drawer()' for beautiful circuits")
        print("\n🌟 Your quantum visualizations will look professional and modern!")
    else:
        print("ℹ️ To get enhanced styling:")
        print("   1. Ensure 'quantum_visual_style.py' is in your Python path")
        print("   2. Install required packages: matplotlib, seaborn, qiskit")
        print("   3. Re-run this demo to see the enhanced visuals!")

if __name__ == "__main__":
    main()