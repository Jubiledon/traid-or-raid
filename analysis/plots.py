# analysis/plots.py
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from statistics import mean, stdev

# ── data ──────────────────────────────────────────────────────────────────────

simple = [1.0,0.967,1.0,1.0,0.967,1.0,0.967,0.933,0.967,1.0,1.0,0.967,
          1.0,0.9,1.0,1.0,0.933,1.0,1.0,1.0,1.0,0.9,0.967,1.0,0.867,
          1.0,1.0,0.967,0.967,1.0]

llm_silent = [0.633,0.4,0.3,0.467,0.133,0.367,0.233,0.233,0.567,0.4,
              0.233,0.133,0.733,0.233,0.1,0.633,0.5,0.233,0.5,0.533,
              0.667,0.767,0.4,0.467,0.2,0.3,0.367,0.4,0.267,0.5]

llm_comms = [0.533,0.467,0.033,0.433,0.1,0.3,0.233,0.2,0.533,0.233,
             0.2,0.067,0.4,0.333,0.067,0.167,0.367,0.367,0.467,0.433]

import os
os.makedirs("figures", exist_ok=True)

# ── Figure 1: Box plot ────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(8, 5))
data = [simple, llm_silent, llm_comms]
labels = ["Simple", "LLM Silent", "LLM Comms"]
colors = ["#4CAF50", "#2196F3", "#FF9800"]

bp = ax.boxplot(data, labels=labels, patch_artist=True, notch=False)
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_ylabel("Collective Efficiency")
ax.set_title("Collective Efficiency by Agent Condition (30/30/20 trials)")
ax.set_ylim(0, 1.1)
ax.axhline(y=mean(simple), color="#4CAF50", linestyle="--", alpha=0.4)
ax.axhline(y=mean(llm_silent), color="#2196F3", linestyle="--", alpha=0.4)
ax.axhline(y=mean(llm_comms), color="#FF9800", linestyle="--", alpha=0.4)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("figures/fig1_boxplot.png", dpi=150)
print("Saved fig1_boxplot.png")
plt.close()

# ── Figure 2: Bar chart with error bars ───────────────────────────────────────

fig, ax = plt.subplots(figsize=(7, 5))
conditions = ["Simple", "LLM Silent", "LLM Comms"]
means = [mean(simple), mean(llm_silent), mean(llm_comms)]
stds = [stdev(simple), stdev(llm_silent), stdev(llm_comms)]
colors = ["#4CAF50", "#2196F3", "#FF9800"]

bars = ax.bar(conditions, means, color=colors, alpha=0.8,
              yerr=stds, capsize=6, edgecolor="white")
ax.set_ylabel("Mean Collective Efficiency")
ax.set_title("Mean Collective Efficiency ± Std Dev by Condition")
ax.set_ylim(0, 1.1)

for bar, m, s in zip(bars, means, stds):
    ax.text(bar.get_x() + bar.get_width()/2, m + s + 0.02,
            f"{m:.3f}", ha="center", va="bottom", fontsize=10, fontweight="bold")

ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("figures/fig2_barchart.png", dpi=150)
print("Saved fig2_barchart.png")
plt.close()

# ── Figure 3: Trial-by-trial line plot ────────────────────────────────────────

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(1, 31), simple, color="#4CAF50", alpha=0.8,
        linewidth=1.5, label="Simple", marker="o", markersize=3)
ax.plot(range(1, 31), llm_silent, color="#2196F3", alpha=0.8,
        linewidth=1.5, label="LLM Silent", marker="s", markersize=3)
ax.plot(range(1, len(llm_comms)+1), llm_comms, color="#FF9800", alpha=0.8,
        linewidth=1.5, label="LLM Comms", marker="^", markersize=3)
