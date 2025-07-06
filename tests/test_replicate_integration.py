#!/usr/bin/env python3
"""
Test suite for Replicate AI integration
Tests all functionality without requiring actual API calls
"""

import unittest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
import tempfile
import json

# Add replicate_apps to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'replicate_apps'))

class TestReplicateIntegration(unittest.TestCase):
    """Test suite for Replicate AI integration"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_env_file = tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False)
        self.test_env_file.write('REPLICATE_API_TOKEN=test_token_12345\n')
        self.test_env_file.close()
        
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_env_file.name):
            os.unlink(self.test_env_file.name)
    
    def test_package_imports(self):
        """Test that all required packages can be imported"""
        try:
            import replicate
            import numpy as np
            import matplotlib.pyplot as plt
            import requests
            from dotenv import load_dotenv
            self.assertTrue(True, "All packages imported successfully")
        except ImportError as e:
            self.fail(f"Package import failed: {e}")
    
    def test_environment_loading(self):
        """Test environment variable loading"""
        from dotenv import load_dotenv
        
        # Test loading from our test file
        load_dotenv(self.test_env_file.name)
        token = os.getenv('REPLICATE_API_TOKEN')
        self.assertEqual(token, 'test_token_12345')
    
    @patch('replicate.run')
    def test_replicate_text_generation(self, mock_run):
        """Test text generation functionality"""
        # Mock the replicate.run response
        mock_run.return_value = ["This is a test response from AI"]
        
        import replicate
        
        # Set up environment
        os.environ['REPLICATE_API_TOKEN'] = 'test_token'
        
        # Test call
        result = replicate.run(
            "meta/llama-2-70b-chat",
            input={"prompt": "Test prompt"}
        )
        
        # Verify
        self.assertEqual(result, ["This is a test response from AI"])
        mock_run.assert_called_once()
    
    @patch('replicate.run')
    def test_replicate_image_generation(self, mock_run):
        """Test image generation functionality"""
        # Mock the replicate.run response
        mock_run.return_value = ["https://example.com/generated_image.png"]
        
        import replicate
        
        # Set up environment
        os.environ['REPLICATE_API_TOKEN'] = 'test_token'
        
        # Test call
        result = replicate.run(
            "stability-ai/stable-diffusion",
            input={
                "prompt": "A beautiful quantum circuit",
                "width": 512,
                "height": 512
            }
        )
        
        # Verify
        self.assertEqual(result, ["https://example.com/generated_image.png"])
        mock_run.assert_called_once()
    
    def test_error_handling_no_token(self):
        """Test error handling when no API token is provided"""
        # Remove token from environment
        if 'REPLICATE_API_TOKEN' in os.environ:
            del os.environ['REPLICATE_API_TOKEN']
        
        # This should not crash the application
        token = os.getenv('REPLICATE_API_TOKEN')
        self.assertIsNone(token)
    
    @patch('replicate.run')
    def test_error_handling_api_failure(self, mock_run):
        """Test error handling when API call fails"""
        # Mock API failure
        mock_run.side_effect = Exception("API Error: Rate limit exceeded")
        
        import replicate
        
        # Set up environment
        os.environ['REPLICATE_API_TOKEN'] = 'test_token'
        
        # Test that exception is raised
        with self.assertRaises(Exception) as context:
            replicate.run("test-model", input={"prompt": "test"})
        
        self.assertIn("API Error", str(context.exception))


class TestQuantumAIHelper(unittest.TestCase):
    """Test the QuantumAIHelper class if Qiskit is available"""
    
    def setUp(self):
        """Set up test environment"""
        os.environ['REPLICATE_API_TOKEN'] = 'test_token_12345'
    
    def test_ai_helper_initialization(self):
        """Test that QuantumAIHelper can be initialized"""
        try:
            from quantum_ai_helper import QuantumAIHelper
            helper = QuantumAIHelper()
            self.assertIsNotNone(helper)
        except ImportError:
            # Skip if Qiskit not available
            self.skipTest("Qiskit not available, skipping QuantumAIHelper tests")
    
    @patch('replicate.run')
    def test_concept_explanation(self, mock_run):
        """Test AI concept explanation functionality"""
        try:
            from quantum_ai_helper import QuantumAIHelper
            
            # Mock response
            mock_run.return_value = ["Quantum entanglement is a phenomenon where..."]
            
            helper = QuantumAIHelper()
            result = helper.explain_quantum_concept("entanglement", "beginner")
            
            self.assertIn("explanation", result)
            self.assertEqual(result["explanation"], "Quantum entanglement is a phenomenon where...")
            
        except ImportError:
            self.skipTest("Qiskit not available, skipping concept explanation test")
    
    @patch('replicate.run')
    def test_circuit_optimization(self, mock_run):
        """Test circuit optimization suggestions"""
        try:
            from quantum_ai_helper import QuantumAIHelper
            from qiskit import QuantumCircuit
            
            # Mock response
            mock_run.return_value = ["Consider reducing circuit depth by..."]
            
            # Create test circuit
            qc = QuantumCircuit(2)
            qc.h(0)
            qc.cx(0, 1)
            
            helper = QuantumAIHelper()
            result = helper.optimize_circuit_with_ai(qc, "depth")
            
            self.assertIn("optimization_suggestions", result)
            self.assertIn("current_metrics", result)
            
        except ImportError:
            self.skipTest("Qiskit not available, skipping circuit optimization test")


class TestDemoScripts(unittest.TestCase):
    """Test the demo scripts"""
    
    def test_simple_demo_execution(self):
        """Test that simple demo can be executed"""
        import subprocess
        import os
        
        # Get the path to the demo script
        demo_path = os.path.join(os.path.dirname(__file__), '..', 'replicate_apps', 'simple_demo.py')
        
        # Run the demo with test environment
        env = os.environ.copy()
        env['REPLICATE_API_TOKEN'] = 'test_token_12345'
        
        try:
            result = subprocess.run([sys.executable, demo_path], 
                                  capture_output=True, 
                                  text=True, 
                                  env=env,
                                  timeout=30)
            
            # Check that it completed successfully
            self.assertEqual(result.returncode, 0, f"Demo failed with error: {result.stderr}")
            self.assertIn("Replicate package imported successfully", result.stdout)
            self.assertIn("Demo completed", result.stdout)
            
        except subprocess.TimeoutExpired:
            self.fail("Demo script timed out")
        except FileNotFoundError:
            self.fail("Demo script not found")


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions and helpers"""
    
    def test_api_token_validation(self):
        """Test API token validation"""
        # Test valid token format (basic check)
        valid_tokens = [
            "r8_test123",
            "test_token_12345",
            "abcd1234efgh5678"
        ]
        
        invalid_tokens = [
            "",
            None,
            "   ",
            "short"
        ]
        
        for token in valid_tokens:
            self.assertIsNotNone(token)
            self.assertGreater(len(token), 5)
        
        for token in invalid_tokens:
            if token is not None:
                self.assertLessEqual(len(token.strip()), 5)
    
    def test_model_name_validation(self):
        """Test model name format validation"""
        valid_models = [
            "meta/llama-2-70b-chat",
            "stability-ai/stable-diffusion",
            "salesforce/blip"
        ]
        
        for model in valid_models:
            self.assertIn("/", model)
            parts = model.split("/")
            self.assertEqual(len(parts), 2)
            self.assertGreater(len(parts[0]), 0)
            self.assertGreater(len(parts[1]), 0)


