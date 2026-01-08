# ---
# jupytext:
#   formats: py:percent
#   text_representation:
#     extension: .py
#     format_name: percent
# ---

# %%
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "derived" / "master_dataset.csv"

# %%
df = pd.read_csv(MASTER)
df

# %%
# Separate biomarker and behavior data
biomarker_df = df[df["measure_kind"] == "biomarker"]
behavior_df = df[df["measure_kind"] == "behavior"]

# Match by study_id and plot
plt.figure()
for study_id in biomarker_df["study_id"].unique():
    bio = biomarker_df[biomarker_df["study_id"] == study_id]["effect_value"].values
    beh = behavior_df[behavior_df["study_id"] == study_id]["effect_value"].values
    if len(bio) > 0 and len(beh) > 0:
        plt.scatter(bio[0], beh[0])

plt.xlabel("biomarker effect size (d)")
plt.ylabel("behavior effect size (d)")
plt.title("starter: inverted-U table subset (scatter)")
plt.show()
