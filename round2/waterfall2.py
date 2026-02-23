import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from plotly.colors import n_colors
import statistics

def plot(fig):

    fig.add_trace(go.Waterfall(
      measure = ["relative", "relative", "total"],
      x = ["Current Revenues", "Current Cost", ["Profit"]],
           y = [1349190000, -781110000, 56808000],
           connector = {"line": {"color" : "#203050"}},
           text = ["1.3B€", "-781M€", "568M€"],
                      textposition="outside",
           decreasing = {"marker":{"color":"Maroon", "line":{"color":"red", "width":2}}},
            increasing = {"marker":{"color":"green", "line":{"color":"limegreen", "width":2}}},
             totals = {"marker":{"color":"#224993", "line":{"color":"#203050", "width":3}}}), row = 1, col = 1)
    

    fig.add_trace(go.Waterfall(
      measure = ["relative", "relative", "relative", "relative", "total"],
      x = ["Current Revenues", "Loss Related To P Decrease", "Revenues Related To Q Increase", "Cost", ["Profit"]],
           y = [1349190000, -284040000, 403635789, -832311947, 636473842],
           connector = {"line": {"color" : "#203050"}},
           text = ["1.3B€", "-284M€", "+404M€", "-832M€", "636M€"],
                      textposition="outside",
           decreasing = {"marker":{"color":"Maroon", "line":{"color":"red", "width":2}}},
            increasing = {"marker":{"color":"green", "line":{"color":"limegreen", "width":2}}},
             totals = {"marker":{"color":"#224993", "line":{"color":"#203050", "width":3}}}), row = 1, col = 2)
    

    fig.write_image("Cost_burden2.png", width = 1500, height = 700, scale = 6)

    #fig.show(renderer = "browser")



def create_figure():

    fig = make_subplots(rows = 1, cols = 2, horizontal_spacing = 0.03, shared_yaxes= True, subplot_titles=("Profitability Pre JV", "Profitability Post JV")).update_layout(template ="plotly_white", title = "", title_x = 0.5, title_y = 0.98, title_font_weight = 600)
    fig.update_layout(margin=dict(t=85, b=0, l=80, r=0))
    fig.update_layout(width = 1200, height = 700)
    fig.update_layout(font_family = "Georgia", font_weight = 600, font_size = 18, showlegend = False)
    fig.update_yaxes(title_text = "Billions of €", row = 1, col =1)
    fig.update_yaxes(title_text = None, row = 1, col =2, title_standoff = 20)
    fig.update_xaxes(showticklabels = True)
    #fig.update_yaxes(title_text = "", row = 1, col = 2)
    fig.update_layout(paper_bgcolor = "#FFFFFF")
    fig.update_layout(plot_bgcolor = "#FFFFFF")
    fig.update_xaxes(tickprefix = " ")
    fig.update_annotations(yshift=20)
    fig.update_annotations(font_size=25)

    


    plot(fig)
    




def main():

    create_figure()


main()
    



