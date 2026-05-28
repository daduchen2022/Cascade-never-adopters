# Cascades on Random Networks with Never-Adopters

## What's new in this version compared with the draft

- **`batch.py`** (new) runs the model over a sweep of mean degree `z`
  for the two research questions and produces the analysis figures
  `figure1_prevalence.pdf` (effect of the never-adopter fraction `q`)
  and `figure2_pattern.pdf` (effect of the spatial pattern), each at
  100 runs per setting with binomial error bars.
- The model code (`agent.py`, `model.py`, `app.py`) is otherwise
  unchanged. The three immunity patterns, including the
  homophily-driven spread of immunity, live in `model.py`
  (`_iid`, `_block`, `_homophily`).

## Install dependencies

```
pip install -r requirements.txt
```

## Run the GUI

```
solara run app.py
```

## Reproduce the analysis figures

```
python batch.py
```

This sweeps the mean degree `z` for the two research questions and
writes `figure1_prevalence.pdf` (effect of the never-adopter fraction
`q`) and `figure2_pattern.pdf` (effect of the spatial pattern).

## Files

- `agent.py` — threshold-rule agent.
- `model.py` — cascade model and the three immunity patterns.
- `app.py` — solara GUI.
- `batch.py` — parameter sweeps that produce the analysis figures.
