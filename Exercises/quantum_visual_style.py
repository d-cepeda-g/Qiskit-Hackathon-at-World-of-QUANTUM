"""
Enhanced Visual Styling for Qiskit Quantum Computing Exercises
============================================================

This module provides beautiful, modern styling for quantum computing visualizations
including Bloch sphere plots, circuit diagrams, histograms, and measurement results.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from qiskit.visualization import plot_bloch_multivector, plot_histogram, circuit_drawer
from qiskit.tools.visualization import _matplotlib
import warnings
warnings.filterwarnings('ignore')

# Modern color palettes for quantum visualizations
QUANTUM_COLORS = {
    'primary': '#1f77b4',      # Professional blue
    'secondary': '#ff7f0e',    # Warm orange
    'accent': '#2ca02c',       # Fresh green
    'highlight': '#d62728',    # Alert red
    'purple': '#9467bd',       # Quantum purple
    'pink': '#e377c2',         # Soft pink
    'brown': '#8c564b',        # Earthy brown
    'gray': '#7f7f7f',         # Neutral gray
    'olive': '#bcbd22',        # Natural olive
    'cyan': '#17becf'          # Electric cyan
}

BLOCH_COLORS = {
    'sphere': '#e6f3ff',       # Light blue sphere
    'grid': '#cccccc',         # Light gray grid
    'axis': '#666666',         # Dark gray axes
    'vector': '#ff4444',       # Bright red vector
    'background': '#ffffff'    # Clean white background
}

def setup_quantum_style():
    """Set up the global matplotlib style for quantum visualizations."""
    
    # Set the style parameters
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Custom parameters for modern look
    params = {
        'figure.figsize': (10, 8),
        'figure.dpi': 100,
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'axes.edgecolor': '#cccccc',
        'axes.linewidth': 1.2,
        'axes.grid': True,
        'axes.axisbelow': True,
        'axes.labelsize': 12,
        'axes.titlesize': 16,
        'axes.titleweight': 'bold',
        'axes.titlepad': 20,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 11,
        'legend.frameon': True,
        'legend.shadow': True,
        'legend.framealpha': 0.9,
        'grid.color': '#e0e0e0',
        'grid.linestyle': '-',
        'grid.linewidth': 0.8,
        'grid.alpha': 0.7,
        'font.size': 11,
        'font.family': ['DejaVu Sans', 'Arial', 'sans-serif'],
        'text.color': '#333333',
        'lines.linewidth': 2.5,
        'lines.markersize': 8,
        'patch.linewidth': 0.5,
        'patch.facecolor': QUANTUM_COLORS['primary'],
        'patch.edgecolor': '#ffffff',
    }
    
    plt.rcParams.update(params)

def styled_bloch_sphere(state, title="Quantum State on Bloch Sphere", figsize=(8, 8)):
    """
    Create a beautifully styled Bloch sphere visualization.
    
    Args:
        state: Quantum state vector
        title: Title for the plot
        figsize: Figure size tuple
    
    Returns:
        matplotlib figure object
    """
    setup_quantum_style()
    
    fig = plt.figure(figsize=figsize)
    fig.suptitle(title, fontsize=16, fontweight='bold', y=0.95)
    
    # Create the Bloch sphere plot with custom styling
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the Bloch sphere with enhanced visual style
    bloch_plot = plot_bloch_multivector(state, title="", figsize=figsize)
    
    # Enhance the styling
    ax.set_facecolor(BLOCH_COLORS['background'])
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def styled_histogram(counts, title="Measurement Results", figsize=(10, 6)):
    """
    Create a beautifully styled histogram for measurement results.
    
    Args:
        counts: Dictionary of measurement counts
        title: Title for the plot
        figsize: Figure size tuple
    
    Returns:
        matplotlib figure object
    """
    setup_quantum_style()
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Prepare data
    labels = list(counts.keys())
    values = list(counts.values())
    total_shots = sum(values)
    probabilities = [v/total_shots for v in values]
    
    # Create gradient colors
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(labels)))
    
    # Create the bar plot with enhanced styling
    bars = ax.bar(labels, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    
    # Add value labels on top of bars
    for bar, prob in zip(bars, probabilities):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + total_shots*0.01,
                f'{height}\n({prob:.1%})', ha='center', va='bottom', 
                fontweight='bold', fontsize=11)
    
    # Styling
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Measurement Outcome', fontsize=12, fontweight='bold')
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_ylim(0, max(values) * 1.15)
    
    # Add grid for better readability
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_axisbelow(True)
    
    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    return fig

def styled_circuit_drawer(circuit, output='mpl', style=None, figsize=(12, 6)):
    """
    Create a beautifully styled quantum circuit diagram.
    
    Args:
        circuit: Qiskit QuantumCircuit object
        output: Output format ('mpl' for matplotlib)
        style: Custom style dictionary
        figsize: Figure size tuple
    
    Returns:
        matplotlib figure object or circuit diagram
    """
    if style is None:
        style = {
            'backgroundcolor': '#ffffff',
            'edgecolor': '#000000',
            'gatefacecolor': '#ffffff',
            'gatetextcolor': '#000000',
            'subtextcolor': '#666666',
            'linecolor': '#000000',
            'creglinecolor': '#778899',
            'gatefontsize': 12,
            'subfontsize': 10,
            'showindex': True,
            'compress': False,
            'figwidth': figsize[0],
            'dpi': 150,
        }
    
    return circuit_drawer(circuit, output=output, style=style)

def create_state_comparison_plot(states, labels, title="Quantum State Comparison"):
    """
    Create a comparison plot of multiple quantum states on Bloch spheres.
    
    Args:
        states: List of quantum state vectors
        labels: List of labels for each state
        title: Overall title for the plot
    
    Returns:
        matplotlib figure object
    """
    setup_quantum_style()
    
    n_states = len(states)
    cols = min(n_states, 3)
    rows = (n_states + cols - 1) // cols
    
    fig = plt.figure(figsize=(5*cols, 5*rows))
    fig.suptitle(title, fontsize=18, fontweight='bold', y=0.95)
    
    for i, (state, label) in enumerate(zip(states, labels)):
        ax = fig.add_subplot(rows, cols, i+1, projection='3d')
        plot_bloch_multivector(state, title=label, fig=fig)
    
    plt.tight_layout()
    return fig

def create_probability_distribution_plot(probabilities, labels, title="Probability Distribution"):
    """
    Create a beautiful probability distribution plot.
    
    Args:
        probabilities: List of probability values
        labels: List of state labels
        title: Plot title
    
    Returns:
        matplotlib figure object
    """
    setup_quantum_style()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create beautiful gradient colors
    colors = plt.cm.plasma(np.linspace(0.1, 0.9, len(probabilities)))
    
    # Create the plot
    bars = ax.bar(labels, probabilities, color=colors, alpha=0.8, 
                  edgecolor='white', linewidth=2)
    
    # Add percentage labels
    for bar, prob in zip(bars, probabilities):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{prob:.1%}', ha='center', va='bottom', 
                fontweight='bold', fontsize=11)
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Quantum State', fontsize=12, fontweight='bold')
    ax.set_ylabel('Probability', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1.1)
    
    # Format y-axis as percentages
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
    
    ax.grid(True, alpha=0.3, axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    return fig

def display_quantum_info_box(title, content, box_style='round'):
    """
    Display a beautifully formatted information box.
    
    Args:
        title: Box title
        content: Box content (list of strings)
        box_style: Box styling
    """
    from IPython.display import display, HTML
    
    html_content = f"""
    <div style="
        border: 2px solid {QUANTUM_COLORS['primary']};
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        background: linear-gradient(135deg, #f8f9ff 0%, #e6f3ff 100%);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <h3 style="
            color: {QUANTUM_COLORS['primary']};
            margin-top: 0;
            font-weight: bold;
            font-size: 18px;
        ">{title}</h3>
        <div style="
            color: #333;
            line-height: 1.6;
            font-size: 14px;
        ">
            {'<br>'.join(content) if isinstance(content, list) else content}
        </div>
    </div>
    """
    
    display(HTML(html_content))

# Initialize the quantum style when module is imported
setup_quantum_style()

print("🎨 Quantum Visual Style Module Loaded!")
print("✨ Enhanced styling for Bloch spheres, histograms, and circuits is now available!")
print("📊 Use styled_bloch_sphere(), styled_histogram(), and styled_circuit_drawer() for beautiful plots!")