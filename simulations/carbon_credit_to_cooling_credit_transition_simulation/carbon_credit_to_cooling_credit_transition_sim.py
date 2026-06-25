"""
Carbon Credit to Cooling Credit Transition Simulation
======================================================
Conceptual counterfactual causal simulation.

Compares a Carbon Credit-centered climate finance pathway with
Cooling Credit pathways of equal and larger scale, examining effects on:
  - natural cooling-function recovery
  - heat-load accumulation
  - water-cycle and soil-moisture recovery
  - ocean heat moderation
  - potential moderation of El Nino-related heat-risk amplification
  - warming mitigation

This is an index-based, causal, conceptual model -- NOT a precise climate forecast.
All indexes are normalized 0-100. Values are illustrative proxies.

Scenarios
---------
A  Carbon Credit baseline  (primary finance: carbon accounting / offsets)
B  Equal-scale Cooling Credit transition (same total finance, redirected to cooling)
C  Larger-scale Cooling Credit transition (CC attracts ESG, insurance, adaptation finance)
D  Hybrid pathway  (Carbon Credit for emissions + Cooling Credit as second layer)

Author: Master / inchacomusho / InchaComisho
Repository: https://github.com/InchaComisho/Sustainable-Future-Cooling-Credit-Portal
"""

import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch

matplotlib.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
})

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Time axis ─────────────────────────────────────────────────────────────────
YEARS = np.arange(2015, 2036)
N = len(YEARS)

# ── Palette ───────────────────────────────────────────────────────────────────
COLOR = {
    "A": "#D62728",
    "B": "#2CA02C",
    "C": "#1F77B4",
    "D": "#FF7F0E",
}
LABEL = {
    "A": "A: Carbon Credit baseline",
    "B": "B: Equal-scale Cooling Credit",
    "C": "C: Larger-scale Cooling Credit",
    "D": "D: Hybrid (Carbon + Cooling Credit)",
}

# ══════════════════════════════════════════════════════════════════════════════
# Interpolation helpers
# ══════════════════════════════════════════════════════════════════════════════

def _lerp(start, end, n=N):
    return np.linspace(start, end, n)


def _curve(start, end, n=N, power=1.0):
    t = np.linspace(0, 1, n) ** power
    return start + (end - start) * t


def _logistic(start, end, n=N, steepness=4, midpoint=0.5):
    t = np.linspace(0, 1, n)
    sig = 1 / (1 + np.exp(-steepness * (t - midpoint)))
    sig = (sig - sig[0]) / (sig[-1] - sig[0])
    return start + (end - start) * sig


# ══════════════════════════════════════════════════════════════════════════════
# Scenario data
# ══════════════════════════════════════════════════════════════════════════════

