# Quantum Computing Exercises with Qiskit

This repository contains a comprehensive set of quantum computing exercises designed to teach quantum programming using Qiskit. The exercises are organized into three progressive levels, each building upon the previous one.

## 🎯 Learning Objectives

By completing these exercises, you will learn:
- Fundamental quantum computing concepts and gates
- Major quantum algorithms and their implementations  
- Variational quantum algorithms for near-term applications
- Quantum machine learning techniques
- How to use Qiskit for quantum programming

## 📋 Prerequisites

### Software Requirements
- Python 3.8 or higher
- Virtual environment (recommended)

### Required Packages
```bash
pip install qiskit>=1.0.0
pip install qiskit-aer>=0.14.0
pip install matplotlib>=3.5.0
pip install numpy>=1.21.0
pip install scipy>=1.7.0
```

### Recommended Setup
```bash
# Create virtual environment
python -m venv quantum_env
source quantum_env/bin/activate  # Linux/Mac
# or
quantum_env\Scripts\activate     # Windows

# Install packages
pip install qiskit qiskit-aer matplotlib numpy scipy jupyter
```

### Knowledge Prerequisites
- Basic Python programming
- Elementary linear algebra
- Basic understanding of complex numbers
- Familiarity with quantum mechanics concepts (helpful but not required)

## 📚 Course Structure

### Part 1: Quantum Computing Basics (`quantum_exercises_01_basics.py`)

**Duration:** 2-3 hours  
**Difficulty:** Beginner

**Topics Covered:**
- Introduction to quantum circuits and qubits
- Basic quantum gates (X, H, CNOT)
- Quantum measurements and state visualization
- Creating superposition states
- Quantum entanglement and Bell states

**Key Exercises:**
1. **Your First Quantum Circuit** - Create and measure a simple qubit
2. **The X Gate** - Learn the quantum NOT operation
3. **Superposition with Hadamard** - Create probabilistic quantum states
4. **Two-Qubit Circuits** - Explore multi-qubit operations
5. **Bell States** - Create entangled quantum states
6. **State Visualization** - Understand quantum states mathematically

**Learning Outcomes:**
- Understand qubit representation and manipulation
- Master basic quantum gates and their effects
- Comprehend superposition and entanglement
- Gain proficiency with Qiskit basics

### Part 2: Quantum Algorithms (`quantum_exercises_02_algorithms.py`)

**Duration:** 3-4 hours  
**Difficulty:** Intermediate

**Topics Covered:**
- Oracle-based quantum algorithms
- Quantum search and optimization
- Quantum Fourier Transform
- Phase estimation techniques

**Key Exercises:**
1. **Deutsch-Jozsa Algorithm** - Exponential speedup for function classification
2. **Grover's Search** - Quadratic speedup for database search
3. **Quantum Phase Estimation** - Essential subroutine for many algorithms
4. **Quantum Fourier Transform** - Fundamental quantum operation
5. **Bernstein-Vazirani Algorithm** - Hidden bit string discovery

**Learning Outcomes:**
- Understand quantum speedup and its sources
- Implement fundamental quantum algorithms
- Learn oracle construction and quantum parallelism
- Explore quantum interference effects

### Part 3: Variational Quantum Algorithms (`quantum_exercises_03_variational.py`)

**Duration:** 4-5 hours  
**Difficulty:** Advanced

**Topics Covered:**
- Hybrid quantum-classical algorithms
- Quantum machine learning
- Optimization on quantum computers
- Near-term quantum applications

**Key Exercises:**
1. **Variational Quantum Eigensolver (VQE)** - Find ground state energies
2. **Quantum Approximate Optimization (QAOA)** - Solve combinatorial problems
3. **Quantum Feature Maps** - Encode classical data into quantum states
4. **Variational Quantum Classifier** - Quantum machine learning for classification
5. **Quantum Neural Networks** - Function approximation with quantum circuits

**Learning Outcomes:**
- Master variational quantum algorithms
- Understand quantum machine learning principles
- Learn feature encoding strategies
- Explore near-term quantum applications

## 🚀 Getting Started

### Quick Start
1. **Clone or download** the exercise files
2. **Activate** your virtual environment with Qiskit installed
3. **Start with Part 1:**
   ```bash
   python quantum_exercises_01_basics.py
   ```

### Recommended Learning Path
1. **Read the introduction** in each file before starting
2. **Run exercises sequentially** - each builds on previous concepts
3. **Experiment with parameters** - modify code to deepen understanding
4. **Complete practice problems** - test your knowledge
5. **Move to next part** only after mastering current concepts

