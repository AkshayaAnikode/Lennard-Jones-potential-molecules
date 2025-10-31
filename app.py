# app.py                                 

import io                                 # For in-memory text buffer to build a CSV
import numpy as np                        # Numerical arrays and math
import matplotlib.pyplot as plt           # Plotting library used inside Streamlit
import streamlit as st                    # Streamlit UI framework

st.set_page_config(page_title="Lennard–Jones Visualizer", layout="wide")
# Sets the browser tab title and makes the page use a wide layout

st.title("Lennard–Jones (LJ) Potential — Interactive")
# Header at top of the page

st.caption("Type a distance r to see potential energy and a two-sphere schematic. Units: eV and nm.")
#descriptive subtitle

# --- Inputs ---
with st.sidebar:                          # Everything inside this block shows in the left sidebar
    st.header("Parameters")               # Sidebar section title
    st.write("Defaults approximate Neon.")# Small note to the user
    epsilon = st.number_input("ε (eV)", min_value=0.0001, value=0.0103, step=0.0001, format="%.4f")
    # Numeric input for epsilon (well depth/attraction strength)

    sigma   = st.number_input("σ (nm)", min_value=0.01,   value=0.2740, step=0.0010, format="%.3f")
    # Numeric input for sigma (size of molecule/distance where PE is 0)

    r_value = st.number_input("Distance r (nm)", min_value=0.001, value=0.350, step=0.001, format="%.3f")
    # Numeric input for distance r: distance between center of two molecules 

# --- LJ function ---
def lj_U(r, eps, sig): #code defines function to compute PE
    r = np.asarray(r)                   
    return 4 * eps * ((sig / r)**12 - (sig / r)**6) #r^12 is repulsive force when molecules is too close & r^6 attractive vanderwal forces at longer distances
    # Lennard–Jones potential U(r) = 4ε[(σ/r)^12 − (σ/r)^6] #U = PE

# Derived reference points
r_min = 2**(1/6) * sigma                  # Distance at which U(r) is minimum: r_min = 2^(1/6)σ / attractive and repuslive forces balanced - stable point
U_min = -epsilon                          # Minimum potential value / energy at r min
U_r   = lj_U(r_value, epsilon, sigma)     # Potential at the user-entered distance r_value

# --- Curves domain (avoid r=0) ---
r_lo = max(0.3 * sigma, 0.01)             # Left PE graph  
r_hi = 4.0 * sigma                        # Right physical schematic spaced by r
r = np.linspace(r_lo, r_hi, 1000)         # 1000 evenly spaced r values between r_lo and r_hi
U = lj_U(r, epsilon, sigma)               # Compute U(r) on the whole grid for plotting

# --- Layout ---
left, right = st.columns(2, gap="large")  # Two side-by-side columns for plots

# --- Left: Potential plot ---
with left:
    fig1, ax1 = plt.subplots(figsize=(6, 4))    # Create a Matplotlib figure and axes
    ax1.plot(r, U, label="LJ potential U(r)")   # Plot the LJ curve
    ax1.axhline(0, linewidth=1)                 # Horizontal line at U = 0 for reference
    ax1.plot([r_value], [U_r], "o")             # Mark the current (r, U(r)) point
    ax1.annotate(f"r = {r_value:.3f} nm\nU = {U_r:.4f} eV",
                 xy=(r_value, U_r), xytext=(10, 10),
                 textcoords="offset points", fontsize=9)
    # Label the current point with its numeric values

    ax1.axvline(sigma, linestyle="--", linewidth=1)        # Vertical line at σ
    ax1.text(sigma, ax1.get_ylim()[1]*0.85, "σ", ha="center", va="top", fontsize=9)
    # Text annotation for σ near the top of the plot

    ax1.axvline(r_min, linestyle="--", linewidth=1)        # Vertical line at r_min
    ax1.text(r_min, ax1.get_ylim()[1]*0.70, "r_min = 2^(1/6)σ", ha="center", va="top", fontsize=9)
    # Label for r_min

    ax1.plot([r_min], [U_min], "s")                        # Square marker at the well minimum
    ax1.annotate(f"well depth = −ε\n(= {U_min:.4f} eV)",
                 xy=(r_min, U_min), xytext=(10, -30),
                 textcoords="offset points", fontsize=9)
    # Annotation explaining the well depth

    ax1.set_xlabel("Distance r (nm)")                      # X-axis label
    ax1.set_ylabel("Potential energy U(r) (eV)")           # Y-axis label
    ax1.set_title("Lennard–Jones Potential")               # Plot title
    ax1.legend(loc="upper right", fontsize=9)              # Legend
    st.pyplot(fig1, clear_figure=True)                     # Render the Matplotlib figure in Streamlit