def build_scenarios():

    # ── Scenario A: Carbon Credit baseline ───────────────────────────────────
    # Carbon finance grows, but goes almost entirely to carbon accounting.
    # Physical cooling investment stays weak.
    # Natural cooling functions continue to erode.
    A = {
        "carbon_credit_funding_index":              _curve(30, 68, power=0.85),
        "cooling_credit_funding_index":             _curve(3,  9,  power=1.0),
        "physical_cooling_investment_index":        _curve(10, 20, power=1.0),
        "natural_cooling_function_index":           _curve(72, 58, power=1.05),
        "water_cycle_recovery_index":               _curve(66, 52, power=1.05),
        "soil_moisture_recovery_index":             _curve(69, 54, power=1.1),
        "forest_evapotranspiration_recovery_index": _curve(71, 58, power=1.05),
        "urban_heat_reduction_index":               _curve(22, 36, power=0.9),
        "ocean_heat_moderation_index":              _curve(74, 59, power=1.1),
        "el_nino_heat_risk_moderation_index":       _curve(68, 52, power=1.1),
        "heat_load_index":                          _curve(40, 73, power=1.1),
        "warming_mitigation_index":                 _curve(22, 44, power=0.8),
    }

    # ── Scenario B: Equal-scale Cooling Credit transition ─────────────────────
    # Same total climate finance as A, but redirected to measurable physical cooling.
    # Carbon Credit is retained only at a smaller scale for emissions accounting.
    B = {
        "carbon_credit_funding_index":              _curve(30, 22, power=1.0),
        "cooling_credit_funding_index":             _logistic(5, 70, steepness=5, midpoint=0.4),
        "physical_cooling_investment_index":        _logistic(12, 76, steepness=5, midpoint=0.4),
        "natural_cooling_function_index":           _logistic(72, 84, steepness=4, midpoint=0.45),
        "water_cycle_recovery_index":               _logistic(66, 82, steepness=4, midpoint=0.45),
        "soil_moisture_recovery_index":             _logistic(69, 84, steepness=4, midpoint=0.45),
        "forest_evapotranspiration_recovery_index": _logistic(71, 85, steepness=4, midpoint=0.45),
        "urban_heat_reduction_index":               _logistic(22, 65, steepness=5, midpoint=0.4),
        "ocean_heat_moderation_index":              _logistic(74, 80, steepness=3, midpoint=0.5),
        "el_nino_heat_risk_moderation_index":       _logistic(68, 78, steepness=3, midpoint=0.5),
        "heat_load_index":                          _curve(40, 54, power=0.85),
        "warming_mitigation_index":                 _logistic(22, 62, steepness=4, midpoint=0.45),
    }

    # ── Scenario C: Larger-scale Cooling Credit ───────────────────────────────
    # Cooling Credit attracts additional ESG, insurance, adaptation, disaster-prevention
    # finance beyond what carbon credit would have raised.
    C = {
        "carbon_credit_funding_index":              _curve(30, 20, power=1.0),
        "cooling_credit_funding_index":             _logistic(5, 90, steepness=5, midpoint=0.38),
        "physical_cooling_investment_index":        _logistic(12, 90, steepness=5, midpoint=0.38),
        "natural_cooling_function_index":           _logistic(72, 91, steepness=4, midpoint=0.4),
        "water_cycle_recovery_index":               _logistic(66, 90, steepness=4, midpoint=0.4),
        "soil_moisture_recovery_index":             _logistic(69, 91, steepness=4, midpoint=0.4),
        "forest_evapotranspiration_recovery_index": _logistic(71, 92, steepness=4, midpoint=0.4),
        "urban_heat_reduction_index":               _logistic(22, 80, steepness=5, midpoint=0.38),
        "ocean_heat_moderation_index":              _logistic(74, 86, steepness=3, midpoint=0.45),
        "el_nino_heat_risk_moderation_index":       _logistic(68, 85, steepness=3, midpoint=0.45),
        "heat_load_index":                          _curve(40, 46, power=0.6),
        "warming_mitigation_index":                 _logistic(22, 76, steepness=4, midpoint=0.4),
    }

    # ── Scenario D: Hybrid pathway ────────────────────────────────────────────
    # Carbon Credit retained for emissions accounting.
    # Cooling Credit added as a second, complementary layer.
    D = {
        "carbon_credit_funding_index":              _curve(30, 58, power=0.9),
        "cooling_credit_funding_index":             _logistic(5, 58, steepness=5, midpoint=0.42),
        "physical_cooling_investment_index":        _logistic(12, 62, steepness=5, midpoint=0.42),
        "natural_cooling_function_index":           _logistic(72, 80, steepness=4, midpoint=0.48),
        "water_cycle_recovery_index":               _logistic(66, 78, steepness=4, midpoint=0.48),
        "soil_moisture_recovery_index":             _logistic(69, 80, steepness=4, midpoint=0.48),
        "forest_evapotranspiration_recovery_index": _logistic(71, 81, steepness=4, midpoint=0.48),
        "urban_heat_reduction_index":               _logistic(22, 60, steepness=5, midpoint=0.42),
        "ocean_heat_moderation_index":              _logistic(74, 78, steepness=3, midpoint=0.5),
        "el_nino_heat_risk_moderation_index":       _logistic(68, 76, steepness=3, midpoint=0.5),
        "heat_load_index":                          _curve(40, 58, power=0.8),
        "warming_mitigation_index":                 _logistic(22, 66, steepness=4, midpoint=0.45),
    }

    return {"A": A, "B": B, "C": C, "D": D}