class TestIntegrationWorkflow(unittest.TestCase):
    """Test complete integration workflows"""
    
    @patch('replicate.run')
    def test_complete_ai_workflow(self, mock_run):
        """Test a complete AI-enhanced workflow"""
        # Mock different types of AI responses
        def mock_run_side_effect(model, input):
            if "llama" in model:
                return ["This is AI-generated text explaining the concept."]
            elif "stable-diffusion" in model:
                return ["https://example.com/generated_image.png"]
            elif "blip" in model:
                return "This image shows a quantum circuit with Hadamard and CNOT gates."
            else:
                return ["Generic AI response"]
        
        mock_run.side_effect = mock_run_side_effect
        
        import replicate
        os.environ['REPLICATE_API_TOKEN'] = 'test_token'
        
        # Test text generation
        text_result = replicate.run(
            "meta/llama-2-70b-chat",
            input={"prompt": "Explain quantum computing"}
        )
        self.assertEqual(text_result, ["This is AI-generated text explaining the concept."])
        
        # Test image generation
        image_result = replicate.run(
            "stability-ai/stable-diffusion",
            input={"prompt": "quantum circuit visualization"}
        )
        self.assertEqual(image_result, ["https://example.com/generated_image.png"])
        
        # Verify all calls were made
        self.assertEqual(mock_run.call_count, 2)


def run_tests():
    """Run all tests and save results"""
    # Create test results directory
    os.makedirs('test_results', exist_ok=True)
    
    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    # Custom test runner that saves results
    with open('test_results/test_report.txt', 'w') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        result = runner.run(suite)
        
        # Also print to console
        print(f"\n{'='*60}")
        print("🧪 TEST RESULTS SUMMARY")
        print(f"{'='*60}")
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
        
        if result.failures:
            print(f"\n❌ FAILURES ({len(result.failures)}):")
            for test, traceback in result.failures:
                print(f"  - {test}")
        
        if result.errors:
            print(f"\n🚨 ERRORS ({len(result.errors)}):")
            for test, traceback in result.errors:
                print(f"  - {test}")
        
        if not result.failures and not result.errors:
            print("\n✅ ALL TESTS PASSED!")
        
        print(f"{'='*60}")
        print("📁 Detailed results saved to: test_results/test_report.txt")
        
        return result


if __name__ == '__main__':
    run_tests()