"""
Quantum Hackathon API Client
============================

A Python client for interacting with the Swift-based Quantum Hackathon API.
This can be used within Jupyter notebooks to store and retrieve quantum experiment data.

Usage example:
    from quantum_api_client import QuantumAPIClient
    
    client = QuantumAPIClient()
    
    # Create a user
    user = client.create_user("alice", "alice@example.com", "Alice Johnson", "Advanced")
    
    # Store an experiment
    experiment = client.create_experiment(
        user_id=user['id'],
        name="Bell State Test",
        circuit_type="Entanglement",
        qubit_count=2,
        gate_sequence="H(0), CNOT(0,1)"
    )
    
    # Update results
    client.update_experiment_results(
        experiment['id'],
        measurement_results="00: 0.501, 11: 0.499",
        success_probability=0.95
    )
"""

import requests
import json
from typing import Dict, List, Optional, Any
import logging

class QuantumAPIClient:
    """Client for interacting with the Quantum Hackathon Swift API."""
    
    def __init__(self, base_url: str = "http://localhost:8080/api"):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL of the API (default: http://localhost:8080/api)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make an HTTP request to the API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, data=json.dumps(data) if data else None)
            elif method.upper() == 'PUT':
                response = self.session.put(url, data=json.dumps(data) if data else None)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            raise
    
    def health_check(self) -> bool:
        """Check if the API is running."""
        try:
            response = requests.get(f"{self.base_url}/../hello", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    # User management methods
    
    def create_user(self, username: str, email: str, full_name: str, 
                   experience_level: str, team_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            username: Unique username
            email: User's email address
            full_name: User's full name
            experience_level: Experience level (e.g., "Beginner", "Intermediate", "Advanced")
            team_name: Optional team name
            
        Returns:
            Created user data
        """
        user_data = {
            "username": username,
            "email": email,
            "fullName": full_name,
            "experienceLevel": experience_level
        }
        if team_name:
            user_data["teamName"] = team_name
            
        return self._make_request('POST', '/users', user_data)
    
    def get_users(self) -> Dict[str, Any]:
        """Get all users."""
        return self._make_request('GET', '/users')
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get a specific user by ID."""
        return self._make_request('GET', f'/users/{user_id}')
    
    def get_user_experiments(self, user_id: str) -> Dict[str, Any]:
        """Get all experiments for a specific user."""
        return self._make_request('GET', f'/users/{user_id}/experiments')
    
    # Experiment management methods
    
    def create_experiment(self, user_id: str, name: str, circuit_type: str,
                         qubit_count: int, gate_sequence: str,
                         measurement_results: Optional[str] = None,
                         success_probability: Optional[float] = None) -> Dict[str, Any]:
        """
        Create a new quantum experiment.
        
        Args:
            user_id: ID of the user creating the experiment
            name: Experiment name
            circuit_type: Type of quantum circuit (e.g., "Entanglement", "Single Qubit")
            qubit_count: Number of qubits in the circuit
            gate_sequence: String describing the gate sequence
            measurement_results: Optional measurement results
            success_probability: Optional success probability
            
        Returns:
            Created experiment data
        """
        experiment_data = {
            "name": name,
            "circuitType": circuit_type,
            "qubitCount": qubit_count,
            "gateSequence": gate_sequence,
            "user": {"id": user_id}
        }
        
        if measurement_results:
            experiment_data["measurementResults"] = measurement_results
        if success_probability is not None:
            experiment_data["successProbability"] = success_probability
            
        return self._make_request('POST', '/experiments', experiment_data)
    
    def get_experiments(self) -> Dict[str, Any]:
        """Get all experiments."""
        return self._make_request('GET', '/experiments')
    
    def get_experiment(self, experiment_id: str) -> Dict[str, Any]:
        """Get a specific experiment by ID."""
        return self._make_request('GET', f'/experiments/{experiment_id}')
    
    def update_experiment_results(self, experiment_id: str, 
                                measurement_results: str,
                                success_probability: float) -> Dict[str, Any]:
        """
        Update the results of an experiment.
        
        Args:
            experiment_id: ID of the experiment to update
            measurement_results: String describing measurement results
            success_probability: Success probability (0.0 to 1.0)
            
        Returns:
            Updated experiment data
        """
        update_data = {
            "measurementResults": measurement_results,
            "successProbability": success_probability
        }
        
        return self._make_request('PUT', f'/experiments/{experiment_id}/results', update_data)
    
    # Statistics methods
    
    def get_stats(self) -> Dict[str, Any]:
        """Get hackathon statistics."""
        return self._make_request('GET', '/stats')
    
    # Convenience methods for Jupyter integration
    
    def quick_experiment(self, username: str, experiment_name: str, 
                        circuit_type: str, qubit_count: int, 
                        gate_sequence: str) -> str:
        """
        Quickly create a user and experiment, return experiment ID.
        Useful for rapid prototyping in notebooks.
        """
        try:
            # Try to find existing user
            users_response = self.get_users()
            users = users_response if isinstance(users_response, list) else []
            user = next((u for u in users if u.get('username') == username), None)
            
            if not user:
                # Create new user
                user = self.create_user(
                    username=username,
                    email=f"{username}@hackathon.local",
                    full_name=username.replace('_', ' ').title(),
                    experience_level="Intermediate"
                )
                self.logger.info(f"Created new user: {username}")
            
            # Create experiment
            experiment = self.create_experiment(
                user_id=user.get('id', ''),
                name=experiment_name,
                circuit_type=circuit_type,
                qubit_count=qubit_count,
                gate_sequence=gate_sequence
            )
            
            self.logger.info(f"Created experiment: {experiment_name}")
            return experiment.get('id', '')
            
        except Exception as e:
            self.logger.error(f"Failed to create quick experiment: {e}")
            raise
    
    def store_qiskit_result(self, experiment_id: str, qiskit_result) -> Dict[str, Any]:
        """
        Store results from a Qiskit experiment.
        
        Args:
            experiment_id: ID of the experiment
            qiskit_result: Qiskit result object
            
        Returns:
            Updated experiment data
        """
        try:
            # Extract measurement results
            counts = qiskit_result.get_counts()
            total_shots = sum(counts.values())
            
            # Format results string
            result_str = ", ".join([f"{state}: {count/total_shots:.3f}" 
                                  for state, count in counts.items()])
            
            # Calculate success probability (assuming |00⟩ state is success for entanglement)
            success_prob = counts.get('00', 0) / total_shots if '00' in counts else 0.5
            
            return self.update_experiment_results(
                experiment_id=experiment_id,
                measurement_results=result_str,
                success_probability=success_prob
            )
            
        except Exception as e:
            self.logger.error(f"Failed to store Qiskit result: {e}")
            raise

# Example usage function for notebooks
def demo_api_usage():
    """Demonstrate API usage - can be called from Jupyter notebooks."""
    client = QuantumAPIClient()
    
    print("🚀 Quantum Hackathon API Demo")
    print("=" * 30)
    
    # Check API health
    if not client.health_check():
        print("❌ API is not running. Please start the server first.")
        return
    
    print("✅ API is running")
    
    try:
        # Create experiment quickly
        experiment_id = client.quick_experiment(
            username="demo_user",
            experiment_name="Demo Bell State",
            circuit_type="Entanglement",
            qubit_count=2,
            gate_sequence="H(0), CNOT(0,1)"
        )
        
        print(f"📊 Created experiment: {experiment_id}")
        
        # Simulate some results
        client.update_experiment_results(
            experiment_id=experiment_id,
            measurement_results="00: 0.487, 01: 0.013, 10: 0.017, 11: 0.483",
            success_probability=0.94
        )
        
        print("📈 Updated with simulated results")
        
        # Get stats
        stats = client.get_stats()
        print(f"📊 Current stats: {stats}")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    demo_api_usage()