SCENARIOS = build_scenarios()
ALL_INDEXES = list(SCENARIOS["A"].keys())

# ══════════════════════════════════════════════════════════════════════════════
# CSV export
# ══════════════════════════════════════════════════════════════════════════════

def export_csv():
    rows = []
    for sc_key, sc_data in SCENARIOS.items():
        for i, yr in enumerate(YEARS):
            row = {"year": int(yr), "scenario": sc_key}
            for col, arr in sc_data.items():
                row[col] = round(float(arr[i]), 2)
            rows.append(row)
    df = pd.DataFrame(rows)
    col_order = ["year", "scenario"] + ALL_INDEXES
    df = df[col_order]
    path = os.path.join(OUTPUT_DIR, "simulation_results.csv")
    df.to_csv(path, index=False)
    print(f"  OK {path}")


# ══════════════════════════════════════════════════════════════════════════════
# Shared helpers
# ══════════════════════════════════════════════════════════════════════════════

def _ax_base(ax, title, ylabel, ylim=(0, 100)):
    ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Year", fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_xlim(YEARS[0] - 0.3, YEARS[-1] + 0.3)
    ax.set_ylim(*ylim)
    ax.tick_params(labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, alpha=0.3, linestyle="--")


def _plot_all(ax, key, lw_boost=("B", "C")):
    for k, sc in SCENARIOS.items():
        lw = 2.5 if k in lw_boost else 1.7
        ls = "-" if k in lw_boost else "--"
        ax.plot(YEARS, sc[key], color=COLOR[k], linewidth=lw, linestyle=ls, label=LABEL[k])
        ax.annotate(f"{sc[key][-1]:.0f}",
                    xy=(YEARS[-1], sc[key][-1]),
                    xytext=(3, 0), textcoords="offset points",
                    fontsize=7.5, color=COLOR[k], va="center")


def _legend(ax, **kw):
    handles = [mpatches.Patch(color=COLOR[k], label=LABEL[k]) for k in ("A", "B", "C", "D")]
    ax.legend(handles=handles, fontsize=7.5, framealpha=0.85, **kw)


def _save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  OK {path}")


# ══════════════════════════════════════════════════════════════════════════════
# Plot 1 — Funding comparison
# ══════════════════════════════════════════════════════════════════════════════

def plot_funding():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    fig.suptitle("Carbon Credit vs. Cooling Credit Funding Index (2015–2035)",
                 fontsize=12, fontweight="bold")

    _ax_base(ax1, "Carbon Credit Funding Index", "Index (0–100)", ylim=(0, 100))
    _ax_base(ax2, "Cooling Credit Funding Index", "Index (0–100)", ylim=(0, 100))

    for k, sc in SCENARIOS.items():
        lw = 2.5 if k == "A" else 1.7
        ls = "-" if k == "A" else "--"
        ax1.plot(YEARS, sc["carbon_credit_funding_index"],
                 color=COLOR[k], linewidth=lw, linestyle=ls, label=LABEL[k])

    for k, sc in SCENARIOS.items():
        lw = 2.5 if k in ("B", "C") else 1.7
        ls = "-" if k in ("B", "C") else "--"
        ax2.plot(YEARS, sc["cooling_credit_funding_index"],
                 color=COLOR[k], linewidth=lw, linestyle=ls, label=LABEL[k])

    ax1.text(0.03, 0.96,
             "In Scenario A, most climate\nfinance flows to carbon accounting.",
             transform=ax1.transAxes, fontsize=7.5, va="top", color="grey")
    ax2.text(0.03, 0.96,
             "In Scenarios B and C, the same or\nlarger finance is redirected to\nmeasurable physical cooling.",
             transform=ax2.transAxes, fontsize=7.5, va="top", color="#1F77B4")

    for ax in (ax1, ax2):
        _legend(ax, loc="lower right")

    _save(fig, "carbon_credit_vs_cooling_credit_funding.png")


