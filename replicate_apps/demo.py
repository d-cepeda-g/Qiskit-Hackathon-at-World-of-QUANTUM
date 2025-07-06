#!/usr/bin/env python3
"""
Demo script for Replicate AI integration with Qiskit
Shows how to use AI models to enhance quantum computing workflows.
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from quantum_ai_helper import QuantumAIHelper, quick_circuit_analysis, explain_concept
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    import numpy as np
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages: pip install -r requirements.txt")
    sys.exit(1)

def main():
    """Main demo function."""
    print("🚀 Quantum AI Demo - Replicate Integration")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    if not os.getenv('REPLICATE_API_TOKEN'):
        print("⚠️  Warning: REPLICATE_API_TOKEN not found in environment")
        print("Copy .env.example to .env and add your API token to use AI features")
        print("Demo will continue with limited functionality...\n")
    
    # Initialize AI helper
    try:
        ai_helper = QuantumAIHelper()
        print("✅ Quantum AI Helper initialized!\n")
    except Exception as e:
        print(f"❌ Failed to initialize AI helper: {e}")
        return
    
    # Demo 1: Create and analyze a Bell state circuit
    print("📊 Demo 1: AI Circuit Analysis")
    print("-" * 30)
    
    # Create Bell state circuit
    qc = QuantumCircuit(2)
    qc.h(0)  # Hadamard on qubit 0
    qc.cx(0, 1)  # CNOT gate
    
    print("Circuit created:")
    print(qc.draw(output='text'))
    
    # Basic analysis without AI (always works)
    print(f"\nBasic Analysis:")
    print(f"- Number of qubits: {qc.num_qubits}")
    print(f"- Number of gates: {len(qc.data)}")
    print(f"- Circuit depth: {qc.depth()}")
    print(f"- Gate types: {[gate[0].name for gate in qc.data]}")
    
    # AI analysis (requires API key)
    if os.getenv('REPLICATE_API_TOKEN'):
        try:
            print("\n🤖 Getting AI analysis...")
            analysis = ai_helper.analyze_circuit_with_ai(
                qc, 
                "This circuit creates a Bell state showing quantum entanglement"
            )
            
            if 'error' not in analysis:
                print("AI Analysis Result:")
                print(f"- AI Description: {analysis.get('analysis', 'No analysis')}")
                print(f"- Suggestions: {analysis.get('suggestions', [])}")
            else:
                print(f"AI analysis failed: {analysis['error']}")
        except Exception as e:
            print(f"AI analysis error: {e}")
    else:
        print("🔒 AI analysis skipped (no API token)")
    
    print("\n" + "=" * 50)
    
    # Demo 2: Concept explanation
    print("📚 Demo 2: AI Concept Explanation")
    print("-" * 35)
    
    if os.getenv('REPLICATE_API_TOKEN'):
        try:
            print("🤖 Getting AI explanation of quantum entanglement...")
            explanation = ai_helper.explain_quantum_concept("quantum entanglement", "beginner")
            
            if 'error' not in explanation:
                result = explanation.get('explanation', 'No explanation available')
                print("AI Explanation:")
                print(result[:500] + "..." if len(result) > 500 else result)
            else:
                print(f"Concept explanation failed: {explanation['error']}")
        except Exception as e:
            print(f"Concept explanation error: {e}")
    else:
        print("🔒 AI concept explanation skipped (no API token)")
        print("Quantum entanglement is a quantum mechanical phenomenon where")
        print("two or more particles become connected in such a way that the")
        print("quantum state of each particle cannot be described independently.")
    
    print("\n" + "=" * 50)
    
    # Demo 3: Circuit optimization suggestions
    print("⚡ Demo 3: Circuit Optimization")
    print("-" * 32)
    
    # Create a more complex circuit
    complex_qc = QuantumCircuit(3)
    complex_qc.h(0)
    complex_qc.cx(0, 1)
    complex_qc.cx(1, 2)
    complex_qc.rz(np.pi/4, 0)
    complex_qc.ry(np.pi/3, 1)
    complex_qc.cx(2, 0)
    complex_qc.h(2)
    
    print("Complex circuit created:")
    print(complex_qc.draw(output='text'))
    
    print(f"\nCircuit metrics:")
    print(f"- Qubits: {complex_qc.num_qubits}")
    print(f"- Gates: {len(complex_qc.data)}")
    print(f"- Depth: {complex_qc.depth()}")
    
    if os.getenv('REPLICATE_API_TOKEN'):
        try:
            print("\n🤖 Getting optimization suggestions...")
            optimization = ai_helper.optimize_circuit_with_ai(complex_qc, "depth")
            
            if 'error' not in optimization:
                suggestions = optimization.get('optimization_suggestions', 'No suggestions')
                print("AI Optimization Suggestions:")
                print(suggestions[:400] + "..." if len(suggestions) > 400 else suggestions)
            else:
                print(f"Optimization failed: {optimization['error']}")
        except Exception as e:
            print(f"Optimization error: {e}")
    else:
        print("🔒 AI optimization skipped (no API token)")
        print("Consider these general optimization tips:")
        print("- Reduce circuit depth by parallelizing gates")
        print("- Minimize CNOT gates which are typically noisy")
        print("- Use gate commutation rules to reorganize circuit")
    
    print("\n" + "=" * 50)
    print("🎯 Demo completed!")
    print("\nTo enable full AI features:")
    print("1. Get a Replicate API token from https://replicate.com")
    print("2. Copy .env.example to .env")
    print("3. Add your token to the .env file")
    print("4. Run this demo again")
    
    print("\n💡 Hackathon Ideas:")
    print("- Quantum education assistant with AI explanations")
    print("- Circuit optimizer using machine learning")
    print("- Quantum art generator using AI image models")
    print("- Natural language quantum programming interface")

if __name__ == "__main__":
    main()