### Interactive Learning
For a more interactive experience, you can convert the Python files to Jupyter notebooks:
```bash
# Start Jupyter
jupyter notebook

# Or use JupyterLab
jupyter lab
```

## 💡 Usage Tips

### Understanding the Code Structure
Each exercise file follows this pattern:
- **Docstring explanation** of concepts and objectives
- **Helper functions** that implement quantum operations
- **Main exercise functions** with step-by-step implementations
- **Analysis sections** explaining results and insights

### Debugging and Troubleshooting
- **Check your Qiskit version:** `python -c "import qiskit; print(qiskit.__version__)"`
- **Verify simulator:** Most exercises use `AerSimulator()` for local simulation
- **Reduce shots** if simulations are slow (default is usually 1000)
- **Check circuit depth** for complex algorithms

### Customization Ideas
- **Modify parameters** in variational algorithms
- **Change problem sizes** (number of qubits, data points)
- **Implement different ansätze** for VQE and QAOA
- **Create your own oracles** for search problems
- **Experiment with different feature maps** for quantum ML

## 🔬 Extended Projects

After completing the main exercises, consider these projects:

### Beginner Projects
- Implement additional Bell states (Φ-, Ψ+, Ψ-)
- Create a quantum random number generator
- Build a quantum coin flip simulator
- Visualize quantum interference patterns

### Intermediate Projects
- Implement Simon's algorithm
- Create a quantum walk simulation
- Build a quantum error correction code
- Implement the quantum teleportation protocol

### Advanced Projects
- Extend VQE to larger molecular systems
- Implement Shor's factoring algorithm
- Create a variational quantum linear solver
- Build a quantum generative adversarial network

## 📖 Additional Resources

### Qiskit Documentation
- [Qiskit Textbook](https://qiskit.org/textbook/) - Comprehensive quantum computing guide
- [Qiskit Tutorials](https://qiskit.org/documentation/tutorials.html) - Official tutorials
- [Qiskit API Reference](https://qiskit.org/documentation/apidoc/qiskit.html) - Complete API documentation

### Quantum Computing Theory
- **Books:**
  - "Quantum Computation and Quantum Information" by Nielsen & Chuang
  - "Programming Quantum Computers" by Johnston, Harrigan & Gimeno-Segovia
  - "Quantum Computing: An Applied Approach" by Hidary

### Online Courses
- [IBM Qiskit Quantum Computing Course](https://qiskit.org/learn/)
- [Microsoft Quantum Development Kit](https://docs.microsoft.com/en-us/quantum/)
- [Google Cirq Documentation](https://quantumai.google/cirq)

### Research Papers
- Look for papers on arXiv.org in the "quant-ph" category
- Follow quantum computing research groups and conferences
- Explore applications in quantum chemistry, optimization, and machine learning

## 🤝 Contributing

If you find errors, have suggestions, or want to add exercises:
1. **Check existing issues** before creating new ones
2. **Provide clear descriptions** of problems or enhancements
3. **Include code examples** when suggesting improvements
4. **Test thoroughly** before submitting contributions

## 📄 License

These exercises are provided for educational purposes. Feel free to use, modify, and share them for learning quantum computing. If you use them in academic or commercial settings, please provide appropriate attribution.

## 🔧 Troubleshooting

### Common Issues

**ImportError: No module named 'qiskit'**
```bash
pip install qiskit qiskit-aer
```

**Slow Simulation**
- Reduce the number of shots: `simulator.run(circuit, shots=100)`
- Use smaller circuits for testing
- Consider using statevector simulator for noise-free simulations

**Circuit Too Deep**
- Some algorithms may create deep circuits that are slow to simulate
- Try reducing the number of layers or iterations
- Use `transpile()` to optimize circuits

**Memory Issues**
- Large quantum circuits can use significant memory
- Start with small examples (2-4 qubits)
- Close unnecessary applications when running simulations

### Getting Help
- **Qiskit Slack:** Join the Qiskit community for discussions
- **Stack Overflow:** Tag questions with "qiskit" and "quantum-computing"
- **GitHub Issues:** Check the Qiskit repository for known issues
- **Documentation:** Always refer to the latest Qiskit documentation

---

**Happy Quantum Programming! 🚀⚛️**

*Remember: Quantum computing is a rapidly evolving field. Stay curious, keep experimenting, and don't hesitate to explore beyond these exercises as you build your quantum programming skills.*