# ══════════════════════════════════════════════════════════════════════════════
# Plot 2 — Heat load reduction pathways
# ══════════════════════════════════════════════════════════════════════════════

def plot_heat_load():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    _ax_base(ax, "Heat Load Reduction Pathways  (0–100, higher = more accumulated heat)",
             "Heat Load Index", ylim=(28, 90))

    _plot_all(ax, "heat_load_index")

    # Gap annotation
    y_a = SCENARIOS["A"]["heat_load_index"][-1]
    y_c = SCENARIOS["C"]["heat_load_index"][-1]
    ax.annotate("", xy=(2034.5, y_c), xytext=(2034.5, y_a),
                arrowprops=dict(arrowstyle="<->", color="purple", lw=1.5))
    ax.text(2034.7, (y_a + y_c) / 2, f"Gap\n{y_a - y_c:.0f} pts",
            fontsize=8, color="purple", va="center")

    ax.fill_between(YEARS,
                    SCENARIOS["A"]["heat_load_index"],
                    SCENARIOS["C"]["heat_load_index"],
                    alpha=0.09, color=COLOR["C"], label="Heat load gap (A − C)")

    ax.text(0.02, 0.04,
            "Cooling Credit redirects finance to physical cooling, soil, water cycle, forest, and ocean.\n"
            "This reduces the rate of heat-load accumulation in the Earth system.",
            transform=ax.transAxes, fontsize=7.5, color="grey")

    _legend(ax, loc="upper left")
    _save(fig, "heat_load_reduction_pathways.png")


# ══════════════════════════════════════════════════════════════════════════════
# Plot 3 — Natural cooling recovery index
# ══════════════════════════════════════════════════════════════════════════════

def plot_natural_cooling():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    _ax_base(ax,
             "Natural Cooling Function Recovery Index  (0–100)",
             "Natural Cooling Function Index", ylim=(40, 100))

    _plot_all(ax, "natural_cooling_function_index")
    ax.fill_between(YEARS,
                    SCENARIOS["A"]["natural_cooling_function_index"],
                    SCENARIOS["C"]["natural_cooling_function_index"],
                    alpha=0.1, color=COLOR["C"])

    ax.text(0.02, 0.04,
            "Composite of: forest evapotranspiration, soil moisture, water cycle, urban cooling,\n"
            "ocean circulation, and biological cooling functions. Proxy index, not a direct measurement.",
            transform=ax.transAxes, fontsize=7.5, color="grey")

    _legend(ax, loc="lower right")
    _save(fig, "natural_cooling_recovery_index.png")


# ══════════════════════════════════════════════════════════════════════════════
# Plot 4 — Water cycle recovery index (multi-dimension)
# ══════════════════════════════════════════════════════════════════════════════

def plot_water_cycle():
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Water Cycle and Land Cooling Recovery Indexes  (2015–2035)",
                 fontsize=12, fontweight="bold")

    dims = [
        ("water_cycle_recovery_index",               "Water Cycle Recovery"),
        ("soil_moisture_recovery_index",             "Soil Moisture Recovery"),
        ("forest_evapotranspiration_recovery_index", "Forest Evapotranspiration Recovery"),
    ]

    for ax, (key, title) in zip(axes, dims):
        _ax_base(ax, title, "Index (0–100)", ylim=(38, 100))
        _plot_all(ax, key)
        _legend(ax, loc="lower right")

    axes[0].text(0.03, 0.05,
                 "Cooling Credit directly incentivizes\nwatershed and soil-water restoration.",
                 transform=axes[0].transAxes, fontsize=7, color="grey")
    axes[1].text(0.03, 0.05,
                 "Soil moisture is a key land-surface\ncooling buffer.",
                 transform=axes[1].transAxes, fontsize=7, color="grey")
    axes[2].text(0.03, 0.05,
                 "Forest evapotranspiration is the\nprimary land cooling mechanism.",
                 transform=axes[2].transAxes, fontsize=7, color="grey")

    _save(fig, "water_cycle_recovery_index.png")


