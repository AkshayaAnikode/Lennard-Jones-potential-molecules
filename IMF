# app.py
import io
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Lennard–Jones Visualizer", layout="wide")

st.title("Lennard–Jones (LJ) Potential — Interactive (no slider)")
st.caption("Type a distance r to see potential energy and a two-sphere schematic. Units: eV and nm.")

# --- Inputs ---
with st.sidebar:
    st.header("Parameters")
    st.write("Defaults approximate Neon.")
    epsilon = st.number_input("ε (eV)", min_value=0.0001, value=0.0103, step=0.0001, format="%.4f")
    sigma   = st.number_input("σ (nm)", min_value=0.01,   value=0.2740, step=0.0010, format="%.3f")
    r_value = st.number_input("Distance r (nm)", min_value=0.001, value=0.350, step=0.001, format="%.3f")

# --- LJ function ---
def lj_U(r, eps, sig):
    r = np.asarray(r)
    return 4 * eps * ((sig / r)**12 - (sig / r)**6)

# Derived reference points
r_min = 2**(1/6) * sigma          # location of potential minimum
U_min = -epsilon                   # depth of the well
U_r   = lj_U(r_value, epsilon, sigma)

# --- Curves domain (avoid r=0) ---
r_lo = max(0.3 * sigma, 0.01)     # keep the left edge reasonable for visibility
r_hi = 4.0 * sigma
r = np.linspace(r_lo, r_hi, 1000)
U = lj_U(r, epsilon, sigma)

# --- Layout ---
left, right = st.columns(2, gap="large")

# --- Left: Potential plot ---
with left:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(r, U, label="LJ potential U(r)")
    ax1.axhline(0, linewidth=1)
    # annotate current r
    ax1.plot([r_value], [U_r], "o")
    ax1.annotate(f"r = {r_value:.3f} nm\nU = {U_r:.4f} eV",
                 xy=(r_value, U_r), xytext=(10, 10),
                 textcoords="offset points", fontsize=9)

    # mark σ and r_min
    ax1.axvline(sigma, linestyle="--", linewidth=1)
    ax1.text(sigma, ax1.get_ylim()[1]*0.85, "σ", ha="center", va="top", fontsize=9)
    ax1.axvline(r_min, linestyle="--", linewidth=1)
    ax1.text(r_min, ax1.get_ylim()[1]*0.70, "r_min = 2^(1/6)σ", ha="center", va="top", fontsize=9)

    # mark well depth at r_min
    ax1.plot([r_min], [U_min], "s")
    ax1.annotate(f"well depth = −ε\n(= {U_min:.4f} eV)",
                 xy=(r_min, U_min), xytext=(10, -30),
                 textcoords="offset points", fontsize=9)

    ax1.set_xlabel("Distance r (nm)")
    ax1.set_ylabel("Potential energy U(r) (eV)")
    ax1.set_title("Lennard–Jones Potential")
    ax1.legend(loc="upper right", fontsize=9)
    st.pyplot(fig1, clear_figure=True)

# --- Right: Two-sphere schematic (not to scale physically) ---
with right:
    # choose sphere radius for drawing (purely illustrative)
    radius = 0.18 * sigma
    # place spheres along x so center-to-center distance is r_value
    cx_left  = -0.5 * r_value
    cx_right =  0.5 * r_value

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    # draw spheres as circles
    circle_left  = plt.Circle((cx_left, 0.0),  radius, fill=True, alpha=0.7)
    circle_right = plt.Circle((cx_right, 0.0), radius, fill=True, alpha=0.7)
    ax2.add_patch(circle_left)
    ax2.add_patch(circle_right)

    # axis cosmetics
    pad = max(1.2 * r_value, 1.2 * sigma)
    ax2.set_xlim(-pad, pad)
    ax2.set_ylim(-pad * 0.4, pad * 0.4)
    ax2.set_aspect("equal", adjustable="box")
    ax2.axis("off")
    ax2.set_title(f"Two 'Molecules' schematic  (center distance r = {r_value:.3f} nm)")

    # dashed line showing center-to-center distance
    ax2.plot([cx_left, cx_right], [0, 0], linestyle="--", linewidth=1)
    ax2.text(0, 0.02 * pad, f"r = {r_value:.3f} nm", ha="center", va="bottom", fontsize=10)
    st.pyplot(fig2, clear_figure=True)

# --- Numeric readout and quick notes ---
st.subheader("Values")
c1, c2, c3 = st.columns(3)
c1.metric("σ (nm)", f"{sigma:.3f}")
c2.metric("r_min (nm)", f"{r_min:.3f}")
c3.metric("U(r) at input (eV)", f"{U_r:.4f}")

st.info(
    "Notes:\n"
    "- For r < σ, the repulsive term ∝ (σ/r)^12 dominates (Pauli repulsion).\n"
    "- The potential well minimum occurs at r_min = 2^(1/6)·σ with depth −ε.\n"
    "- As r → ∞, U(r) → 0 from below (weak attraction vanishes)."
)

# Optional: download the potential curve as CSV for your report
csv = io.StringIO()
csv.write("r_nm,U_eV\n")
for rv, uv in zip(r, U):
    csv.write(f"{rv:.6f},{uv:.8f}\n")
st.download_button("Download potential curve (CSV)", data=csv.getvalue(),
                   file_name="lj_potential.csv", mime="text/csv")

st.caption("Tip: change ε and σ to match other species; enter r to sample the curve without using a slider.")
