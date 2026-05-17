from model import CascadeModel
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)
from mesa.visualization.components import AgentPortrayalStyle


## Node colors:
##   red       -> immune (never-adopter), state locked at 0
##   tab:blue  -> active (adopted)
##   lightgray -> inactive
def agent_portrayal(agent):
    if agent.immune:
        color = "tab:red"
    elif agent.active:
        color = "tab:blue"
    else:
        color = "lightgray"
    return AgentPortrayalStyle(color=color, marker="o", size=20)


## GUI defaults use N = 10000, but for the
## interactive demo we drop N to a few hundred so the network render is
## readable and the run completes quickly.
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "N": Slider("Population N", value=500, min=100, max=2000, step=100),
    "z": Slider("Mean degree z", value=4.0, min=1.0, max=10.0, step=0.5),
    "phi_star": Slider("Mean threshold phi*", value=0.18, min=0.05, max=0.45, step=0.01),
    "q": Slider("Never-adopter fraction q", value=0.10, min=0.0, max=0.40, step=0.01),
    "pattern": {
        "type": "Select",
        "value": "iid",
        "values": CascadeModel.patterns,
        "label": "Immunity pattern",
    },
}


## Start the GUI with a 500-node network so the very first render is
## fast and readable; users can pull the slider up to 2000 once the page
## has loaded.
cascade_model = CascadeModel(N=500)
SpaceGraph = make_space_component(agent_portrayal, draw_grid=False)
ActivePlot = make_plot_component({"active_fraction": "tab:blue"})

page = SolaraViz(
    cascade_model,
    components=[SpaceGraph, ActivePlot],
    model_params=model_params,
    name="Cascades on Random Networks with Never-Adopters",
)
page