# ══════════════════════════════════════════════════════════════════════════════
# Plot 5 — Ocean heat and El Nino risk
# ══════════════════════════════════════════════════════════════════════════════

def plot_ocean_el_nino():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    fig.suptitle("Ocean Heat Moderation and El Nino Heat-Risk Moderation (2015–2035)",
                 fontsize=12, fontweight="bold")

    _ax_base(ax1, "Ocean Heat Moderation Index", "Index (0–100, higher = better moderated)",
             ylim=(40, 100))
    _ax_base(ax2, "El Nino Heat-Risk Moderation Index",
             "Index (0–100, higher = lower heat-risk amplification)", ylim=(38, 95))

    _plot_all(ax1, "ocean_heat_moderation_index")
    _plot_all(ax2, "el_nino_heat_risk_moderation_index")

    for ax in (ax1, ax2):
        _legend(ax, loc="lower right")

    ax1.text(0.03, 0.05,
             "Ocean heat moderation improved by reduced background heat load,\n"
             "land-water cooling recovery, and watershed restoration support.",
             transform=ax1.transAxes, fontsize=7, color="grey")
    ax2.text(0.03, 0.05,
             "Cooling Credit does NOT stop El Nino. It moderates the heat-risk\n"
             "AMPLIFICATION from El Nino through reduced background heat load\n"
             "and improved land-water cooling buffers. (Proxy index.)",
             transform=ax2.transAxes, fontsize=7, color="#B22222")

    _save(fig, "ocean_heat_and_el_nino_risk_index.png")


# ══════════════════════════════════════════════════════════════════════════════
# Plot 6 — Cooling Credit scaling effect (bar chart at 2035)
# ══════════════════════════════════════════════════════════════════════════════

def plot_scaling_effect():
    dims = [
        ("natural_cooling_function_index",           "Natural\nCooling\nFunction"),
        ("water_cycle_recovery_index",               "Water\nCycle\nRecovery"),
        ("urban_heat_reduction_index",               "Urban\nHeat\nReduction"),
        ("ocean_heat_moderation_index",              "Ocean\nHeat\nModeration"),
        ("el_nino_heat_risk_moderation_index",       "El Nino\nRisk\nModeration"),
        ("warming_mitigation_index",                 "Warming\nMitigation"),
    ]
    # heat_load_index is inverted (lower = better) — show gap from A
    # We'll show absolute values for all forward indicators

    x = np.arange(len(dims))
    width = 0.2
    offsets = {"A": -1.5 * width, "B": -0.5 * width, "C": 0.5 * width, "D": 1.5 * width}

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_title("Cooling Credit Scaling Effect — Index Values at 2035 (by scenario)",
                 fontsize=12, fontweight="bold", pad=12)

    for k, sc in SCENARIOS.items():
        vals = [float(sc[key][-1]) for key, _ in dims]
        bars = ax.bar(x + offsets[k], vals, width, color=COLOR[k],
                      alpha=0.85, label=LABEL[k])
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
                    f"{v:.0f}", ha="center", va="bottom", fontsize=7, color=COLOR[k],
                    fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels([lbl for _, lbl in dims], fontsize=9)
    ax.set_ylabel("Index value at 2035  (0–100)", fontsize=9)
    ax.set_ylim(0, 110)
    ax.legend(fontsize=8.5, loc="upper right", framealpha=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, alpha=0.3, linestyle="--", axis="y")
    ax.text(0.01, 0.02,
            "Larger Cooling Credit scale (C) consistently outperforms Carbon Credit baseline (A) across all dimensions.",
            transform=ax.transAxes, fontsize=8, color="grey")

    _save(fig, "cooling_credit_scaling_effect.png")


