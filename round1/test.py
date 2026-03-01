import plotly.graph_objects as go

fig = go.Figure(go.Treemap(
    labels = ["A", "B", "C", "D", "E"],
    parents = ["", "A", "B", "C", "A"] 
))

fig.show(renderer = "browser")