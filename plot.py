from oemof import solph

import matplotlib.pyplot as plt
import plotly.graph_objects as go

def plot(es: solph.EnergySystem):
    if es is not None:
        # printEsGraph(es, image_directory)

        busses = []
        bus_figures = []

        results = es.results["main"]

        for node in es.nodes:
            if isinstance(node, solph.Bus):
                busses.append(node)

        for bus in busses:
            fig = go.Figure(layout=dict(title=f"{bus} bus"))
            for t, g in solph.views.node(results, node=bus)[
                "sequences"
            ].items():
                idx_asset = abs(t[0].index(bus) - 1)

                fig.add_trace(
                    go.Scatter(
                        x=g.index,
                        y=g.values * pow(-1, idx_asset),
                        name=t[0][idx_asset].label,
                    )
                )
            bus_figures.append(fig)
    
    return bus_figures