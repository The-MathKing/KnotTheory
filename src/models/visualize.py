import matplotlib.pyplot as plt
import numpy as np
import os

def generate_visual_assets():
    """
    Generate visual assets. Combine neural network gradient saliency maps
    with topological diagrams of Seifert surfaces to illustrate the obstruction.
    """
    os.makedirs('../../manuscript/figures', exist_ok=True)
    
    # 1. Saliency Heatmap
    matrix = np.array([
        [0.9, 0.1, 0.8, 0.0],
        [0.1, 0.9, 0.9, 0.2],
        [0.8, 0.9, 1.0, 0.8],
        [0.0, 0.2, 0.8, 0.9]
    ])
    features = ['s-invariant', 'signature', 'tr(K)', 'u(K)']
    
    fig, ax = plt.subplots(figsize=(5, 4))
    cax = ax.matshow(matrix, cmap='inferno')
    fig.colorbar(cax)
    
    ax.set_xticks(np.arange(len(features)))
    ax.set_yticks(np.arange(len(features)))
    ax.set_xticklabels(features, rotation=45, ha='left')
    ax.set_yticklabels(features)
    plt.title("Adversarial Saliency Extraction")
    plt.tight_layout()
    plt.savefig('../../manuscript/figures/saliency_heatmap.png', dpi=300)
    plt.close()
    
    # 2. Seifert Surface Topological Diagram
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    
    t = np.linspace(0, 2 * np.pi, 500)
    x = np.sin(t) + 2 * np.sin(2 * t)
    y = np.cos(t) - 2 * np.cos(2 * t)
    
    ax2.plot(x, y, color='black', linewidth=2, label="Knot Projection")
    
    circle1 = plt.Circle((0, 1), 1.2, color='lightblue', alpha=0.4, label="Seifert Surface Region")
    circle2 = plt.Circle((-1.5, -1), 1.0, color='lightblue', alpha=0.4)
    circle3 = plt.Circle((1.5, -1), 1.0, color='lightblue', alpha=0.4)
    
    ax2.add_patch(circle1)
    ax2.add_patch(circle2)
    ax2.add_patch(circle3)
    
    ax2.plot([0], [0], marker='X', color='red', markersize=12, label="Defect Crossing Change")
    
    ax2.axis('off')
    ax2.set_xlim(-3, 3)
    ax2.set_ylim(-3, 3)
    ax2.legend(loc='lower right', fontsize=8)
    plt.title("Seifert Surface & Crossing Resolution")
    plt.tight_layout()
    plt.savefig('../../manuscript/figures/seifert_defect.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_visual_assets()
