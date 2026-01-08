from __future__ import annotations

import matplotlib.pyplot as plt


def savefig(path: str, dpi: int = 200) -> None:
    """Consistent save helper."""
    plt.tight_layout()
    plt.savefig(path, dpi=dpi)
    plt.close()
