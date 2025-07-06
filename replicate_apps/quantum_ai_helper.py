"""
Quantum AI Helper - Replicate Integration for Qiskit Hackathon
Provides AI-enhanced quantum computing capabilities using Replicate models.
"""

import os
import replicate
from dotenv import load_dotenv
import numpy as np
from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import requests

# Load environment variables
load_dotenv()

class QuantumAIHelper:
    def __init__(self):
        """Initialize the Quantum AI Helper with Replicate client."""
        self.replicate_client = replicate
        api_token = os.getenv('REPLICATE_API_TOKEN')
        if api_token:
            os.environ['REPLICATE_API_TOKEN'] = api_token
    
    def analyze_circuit_with_ai(self, quantum_circuit, description=""):
        """
        Analyze a quantum circuit using AI models from Replicate.
        
        Args:
            quantum_circuit: Qiskit QuantumCircuit object
            description: Optional description of what the circuit should do
        
        Returns:
            AI analysis and suggestions
        """
        try:
            # Convert circuit to image
            circuit_image = self._circuit_to_image(quantum_circuit)
            
            # Use Replicate's image analysis model
            output = replicate.run(
                "salesforce/blip:2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746",
                input={
                    "image": circuit_image,
                    "question": f"Describe this quantum circuit diagram. {description}"
                }
            )
            
            return {
                "analysis": output,
                "circuit_gates": len(quantum_circuit.data),
                "qubits": quantum_circuit.num_qubits,
                "suggestions": self._generate_suggestions(quantum_circuit)
            }
        except Exception as e:
            return {"error": f"AI analysis failed: {str(e)}"}
    
    def explain_quantum_concept(self, concept, level="beginner"):
        """
        Get AI-generated explanations of quantum concepts.
        
        Args:
            concept: Quantum computing concept to explain
            level: Explanation level (beginner, intermediate, advanced)
        
        Returns:
            AI-generated explanation
        """
        try:
            prompt = f"""
            Explain the quantum computing concept '{concept}' at a {level} level.
            Include practical examples and how it relates to quantum circuits.
            Make it educational and easy to understand for hackathon participants.
            """
            
            output = replicate.run(
                "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
                input={
                    "prompt": prompt,
                    "max_new_tokens": 500,
                    "temperature": 0.7
                }
            )
            
            return {"explanation": "".join(output)}
        except Exception as e:
            return {"error": f"Concept explanation failed: {str(e)}"}
    
    def generate_quantum_art(self, quantum_state, style="abstract"):
        """
        Generate artistic visualizations of quantum states using AI.
        
        Args:
            quantum_state: Quantum state vector or description
            style: Art style for visualization
        
        Returns:
            Generated artwork URL
        """
        try:
            prompt = f"""
            Create an abstract artistic visualization representing a quantum state.
            Style: {style}
            The image should represent quantum superposition, entanglement, and wave functions.
            Use colors that represent the quantum state: {quantum_state}
            Make it beautiful and scientifically inspired.
            """
            
            output = replicate.run(
                "stability-ai/stable-diffusion:27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
                input={
                    "prompt": prompt,
                    "width": 512,
                    "height": 512,
                    "num_inference_steps": 50
                }
            )
            
            return {"artwork_url": output[0] if output else None}
        except Exception as e:
            return {"error": f"Quantum art generation failed: {str(e)}"}
    
    def optimize_circuit_with_ai(self, quantum_circuit, target="depth"):
        """
        Get AI suggestions for optimizing quantum circuits.
        
        Args:
            quantum_circuit: Qiskit QuantumCircuit object
            target: Optimization target (depth, gates, fidelity)
        
        Returns:
            Optimization suggestions
        """
        circuit_info = {
            "gates": len(quantum_circuit.data),
            "qubits": quantum_circuit.num_qubits,
            "depth": quantum_circuit.depth(),
            "gate_types": [gate[0].name for gate in quantum_circuit.data]
        }
        
        prompt = f"""
        Analyze this quantum circuit and suggest optimizations:
        - Number of gates: {circuit_info['gates']}
        - Number of qubits: {circuit_info['qubits']}
        - Circuit depth: {circuit_info['depth']}
        - Gate types: {circuit_info['gate_types']}
        
        Target optimization: {target}
        
        Provide specific suggestions for improving this circuit.
        """
        
        try:
            output = replicate.run(
                "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
                input={
                    "prompt": prompt,
                    "max_new_tokens": 400,
                    "temperature": 0.6
                }
            )
            
            return {
                "optimization_suggestions": "".join(output),
                "current_metrics": circuit_info
            }
        except Exception as e:
            return {"error": f"Circuit optimization failed: {str(e)}"}
    
    def _circuit_to_image(self, quantum_circuit):
        """Convert quantum circuit to base64 image for AI analysis."""
        try:
            # Create circuit diagram
            fig, ax = plt.subplots(figsize=(10, 6))
            quantum_circuit.draw(output='mpl', ax=ax)
            
            # Convert to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
            buffer.seek(0)
            
            # Encode as base64
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close(fig)
            
            return f"data:image/png;base64,{image_base64}"
        except Exception as e:
            print(f"Error converting circuit to image: {e}")
            return None
    
    def _generate_suggestions(self, quantum_circuit):
        """Generate basic suggestions for quantum circuit improvement."""
        suggestions = []
        
        if quantum_circuit.depth() > 10:
            suggestions.append("Consider reducing circuit depth for better fidelity")
        
        if quantum_circuit.num_qubits > 5:
            suggestions.append("Large number of qubits - consider error correction")
        
        gate_counts = {}
        for gate in quantum_circuit.data:
            gate_name = gate[0].name
            gate_counts[gate_name] = gate_counts.get(gate_name, 0) + 1
        
        if gate_counts.get('cx', 0) > quantum_circuit.num_qubits:
            suggestions.append("Many CNOT gates detected - consider gate optimization")
        
        return suggestions

# Convenience functions for easy usage
def get_ai_helper():
    """Get a configured QuantumAIHelper instance."""
    return QuantumAIHelper()

def quick_circuit_analysis(circuit):
    """Quick analysis of a quantum circuit using AI."""
    helper = get_ai_helper()
    return helper.analyze_circuit_with_ai(circuit)

def explain_concept(concept, level="beginner"):
    """Quick explanation of a quantum concept."""
    helper = get_ai_helper()
    return helper.explain_quantum_concept(concept, level)