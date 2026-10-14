from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Match the site's font: Times for text, STIX (a Times-like math font) for $...$
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "mathtext.fontset": "stix",
    "font.size": 12,
})

x = np.linspace(-2, 2, 200)

fig, ax = plt.subplots(figsize=(6, 3.5))
ax.plot(x, x**2, label=r"$y = x^2$")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False)

# Save next to this script, no matter which folder you run it from
out = Path(__file__).parent / "plot.svg"
fig.savefig(out, bbox_inches="tight", transparent=True)