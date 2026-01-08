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
plt.figure()
plt.scatter(df["effect_size_biomarker_d"], df["effect_size_behavior_d"])
plt.xlabel("biomarker effect size (d)")
plt.ylabel("behavior effect size (d)")
plt.title("starter: inverted-U table subset (scatter)")
plt.show()
