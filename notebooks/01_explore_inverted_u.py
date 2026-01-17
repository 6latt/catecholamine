# ---
# jupytext:
#   formats: py:percent
#   text_representation:
#     extension: .py
#     format_name: percent
# ---

# %% [markdown]
# # Inverted-U Relationship Exploration
#
# This notebook explores the inverted-U relationship between catecholamine levels
# and cognitive performance using the master dataset.

# %%
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "derived" / "master_dataset.csv"

# %% [markdown]
# ## Load Master Dataset

# %%
df = pd.read_csv(MASTER)
print(f"Loaded {len(df)} rows from master dataset")
df.head()

# %% [markdown]
# ## Biomarker vs Behavior Scatter Plot
#
# This plot shows the relationship between biomarker effect sizes (e.g., dopamine levels)
# and behavioral effect sizes (e.g., working memory performance) for matching studies.

# %%
# Separate biomarker and behavior data
biomarker_df = df[df["measure_kind"] == "biomarker"]
behavior_df = df[df["measure_kind"] == "behavior"]

# Match by study_id and plot
plt.figure(figsize=(8, 6))
points_plotted = False

for study_id in biomarker_df["study_id"].unique():
    bio = biomarker_df[biomarker_df["study_id"] == study_id]["effect_value"].values
    beh = behavior_df[behavior_df["study_id"] == study_id]["effect_value"].values
    
    if len(bio) > 0 and len(beh) > 0:
        plt.scatter(bio[0], beh[0], alpha=0.6, s=50)
        points_plotted = True

if not points_plotted:
    plt.close()
    print("No paired biomarker/behavior data found with matching study_id values.")
    print("Nothing to plot.")
else:
    plt.xlabel("Biomarker Effect Size (Cohen's d)")
    plt.ylabel("Behavior Effect Size (Cohen's d)")
    plt.title("Inverted-U Pattern: Biomarker vs Behavior Effects")
    plt.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.3)
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.show()

# %%