# --- Right: Two-sphere schematic (not to scale physically) ---
with right:
    radius = 0.18 * sigma                    # Visual radius for the circles (illustrative only)
    cx_left  = -0.5 * r_value                # X-coordinate for left sphere center
    cx_right =  0.5 * r_value                # X-coordinate for right sphere center

    fig2, ax2 = plt.subplots(figsize=(6, 4)) # New figure for the schematic
    circle_left  = plt.Circle((cx_left, 0.0),  radius, fill=True, alpha=0.7)
    circle_right = plt.Circle((cx_right, 0.0), radius, fill=True, alpha=0.7)
    ax2.add_patch(circle_left)               # Draw left circle
    ax2.add_patch(circle_right)              # Draw right circle

    pad = max(1.2 * r_value, 1.2 * sigma)    # Padding for plot limits so circles fit
    ax2.set_xlim(-pad, pad)                   # X-limits centered around 0
    ax2.set_ylim(-pad * 0.4, pad * 0.4)       # Y-limits (smaller since we only need a strip)
    ax2.set_aspect("equal", adjustable="box") # Keep circles circular (equal aspect ratio)
    ax2.axis("off")                           # Hide axes for a cleaner schematic
    ax2.set_title(f"Two 'Molecules' schematic  (center distance r = {r_value:.3f} nm)")
    # Title showing the current separation

    ax2.plot([cx_left, cx_right], [0, 0], linestyle="--", linewidth=1)
    # Dashed line between centers to visualize the distance r

    ax2.text(0, 0.02 * pad, f"r = {r_value:.3f} nm", ha="center", va="bottom", fontsize=10)
    # Text label for r near the dashed line

    st.pyplot(fig2, clear_figure=True)       # Render the schematic figure in Streamlit

# --- Numeric readout and quick notes ---
st.subheader("Values")                       # Small header above the metrics
c1, c2, c3 = st.columns(3)                   # Three metric columns
c1.metric("σ (nm)", f"{sigma:.3f}")          # Show σ nicely formatted
c2.metric("r_min (nm)", f"{r_min:.3f}")      # Show r_min
c3.metric("U(r) at input (eV)", f"{U_r:.4f}")# Show current U(r)

st.info(
    "Notes:\n"
    "- For r < σ, the repulsive term ∝ (σ/r)^12 dominates (Pauli repulsion).\n"
    "- The potential well minimum occurs at r_min = 2^(1/6)·σ with depth −ε.\n"
    "- As r → ∞, U(r) → 0 from below (weak attraction vanishes)."
)
# Blue info box summarizing the physics

# Optional: download the potential curve as CSV for your report
csv = io.StringIO()                          # Create an in-memory text buffer
csv.write("r_nm,U_eV\n")                     # CSV header row
for rv, uv in zip(r, U):                     # Loop over all sampled points
    csv.write(f"{rv:.6f},{uv:.8f}\n")        # Write each r,U pair as a row
st.download_button("Download potential curve (CSV)", data=csv.getvalue(),
                   file_name="lj_potential.csv", mime="text/csv")
# Adds a button so users can download the sampled LJ curve as CSV

st.caption("Tip: change ε and σ to match other species; enter r to sample the curve without using a slider.")
# Small footer hint
