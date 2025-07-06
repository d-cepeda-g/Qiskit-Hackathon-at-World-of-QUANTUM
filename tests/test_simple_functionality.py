#!/usr/bin/env python3
"""
Simple functionality tests for Replicate integration
Basic tests that verify setup and imports
"""

import unittest
import os
import sys
import subprocess

class TestBasicSetup(unittest.TestCase):
    """Test basic setup and environment"""
    
    def test_virtual_environment_exists(self):
        """Test that virtual environment is properly set up"""
        venv_path = os.path.join(os.path.dirname(__file__), '..', 'venv')
        self.assertTrue(os.path.exists(venv_path), "Virtual environment directory not found")
        
        # Check for Python executable
        python_exe = os.path.join(venv_path, 'bin', 'python')
        if not os.path.exists(python_exe):
            python_exe = os.path.join(venv_path, 'Scripts', 'python.exe')  # Windows
        
        self.assertTrue(os.path.exists(python_exe), "Python executable not found in venv")
    
    def test_env_file_exists(self):
        """Test that environment configuration file exists"""
        env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
        self.assertTrue(os.path.exists(env_file), ".env file not found")
        
        # Check content
        with open(env_file, 'r') as f:
            content = f.read()
            self.assertIn('REPLICATE_API_TOKEN', content)
    
    def test_demo_files_exist(self):
        """Test that demo files are present"""
        demo_dir = os.path.join(os.path.dirname(__file__), '..', 'replicate_apps')
        self.assertTrue(os.path.exists(demo_dir), "replicate_apps directory not found")
        
        simple_demo = os.path.join(demo_dir, 'simple_demo.py')
        self.assertTrue(os.path.exists(simple_demo), "simple_demo.py not found")
        
        ai_helper = os.path.join(demo_dir, 'quantum_ai_helper.py')
        self.assertTrue(os.path.exists(ai_helper), "quantum_ai_helper.py not found")
    
    def test_requirements_file_exists(self):
        """Test that requirements file exists and has expected packages"""
        req_file = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
        self.assertTrue(os.path.exists(req_file), "requirements.txt not found")
        
        with open(req_file, 'r') as f:
            content = f.read()
            self.assertIn('replicate', content)
            self.assertIn('python-dotenv', content)
    
    def test_documentation_exists(self):
        """Test that documentation files exist"""
        docs = [
            'QUICK_START.md',
            'REPLICATE_INTEGRATION.md'
        ]
        
        for doc in docs:
            doc_path = os.path.join(os.path.dirname(__file__), '..', doc)
            self.assertTrue(os.path.exists(doc_path), f"{doc} not found")


class TestImportsInVenv(unittest.TestCase):
    """Test imports in virtual environment"""
    
    def setUp(self):
        """Set up test environment"""
        self.venv_python = self._get_venv_python()
    
    def _get_venv_python(self):
        """Get path to virtual environment Python"""
        venv_path = os.path.join(os.path.dirname(__file__), '..', 'venv')
        python_exe = os.path.join(venv_path, 'bin', 'python')
        if not os.path.exists(python_exe):
            python_exe = os.path.join(venv_path, 'Scripts', 'python.exe')  # Windows
        return python_exe
    
    def test_replicate_import(self):
        """Test that replicate can be imported in venv"""
        result = subprocess.run([
            self.venv_python, '-c', 'import replicate; print("OK")'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0, f"Replicate import failed: {result.stderr}")
        self.assertIn("OK", result.stdout)
    
    def test_numpy_import(self):
        """Test that numpy can be imported in venv"""
        result = subprocess.run([
            self.venv_python, '-c', 'import numpy; print("OK")'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0, f"NumPy import failed: {result.stderr}")
        self.assertIn("OK", result.stdout)
    
    def test_matplotlib_import(self):
        """Test that matplotlib can be imported in venv"""
        result = subprocess.run([
            self.venv_python, '-c', 'import matplotlib; print("OK")'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0, f"Matplotlib import failed: {result.stderr}")
        self.assertIn("OK", result.stdout)
    
    def test_dotenv_import(self):
        """Test that python-dotenv can be imported in venv"""
        result = subprocess.run([
            self.venv_python, '-c', 'from dotenv import load_dotenv; print("OK")'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0, f"python-dotenv import failed: {result.stderr}")
        self.assertIn("OK", result.stdout)


class TestDemoExecution(unittest.TestCase):
    """Test demo script execution"""
    
    def setUp(self):
        """Set up test environment"""
        self.venv_python = self._get_venv_python()
        self.demo_path = os.path.join(os.path.dirname(__file__), '..', 'replicate_apps', 'simple_demo.py')
    
    def _get_venv_python(self):
        """Get path to virtual environment Python"""
        venv_path = os.path.join(os.path.dirname(__file__), '..', 'venv')
        python_exe = os.path.join(venv_path, 'bin', 'python')
        if not os.path.exists(python_exe):
            python_exe = os.path.join(venv_path, 'Scripts', 'python.exe')  # Windows
        return python_exe
    
    def test_simple_demo_runs(self):
        """Test that simple demo runs without errors"""
        env = os.environ.copy()
        env['REPLICATE_API_TOKEN'] = 'test_token_for_demo'
        
        result = subprocess.run([
            self.venv_python, self.demo_path
        ], capture_output=True, text=True, env=env, timeout=60)
        
        self.assertEqual(result.returncode, 0, f"Demo failed: {result.stderr}")
        self.assertIn("Replicate AI Demo", result.stdout)
        self.assertIn("Demo completed", result.stdout)


if __name__ == '__main__':
    # Run tests and save results
    test_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(test_dir, '..', 'test_results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Run tests with detailed output
    with open(os.path.join(results_dir, 'simple_test_report.txt'), 'w') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(sys.modules[__name__])
        result = runner.run(suite)
        
        # Print summary to console
        print(f"\n{'='*50}")
        print("🧪 SIMPLE TESTS SUMMARY")
        print(f"{'='*50}")
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        
        if result.failures or result.errors:
            print("\n❌ Some tests failed")
            for test, error in result.failures + result.errors:
                print(f"  - {test}: {error.split('AssertionError:')[-1].strip()}")
        else:
            print("\n✅ ALL SIMPLE TESTS PASSED!")
        
        print(f"{'='*50}")
        print("📁 Results saved to: test_results/simple_test_report.txt")