# ══════════════════════════════════════════════════════════════════════════════
# Plot 7 — Policy transition causal loop diagram
# ══════════════════════════════════════════════════════════════════════════════

def plot_causal_loop():
    fig, ax = plt.subplots(figsize=(14, 9.5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9.5)
    ax.axis("off")
    ax.set_facecolor("#FAFAFA")
    fig.patch.set_facecolor("#FAFAFA")

    ax.set_title(
        "Policy Transition Causal Loop — Carbon Credit vs. Cooling Credit Pathways",
        fontsize=12, fontweight="bold", pad=16,
    )

    # Node layout: (x, y, label, color)
    nodes = [
        # Finance inputs
        (2.2,  8.8, "Carbon Credit\nFinance",                  "#B22222"),
        (11.8, 8.8, "Cooling Credit\nFinance",                 "#1F77B4"),
        # Intermediate
        (2.2,  7.2, "Carbon\nAccounting",                      "#D62728"),
        (11.8, 7.2, "Physical Cooling\nInvestment",            "#1F77B4"),
        # Physical cooling branches
        (5.5,  5.8, "Urban Heat\nReduction",                   "#2CA02C"),
        (9.0,  5.8, "Forest\nEvapotranspiration\nRecovery",    "#228B22"),
        (7.0,  4.6, "Water Cycle &\nSoil Moisture\nRecovery", "#006400"),
        # Emissions reduction (weak path from carbon accounting)
        (2.2,  5.6, "Emissions\nReduction",                    "#E07000"),
        # Natural cooling
        (7.0,  3.2, "Natural Cooling\nFunction Recovery",      "#00688B"),
        # Ocean
        (7.0,  2.0, "Ocean Heat\nModeration",                  "#00509E"),
        # El Nino
        (7.0,  0.9, "El Nino Heat-Risk\nModeration",           "#3A3A8C"),
        # Heat load
        (11.8, 2.0, "Heat Load\nReduction",                    "#8B0000"),
        # Warming mitigation
        (7.0,  7.4, "Warming\nMitigation",                     "#4B0082"),
    ]

    node_pos = {}
    for (x, y, lbl, col) in nodes:
        node_pos[lbl] = (x, y)
        fc = col + "18"
        box = FancyBboxPatch(
            (x - 1.15, y - 0.42), 2.3, 0.84,
            boxstyle="round,pad=0.1", linewidth=1.4,
            edgecolor=col, facecolor=fc, zorder=3,
        )
        ax.add_patch(box)
        ax.text(x, y, lbl, ha="center", va="center", fontsize=8,
                fontweight="bold", color=col, zorder=4)

    # Edges: (from, to, label, style, color)
    edges = [
        ("Carbon Credit\nFinance",  "Carbon\nAccounting",                 "funds",           "#B22222"),
        ("Carbon\nAccounting",      "Emissions\nReduction",               "partial impact",  "#D62728"),
        ("Emissions\nReduction",    "Warming\nMitigation",                "weak-moderate",   "#E07000"),
        ("Carbon Credit\nFinance",  "Warming\nMitigation",                "",                "#D62728"),
        ("Cooling Credit\nFinance", "Physical Cooling\nInvestment",       "funds",           "#1F77B4"),
        ("Physical Cooling\nInvestment", "Urban Heat\nReduction",         "",                "#2CA02C"),
        ("Physical Cooling\nInvestment", "Forest\nEvapotranspiration\nRecovery", "",         "#228B22"),
        ("Physical Cooling\nInvestment", "Water Cycle &\nSoil Moisture\nRecovery", "",       "#006400"),
        ("Urban Heat\nReduction",   "Natural Cooling\nFunction Recovery", "",                "#2CA02C"),
        ("Forest\nEvapotranspiration\nRecovery", "Natural Cooling\nFunction Recovery", "",   "#228B22"),
        ("Water Cycle &\nSoil Moisture\nRecovery", "Natural Cooling\nFunction Recovery", "","#006400"),
        ("Natural Cooling\nFunction Recovery", "Ocean Heat\nModeration",  "",                "#00688B"),
        ("Ocean Heat\nModeration",  "El Nino Heat-Risk\nModeration",      "indirect",        "#00509E"),
        ("Natural Cooling\nFunction Recovery", "Heat Load\nReduction",    "",                "#8B0000"),
        ("Natural Cooling\nFunction Recovery", "Warming\nMitigation",     "",                "#4B0082"),
        ("Heat Load\nReduction",    "Warming\nMitigation",                "",                "#8B0000"),
    ]

    def _arrow(ax, x0, y0, x1, y1, col, lbl="", rad=0.05):
        dx = x1 - x0; dy = y1 - y0
        nn = max((dx ** 2 + dy ** 2) ** 0.5, 0.01)
        sh = 0.5
        xs = x0 + sh * dx / nn
        ys = y0 + sh * dy / nn
        xe = x1 - sh * dx / nn
        ye = y1 - sh * dy / nn
        ax.annotate("", xy=(xe, ye), xytext=(xs, ys),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.25,
                                    connectionstyle=f"arc3,rad={rad}"),
                    zorder=2)
        if lbl:
            mx, my = (xs + xe) / 2, (ys + ye) / 2
            ax.text(mx, my, lbl, fontsize=6.5, color=col,
                    ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.08", fc="white", alpha=0.75, lw=0))

    for (src, dst, lbl, col) in edges:
        x0, y0 = node_pos[src]
        x1, y1 = node_pos[dst]
        _arrow(ax, x0, y0, x1, y1, col, lbl)

    # Weak path annotation
    ax.text(2.2, 6.3,
            "Carbon Credit has weak coefficients\nfor direct physical cooling\n(primary effect: accounting)",
            ha="center", va="center", fontsize=7, color="#B22222",
            bbox=dict(boxstyle="round", fc="#FFF0F0", ec="#B22222", alpha=0.85))

    # Legend box
    ax.text(0.01, 0.01,
            "Cooling Credit finance flows directly to physical cooling, water cycle,\n"
            "soil, forest evapotranspiration, and urban cooling — the 'missing layer'\n"
            "that Carbon Credit finance does not typically reach.",
            transform=ax.transAxes, fontsize=8, va="bottom",
            bbox=dict(boxstyle="round", fc="#EFF8FF", ec="#1F77B4", alpha=0.9))

    _save(fig, "policy_transition_causal_loop.png")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("\nCarbon Credit to Cooling Credit Transition Simulation")
    print("=" * 55)
    print("Generating outputs...\n")

    print("[1/8] CSV results...")
    export_csv()

    print("[2/8] Funding comparison...")
    plot_funding()

    print("[3/8] Heat load reduction pathways...")
    plot_heat_load()

    print("[4/8] Natural cooling recovery index...")
    plot_natural_cooling()

    print("[5/8] Water cycle recovery index...")
    plot_water_cycle()

    print("[6/8] Ocean heat and El Nino risk index...")
    plot_ocean_el_nino()

    print("[7/8] Cooling Credit scaling effect...")
    plot_scaling_effect()

    print("[8/8] Policy transition causal loop...")
    plot_causal_loop()

    print(f"\nAll outputs written to: {OUTPUT_DIR}")
    print("\nNOTE: This is a conceptual counterfactual simulation.")
    print("Indexes are illustrative proxies, not measured global totals.")


if __name__ == "__main__":
    main()
