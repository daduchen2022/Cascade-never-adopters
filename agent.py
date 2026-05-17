from mesa import Agent


class ThresholdAgent(Agent):
    ## Watts threshold rule with a never-adopter override.
    ## Non-immune agents adopt (state 1) when the fraction of their neighbors already in state 1 reaches their personal threshold phi.
    ## Adoption is irreversible (PAP). Immune agents stay at state 0 for the whole run no matter what their neighbors do.

    def __init__(self, model, phi, immune):
        super().__init__(model)
        self.phi = phi
        self.immune = immune
        self.active = False

    def step(self):
        if self.immune or self.active:
            return
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=False)
        if not neighbors:
            return
        active_share = sum(1 for n in neighbors if n.active) / len(neighbors)
        if active_share >= self.phi:
            self.active = True
