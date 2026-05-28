## Run the model across a sweep of mean degree z and save the two
## analysis figures: Figure 1 (effect of q) and Figure 2 (effect of pattern).

import math
import matplotlib
matplotlib.use("Agg")  ## no screen needed; we only save files
import matplotlib.pyplot as plt
from model import CascadeModel

N = 2000           ## number of nodes (people) in each run
PHI_STAR = 0.18    ## average threshold; this is the value Watts (2002)
                   ## uses for his cascade-window cross-section, so our
                   ## plots line up with his
N_RUNS = 100       ## times we repeat each setting, then average over
Z_VALUES = [1.0 + 0.5 * i for i in range(17)]   ## mean degrees 1.0 to 9.0


def cascade_probability(z, q, pattern):
    ## Run the model N_RUNS times at this setting. Return how often a
    ## global cascade happened (final adoption >= 50%) and the standard
    ## error of that fraction (the size of the error bars).
    hits = 0
    for run in range(N_RUNS):
        m = CascadeModel(N=N, z=z, phi_star=PHI_STAR, q=q,
                         pattern=pattern, seed=run)
        while m.running:
            m.step()
        if m.active_fraction >= 0.5:
            hits += 1
    p = hits / N_RUNS
    se = math.sqrt(p * (1 - p) / N_RUNS)   ## standard error of a fraction
    return p, se


def curve(q, pattern):
    ## Cascade probability (and its error bar) at every z in the sweep.
    probs, errors = [], []
    for z in Z_VALUES:
        p, se = cascade_probability(z, q, pattern)
        probs.append(p)
        errors.append(se)
    return probs, errors


def make_figure1():
    ## Question 1: vary the never-adopter fraction q, keep Scattered.
    fig, ax = plt.subplots(figsize=(5, 3.5))
    for q in [0.0, 0.10, 0.20]:
        probs, errors = curve(q, "iid")
        print(f"  q={q:.2f}: {[round(p, 2) for p in probs]}")
        ax.errorbar(Z_VALUES, probs, yerr=errors, marker="o", capsize=2,
                    label=f"q = {q:.2f}")
    ax.set_xlabel("mean degree z")
    ax.set_ylabel("P(global cascade)")
    ax.set_title(f"Scattered immunity, $\\phi_*$ = {PHI_STAR}")
    ax.legend()
    fig.tight_layout()
    fig.savefig("figure1_prevalence.pdf")


def make_figure2():
    ## Question 2: keep q = 0.10, compare the three immunity patterns.
    fig, ax = plt.subplots(figsize=(5, 3.5))
    for pattern in ["iid", "block", "homophily"]:
        probs, errors = curve(0.10, pattern)
        print(f"  {pattern}: {[round(p, 2) for p in probs]}")
        ax.errorbar(Z_VALUES, probs, yerr=errors, marker="o", capsize=2,
                    label=pattern)
    ax.set_xlabel("mean degree z")
    ax.set_ylabel("P(global cascade)")
    ax.set_title(f"q = 0.10, $\\phi_*$ = {PHI_STAR}")
    ax.legend()
    fig.tight_layout()
    fig.savefig("figure2_pattern.pdf")


if __name__ == "__main__":
    print("Figure 1: effect of q (Scattered)")
    make_figure1()
    print("Figure 2: effect of pattern (q = 0.10)")
    make_figure2()
    print("saved figure1_prevalence.pdf and figure2_pattern.pdf")
