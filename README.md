# Cascades on Random Networks with Never-Adopters

Model code for the proposal in `../paper/proposal.pdf`.

## Install dependencies

```
pip install -r requirements.txt
```

## Run

Launch the interactive GUI with solara:

```
solara run app.py
```

This opens the model in your browser. Use the sliders on the left to
change `N`, `z`, `phi_star`, `q`, and the immunity pattern; the network
plot and the adoption time series update live.

## Files

- `agent.py` — threshold-rule agent.
- `model.py` — cascade model and the three immunity patterns.
- `app.py` — solara GUI launcher.