ax.axhline(y=mean(simple), color="#4CAF50", linestyle="--", alpha=0.3)
ax.axhline(y=mean(llm_silent), color="#2196F3", linestyle="--", alpha=0.3)
ax.axhline(y=mean(llm_comms), color="#FF9800", linestyle="--", alpha=0.3)
ax.set_xlabel("Trial Number")
ax.set_ylabel("Collective Efficiency")
ax.set_title("Collective Efficiency Per Trial by Condition")
ax.legend()
ax.set_ylim(0, 1.1)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("figures/fig3_lineplot.png", dpi=150)
print("Saved fig3_lineplot.png")
plt.close()

# ── Figure 4: Inequality (score spread within episodes) ───────────────────────

# raw per-agent scores from your CSVs
simple_scores_raw = [
    [7,5,12,6],[9,4,9,7],[7,8,9,6],[6,8,9,7],[10,9,4,6],[8,7,10,5],
    [7,7,6,9],[12,6,5,5],[9,5,6,9],[2,10,6,12],[8,1,11,10],[9,4,9,7],
    [11,8,6,5],[6,9,8,4],[11,5,5,9],[6,8,6,10],[6,6,10,6],[7,7,7,9],
    [4,8,7,11],[12,5,7,6],[8,8,8,6],[6,8,5,8],[5,12,7,5],[4,4,11,11],
    [8,6,6,6],[9,7,7,7],[6,7,10,7],[13,6,4,6],[7,7,8,7],[11,3,9,7]
]
llm_silent_scores_raw = [
    [3,4,9,3],[0,4,3,5],[1,0,6,2],[3,3,3,5],[1,0,1,2],[2,4,2,3],
    [0,2,3,2],[1,0,4,2],[4,2,8,3],[0,5,4,3],[0,0,3,4],[1,1,1,1],
    [7,0,7,8],[2,1,2,2],[2,0,0,1],[1,0,11,7],[5,9,0,1],[0,3,3,1],
    [1,8,4,2],[0,6,6,4],[5,0,8,7],[3,14,0,6],[4,0,4,4],[1,7,2,4],
    [2,2,2,0],[3,2,2,2],[2,5,2,2],[2,0,9,1],[0,6,0,2],[4,8,1,2]
]
llm_comms_scores_raw = [
    [0,10,1,5],[3,3,4,4],[0,1,0,0],[3,5,3,2],[1,0,1,1],[4,0,3,2],
    [1,0,0,4],[0,2,4,0],[9,5,2,0],[1,2,1,3],[0,0,0,5],[0,0,1,1],
    [6,3,0,3],[1,3,3,3],[1,0,0,1],[0,0,1,4],[7,4,0,0],[4,5,0,2],
    [2,0,0,12],[0,9,2,2]
]

def gini(scores):
    s = sorted(scores)
    n = len(s)
    if sum(s) == 0:
        return 0
    cumsum = sum((i+1)*v for i, v in enumerate(s))
    return (2*cumsum) / (n * sum(s)) - (n+1)/n

simple_gini = [gini(s) for s in simple_scores_raw]
silent_gini = [gini(s) for s in llm_silent_scores_raw]
comms_gini  = [gini(s) for s in llm_comms_scores_raw]

fig, ax = plt.subplots(figsize=(8, 5))
gini_data = [simple_gini, silent_gini, comms_gini]
gini_labels = ["Simple", "LLM Silent", "LLM Comms"]
colors = ["#4CAF50", "#2196F3", "#FF9800"]
bp2 = ax.boxplot(gini_data, labels=gini_labels, patch_artist=True)
for patch, color in zip(bp2["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_ylabel("Gini Coefficient (0=equal, 1=unequal)")
ax.set_title("Inequality of Resource Distribution Within Episodes")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("figures/fig4_gini.png", dpi=150)
print("Saved fig4_gini.png")
plt.close()

# ── Stats summary table ───────────────────────────────────────────────────────

print("\n── Summary Statistics ──")
for name, d in [("Simple", simple), ("LLM Silent", llm_silent), ("LLM Comms", llm_comms)]:
    print(f"{name:12s} | mean={mean(d):.3f} | std={stdev(d):.3f} | "
          f"min={min(d):.3f} | max={max(d):.3f} | n={len(d)}")