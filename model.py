import math
import networkx as nx
from mesa import Model
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
from agent import ThresholdAgent


class CascadeModel(Model):
    ## Watts threshold cascade on a Poisson random graph, with a fraction q of permanent never-adopters laid down in one of three patterns:
    ##   "iid"       -- each node independently marked with probability q
    ##   "block"     -- mark 2-step balls around random centers until the
    ##                  immune fraction reaches q
    ##   "homophily" -- grow from a small seed by local infection until
    ##                  the immune fraction reaches q
    ## In "block" and "homophily" we unmark a random subset of the last addition so the final fraction lands exactly at q.

    patterns = ["iid", "block", "homophily"]

    def __init__(self, N=10000, z=4.0, phi_star=0.18, q=0.10,
                 pattern="iid", seed=None):
        if seed is not None:
            seed = int(seed)
        super().__init__(rng=seed)

        self.N = N
        self.z = z
        self.phi_star = phi_star
        self.q = q
        self.pattern = pattern

        ## Random graph with Poisson degrees: G(N, p) with p = z/(N-1).
        p = z / (N - 1)
        self.G = nx.erdos_renyi_graph(N, p, seed=self.random.randint(0, 2**31 - 1))
        self.grid = NetworkGrid(self.G)

        ## Decide which nodes are immune, then place one agent per node.
        immune = self._assign_immune()
        for node in self.G.nodes():
            phi = self.random.uniform(phi_star - 0.05, phi_star + 0.05)
            self.grid.place_agent(ThresholdAgent(self, phi, node in immune), node)

        ## Cascade initialization: switch 0.1% of non-immune agents to state 1.
        non_immune = [a for a in self.agents if not a.immune]
        n_seed = max(1, math.ceil(0.001 * len(non_immune)))
        for a in self.random.sample(non_immune, n_seed):
            a.active = True

        ## Reporter state. active_fraction and newly_activated are read
        ## back by the DataCollector via their string names.
        active = sum(1 for a in self.agents if a.active)
        self.active_fraction = active / len(self.agents)
        self.newly_activated = 0

        self.datacollector = DataCollector(model_reporters={
            "active_fraction": "active_fraction",
            "newly_activated": "newly_activated",
        })
        self.datacollector.collect(self)
        self.running = True

    def step(self):
        ## One asynchronous pass over the agents; stop when nobody flipped.
        active_before = sum(1 for a in self.agents if a.active)
        self.agents.shuffle_do("step")
        active_after = sum(1 for a in self.agents if a.active)

        self.newly_activated = active_after - active_before
        self.active_fraction = active_after / len(self.agents)
        if self.newly_activated == 0:
            self.running = False
        self.datacollector.collect(self)

    def _assign_immune(self):
        ## Immunity assignment.
        target = math.ceil(self.q * self.N)
        if target == 0:
            return set()
        if self.pattern == "iid":
            return self._iid()
        if self.pattern == "block":
            return self._block(target)
        if self.pattern == "homophily":
            return self._homophily(target)
        raise ValueError(f"Unknown pattern: {self.pattern}")

    def _iid(self):
        ## Each node independently with probability q.
        return {n for n in self.G.nodes() if self.random.random() < self.q}

    def _block(self, target):
        ## Repeat: pick a non-immune center, mark every node within graph
        ## distance 2 of it. If the last addition pushes the count past
        ## target, randomly drop the extra back to non-immune.
        immune = set()
        all_nodes = set(self.G.nodes())
        while len(immune) < target:
            center = self.random.choice(list(all_nodes - immune))
            ball = set(nx.single_source_shortest_path_length(self.G, center, cutoff=2))
            new = ball - immune
            room = target - len(immune)
            if len(new) > room:
                new = set(self.random.sample(list(new), room))
            immune.update(new)
        return immune

    def _homophily(self, target):
        ## Mark a random seed of 10% of target. Then each round, every
        ## non-immune node turns immune with prob 0.15 * (immune neighbor
        ## share). Alter the last round if it goes past target.
        nodes = list(self.G.nodes())
        seed_size = max(1, math.ceil(0.1 * target))
        immune = set(self.random.sample(nodes, seed_size))
        for _ in range(10000):  ## Avoid infinite loop
            if len(immune) >= target:
                break
            added = []
            for n in nodes:
                if n in immune:
                    continue
                nbrs = list(self.G.neighbors(n))
                if not nbrs:
                    continue
                f = sum(1 for nb in nbrs if nb in immune) / len(nbrs)
                if self.random.random() < 0.15 * f:
                    added.append(n)
            room = target - len(immune)
            if len(added) > room:
                added = self.random.sample(added, room)
            immune.update(added)
        return immune
