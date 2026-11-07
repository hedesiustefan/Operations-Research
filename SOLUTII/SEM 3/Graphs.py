from pydantic import BaseModel, model_validator
from typing import Optional
from networkx import DiGraph
import pulp
import time

class Node(BaseModel, frozen=True):
    """
    class of network node with attributes:
    name: str - name of node
    demand: float - demand of node (if node is destination)
    supply: float - supply of node (if node is source)
    capacity: float - maximum flow out of node
    type: str - type of node
    x: float - x-coordinate of node
    y: float - y-coordinate of node
    fixed_cost: float - cost of selecting node
    """
    name: str 
    demand : float | dict[str, float] = 0.0
    supply : float | dict[str, float] = 0.0
    capacity : Optional[float] = float('inf')
    type : Optional[str] = None
    x : Optional[float] = 0.0
    y : Optional[float] = 0.0
    fixed_cost : Optional[float] = 0.0

    @model_validator(mode='after')
    def validate(self):
        if any(v < 0 for v in (self.demand.values() if isinstance(self.demand, dict) else [self.demand])):
            raise ValueError("Demand cannot be negative")
        if any(v < 0 for v in (self.supply.values() if isinstance(self.supply, dict) else [self.supply])):
            raise ValueError("Supply cannot be negative")
        if self.capacity is not None and self.capacity < 0:
            raise ValueError("Capacity cannot be negative")
        if self.fixed_cost < 0:
            raise ValueError("Fixed cost cannot be negative")
        return self

class Edge(BaseModel, frozen=True):
    """class of edge between two nodes with attributes:
    origin: 'Node' - origin node of edge
    destination: 'Node' - destination node of edge
    capacity: float - maximum flow through edge
    variable_cost: float - cost per unit flow through edge
    fixed_cost: float - cost of selecting edge
    """
    origin: Node
    destination: Node
    capacity: Optional[float] = float('inf')
    variable_cost: Optional[float] = 0.0
    fixed_cost: Optional[float] = 0.0

    @model_validator(mode='after')
    def validate(self):
        """validate of edge definition is correct"""
        # check that node names are different
        if self.origin.name == self.destination.name:
            raise ValueError('origin and destination names must be different')
        # check that capacity is non-negative
        if self.capacity < 0:
            raise ValueError('capacity must be non-negative')
        # check that variable_cost is non-negative
        if self.variable_cost < 0:
            raise ValueError('variable_cost must be non-negative')
        # check that fixed_cost is non-negative
        if self.fixed_cost < 0:
            raise ValueError('fixed_cost must be non-negative')
        return self

