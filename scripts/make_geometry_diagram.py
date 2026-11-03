"""
Generates a clean, professional, high-resolution vector-quality diagram
for the 'RADAR DESK GEOMETRY' to replace the text box on Slide 6.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generate_geometry_diagram():
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    fig.patch.set_facecolor('#0f172a')  # Slate 900
    ax.set_facecolor('#0f172a')

    # Remove all standard axes
    ax.set_xlim(-0.2, 8.2)
    ax.set_ylim(-0.5, 7.5)
    ax.axis('off')

    # Title Banner
    ax.text(4.0, 7.1, "RADAR DESK GEOMETRY & PLACEMENT", 
            ha='center', va='center', color='#38bdf8', 
            fontsize=17, fontweight='bold', fontfamily='sans-serif')
    ax.text(4.0, 6.7, "First Fresnel Zone (FFZ) Reflection Architecture", 
            ha='center', va='center', color='#94a3b8', 
            fontsize=11, fontfamily='sans-serif')

    # 1. First Fresnel Zone (Dotted Ellipse)
    ellipse = patches.Ellipse((4.0, 4.3), width=5.6, height=3.0, 
                              angle=0, fill=True, facecolor='#1e293b', 
                              edgecolor='#0284c7', linestyle='--', linewidth=2, alpha=0.55)
    ax.add_patch(ellipse)
    ax.text(4.0, 5.5, "First Fresnel Zone Boundary (r₁ ≈ 17.4 cm)", 
            ha='center', va='center', color='#0284c7', fontsize=9, fontweight='bold', style='italic')

    # 2. NodeMCU TX Box (Left)
    tx_box = patches.FancyBboxPatch((0.5, 3.7), 2.0, 1.2, 
                                   boxstyle="round,pad=0.1,rounding_size=0.15",
                                   facecolor='#1e293b', edgecolor='#38bdf8', linewidth=2.5)
    ax.add_patch(tx_box)
    ax.text(1.5, 4.5, "NodeMCU (TX)", ha='center', va='center', color='#ffffff', fontsize=12, fontweight='bold')
    ax.text(1.5, 4.15, "ESP8266 +20.5 dBm", ha='center', va='center', color='#38bdf8', fontsize=9.5)
    ax.text(1.5, 3.85, "(USB Power Bank)", ha='center', va='center', color='#94a3b8', fontsize=8.5)

    # Antenna on TX
    ax.plot([2.5, 2.7], [4.3, 4.3], color='#38bdf8', linewidth=3)
    ax.scatter([2.7], [4.3], color='#38bdf8', s=80, zorder=5)

    # TX WiFi Wave Arcs
    for rad, a in zip([0.3, 0.55, 0.8], [0.8, 0.5, 0.3]):
        arc = patches.Arc((2.7, 4.3), rad*2, rad*2, angle=0, theta1=-45, theta2=45, 
                          color='#38bdf8', linewidth=2, alpha=a)
        ax.add_patch(arc)

    # 3. ESP32 RX Box (Right)
    rx_box = patches.FancyBboxPatch((5.5, 3.7), 2.0, 1.2, 
                                   boxstyle="round,pad=0.1,rounding_size=0.15",
                                   facecolor='#1e293b', edgecolor='#10b981', linewidth=2.5)
    ax.add_patch(rx_box)
    ax.text(6.5, 4.5, "ESP32 (RX)", ha='center', va='center', color='#ffffff', fontsize=12, fontweight='bold')
    ax.text(6.5, 4.15, "CSI Demodulator", ha='center', va='center', color='#10b981', fontsize=9.5)
    ax.text(6.5, 3.85, "(Laptop USB COM9)", ha='center', va='center', color='#94a3b8', fontsize=8.5)

    # Antenna on RX
    ax.plot([5.5, 5.3], [4.3, 4.3], color='#10b981', linewidth=3)
    ax.scatter([5.3], [4.3], color='#10b981', s=80, zorder=5)

    # Line of Sight (LOS) Baseline Arrow
    ax.annotate('', xy=(5.2, 4.3), xytext=(2.8, 4.3),
                arrowprops=dict(arrowstyle='<->', color='#64748b', linewidth=2))
    ax.text(4.0, 4.55, "Line-of-Sight Distance (0.8 m to 1.0 m)", 
            ha='center', va='center', color='#cbd5e1', fontsize=10, fontweight='bold')

    # 4. Human Subject (Seated in Center Bottom)
    subject_bg = patches.FancyBboxPatch((2.6, 0.4), 2.8, 2.3,
                                       boxstyle="round,pad=0.1,rounding_size=0.2",
                                       facecolor='#1e293b', edgecolor='#e11d48', linewidth=2.5)
    ax.add_patch(subject_bg)

    # Head & Chest Silhouette representation
    head = patches.Circle((4.0, 2.15), 0.35, facecolor='#f43f5e', edgecolor='#ffffff', linewidth=1.5)
    ax.add_patch(head)
    
    chest = patches.FancyBboxPatch((3.55, 1.2), 0.9, 0.7,
                                  boxstyle="round,pad=0.08,rounding_size=0.1",
                                  facecolor='#be123c', edgecolor='#ffffff', linewidth=1.5)
    ax.add_patch(chest)

    # Heart pulse icon on chest
    ax.text(4.0, 1.55, "♥", ha='center', va='center', color='#ffffff', fontsize=16, fontweight='bold')

    ax.text(4.0, 0.88, "SUBJECT SEATED", ha='center', va='center', color='#ffffff', fontsize=11, fontweight='bold')
    ax.text(4.0, 0.60, "Thoracic Wall: 0.2 mm Pulse", ha='center', va='center', color='#f43f5e', fontsize=9.5, fontweight='bold')

    # Perpendicular Distance Arrow
    ax.annotate('', xy=(4.0, 4.2), xytext=(4.0, 2.65),
                arrowprops=dict(arrowstyle='<->', color='#e11d48', linewidth=2.5, linestyle='--'))
    ax.text(4.65, 3.4, "30 to 50 cm\nPerpendicular", 
            ha='left', va='center', color='#fecdd3', fontsize=10, fontweight='bold')

    # 5. Ray Paths (Forward wave and Reflected wave)
    # Forward wave: TX -> Chest
    ax.annotate('', xy=(3.5, 1.8), xytext=(2.7, 4.1),
                arrowprops=dict(arrowstyle='->', color='#38bdf8', linewidth=2.5, linestyle='-'))
    ax.text(2.6, 2.8, "Incident Wave\n(2.4 GHz)", 
            ha='right', va='center', color='#38bdf8', fontsize=9, fontweight='bold')

    # Reflected wave: Chest -> RX
    ax.annotate('', xy=(5.3, 4.1), xytext=(4.5, 1.8),
                arrowprops=dict(arrowstyle='->', color='#10b981', linewidth=2.5, linestyle='-'))
    ax.text(5.4, 2.8, "Reflected Wave\n(Phase Modulated)", 
            ha='left', va='center', color='#10b981', fontsize=9, fontweight='bold')

    # Bottom notes strip
    ax.text(4.0, 0.05, "✔ Hands resting on desk  |  ✔ Antennas at chest height (~1.0 m)  |  ✔ Natural breathing",
            ha='center', va='center', color='#94a3b8', fontsize=9.5, style='italic')

    plt.tight_layout()
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "radar_desk_geometry.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=300)
    plt.close()
    print(f"[SUCCESS] High-res radar geometry diagram saved to: {out_path}")

if __name__ == "__main__":
    generate_geometry_diagram()