class FlowGraph(DiGraph):
    """class to define and solve minimum cost flow problems"""

    def __init__(self, nodes: list[Node], edges: list[Edge]):
        """initialize graph with nodes and edges"""
        super().__init__()
        for node in nodes:
            self.add_node(node)
        for edge in edges:
            self.add_edge(edge)

    def add_node(self, node: Node):
        """add node to graph"""
        if not isinstance(node, Node):
            raise TypeError("node must be an instance of Node class")
        super().add_node(node.name, demand=node.demand, supply=node.supply, capacity=node.capacity, type=node.type, x=node.x, y=node.y, fixed_cost=node.fixed_cost)

    def add_edge(self, edge: Edge):
        """add edge to graph"""
        if not isinstance(edge, Edge):
            raise TypeError("edge must be an instance of Edge class")
        super().add_edge(edge.origin.name, edge.destination.name, capacity=edge.capacity, variable_cost=edge.variable_cost, fixed_cost=edge.fixed_cost)

    def min_cost_flow(self, integer=False, verbose=True):
        """
        run minimum cost flow optimization
        @param integer: bool - require integer flows (default: False)
        @param verbose: bool - print optimization status (default: True)
        @return: status of optimization
        """
        self.verbose = verbose
        self.integer = integer
        self.commodities = self._get_commodities()

        start_time = time.time()
        self.prob = pulp.LpProblem("FlowGraph_min_cost_flow", pulp.LpMinimize)
        self._assign_decision_variables()
        self._assign_objective_function()
        self._assign_constraints()
        if self.verbose:
            print(f"Model creation time: {time.time() - start_time:.2f} s")

        start_time = time.time()
        self.result = self.prob.solve(pulp.HiGHS(msg=False))
        solve_time = time.time() - start_time

        status = self.result.status_str
        if self.verbose:
            if status == "Optimal":
                print(f"Optimal solution found: {self.result.objective:.2f} in {solve_time:.2f} s")
            else:
                print(f"Optimization status: {status} in {solve_time:.2f} s")

        self._assign_variable_values(status == "Optimal")
        return status

    def max_flow(self, source, sink, integer=False, verbose=True):
        """
        run maximum flow optimization (single commodity)
        @param source: name of the source node
        @param sink: name of the sink node
        @param integer: bool - require integer flows (default: False)
        @param verbose: bool - print optimization status (default: True)
        @return: status of optimization
        """
        self.verbose = verbose
        self.integer = integer
        self.commodities = [None]

        self.prob = pulp.LpProblem("FlowGraph_max_flow", pulp.LpMaximize)
        self._assign_decision_variables()

        # objective: net flow leaving the source
        self.prob += (pulp.lpSum(self.flow[source, v, None] for v in self.successors(source))
                      - pulp.lpSum(self.flow[u, source, None] for u in self.predecessors(source)))

        for n, data in self.nodes(data=True):
            inflow = pulp.lpSum(self.flow[u, n, None] for u in self.predecessors(n))
            outflow = pulp.lpSum(self.flow[n, v, None] for v in self.successors(n))
            # flow conservation at every node except source and sink
            if n not in (source, sink):
                self.prob += inflow == outflow, f"Conservation_{n}"
            if data["capacity"] is not None and data["capacity"] != float("inf"):
                self.prob += outflow <= data["capacity"], f"Capacity_{n}"

        for u, v, data in self.edges(data=True):
            if data["capacity"] is not None and data["capacity"] != float("inf"):
                self.prob += self.flow[u, v, None] <= data["capacity"], f"Edge_capacity_{u}_{v}"

        self.result = self.prob.solve(pulp.HiGHS(msg=False))
        status = self.result.status_str
        if self.verbose:
            if status == "Optimal":
                print(f"Maximum flow found: {self.result.objective:.2f}")
            else:
                print(f"Optimization status: {status}")

        self._assign_variable_values(status == "Optimal")
        return status

    def _get_commodities(self):
        keys = set()
        for _, data in self.nodes(data=True):
            for attr in ("demand", "supply"):
                if isinstance(data[attr], dict):
                    keys.update(data[attr].keys())
        return sorted(keys) if keys else [None]

    def _node_value(self, data, attr, k):
        value = data[attr]
        return value.get(k, 0.0) if isinstance(value, dict) else value

    def _assign_decision_variables(self):
        """one flow variable per edge, bounded by the edge capacity"""
        cat = "Integer" if self.integer else "Continuous"
        self.flow = {}
        for u, v, data in self.edges(data=True):
            for k in self.commodities:
                self.flow[u, v, k] = self.prob.add_variable(
                    f"flow_{u}_{v}" + (f"_{k}" if k is not None else ""), lowBound=0, cat=cat,
                )
        self.open = {
            n: self.prob.add_variable(f"open_{n}", cat="Binary")
            for n, data in self.nodes(data=True) if data["fixed_cost"]
        }

    def _assign_objective_function(self):
        """total transport cost"""
        self.prob += (pulp.lpSum(data["variable_cost"] * self.flow[u, v, k] for u, v, data in self.edges(data=True) for k in self.commodities)
                      + pulp.lpSum(self.nodes[n]["fixed_cost"] * y for n, y in self.open.items()))

    def _assign_constraints(self):
        """flow balance and node capacity for every node"""
        big_m = sum(self._node_value(data, "supply", k) for _, data in self.nodes(data=True) for k in self.commodities)
        for n, data in self.nodes(data=True):
            for k in self.commodities:
                inflow = pulp.lpSum(self.flow[u, n, k] for u in self.predecessors(n))
                outflow = pulp.lpSum(self.flow[n, v, k] for v in self.successors(n))
                # what arrives plus what the node supplies must cover what it sends on plus its demand
                self.prob += inflow - outflow >= self._node_value(data, "demand", k) - self._node_value(data, "supply", k), f"Balance_{n}" + (f"_{k}" if k is not None else "")
            total_outflow = pulp.lpSum(self.flow[n, v, k] for v in self.successors(n) for k in self.commodities)
            if data["capacity"] is not None and data["capacity"] != float("inf"):
                self.prob += total_outflow <= data["capacity"], f"Capacity_{n}"
            if n in self.open:
                m = data["capacity"] if data["capacity"] not in (None, float("inf")) else big_m
                self.prob += total_outflow <= m * self.open[n], f"Open_{n}"
        for u, v, data in self.edges(data=True):
            if data["capacity"] is not None and data["capacity"] != float("inf"):
                self.prob += pulp.lpSum(self.flow[u, v, k] for k in self.commodities) <= data["capacity"], f"Edge_capacity_{u}_{v}"

    def _assign_variable_values(self, optimal):
        """store the optimal flow on each edge as the 'flow' attribute"""
        for u, v in self.edges():
            if not optimal:
                self.edges[u, v]["flow"] = None
            elif self.commodities == [None]:
                self.edges[u, v]["flow"] = self.flow[u, v, None].value()
            else:
                self.edges[u, v]["flow"] = {k: self.flow[u, v, k].value() for k in self.commodities}
        for n, y in getattr(self, "open", {}).items():
            self.nodes[n]["open"] = round(y.value()) if optimal else None