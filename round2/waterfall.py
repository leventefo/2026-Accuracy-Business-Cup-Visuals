import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from plotly.colors import n_colors
import statistics

def plot(fig):

    fig.add_trace(go.Waterfall(
      measure = ["absolute", "relative", "relative", "relative", "relative", "total"],
      x = ["Affordable baseline", "Safety & ADAS", "CO2 comliance tech",
           "Euro 7 pollutant compliance",
           "eCall + telematics", ["End price"]],
           y = [14000, 600, 2400, 1800, 200, 19000],
           connector = {"line": {"color" : "#203050"}},
           text = ["14000€", "+600€", "+2400€", "+1800€", "+200€", "19000€"],
                      textposition="outside",
           decreasing = {"marker":{"color":"Maroon", "line":{"color":"red", "width":2}}},
            increasing = {"marker":{"color":"#8b0000"}},
             totals = {"marker":{"color":"#224993", "line":{"color":"#203050", "width":3}}}), row = 1, col = 1)
    

    fig.add_trace(go.Waterfall(
      measure = ["absolute", "relative", "relative", "relative", "relative", "total"],
      x = ["Affordable baseline", "Safety & ADAS", "CO2 comliance tech",
           "Euro 7 pollutant compliance",
           "eCall + telematics", ["End price"]],
           y = [42222, 600, 2400, 1800, 200, 47222],
           connector = {"line": {"color" : "#203050"}},
           text = ["42222€", "+600€", "+2400€", "+1800€", "+200€", "47222€"],
                      textposition="outside",
           decreasing = {"marker":{"color":"Maroon", "line":{"color":"red", "width":2}}},
            increasing = {"marker":{"color":"#8b0000"}},
             totals = {"marker":{"color":"#224993", "line":{"color":"#203050", "width":3}}}), row = 1, col = 2)
    

    fig.write_image("Cost_burden.png", width = 1200, height = 550, scale = 6)

    #fig.show(renderer = "browser")



def create_figure():

    fig = make_subplots(rows = 1, cols = 2, horizontal_spacing = 0.07, subplot_titles=("A-segment", "Average mainstream")).update_layout(template ="plotly_white", title = "", title_x = 0.5, title_y = 0.98, title_font_weight = 600)
    fig.update_layout(margin=dict(t=85, b=0, l=80, r=0))
    fig.update_layout(width = 1200, height = 550)
    fig.update_layout(font_family = "Georgia", font_weight = 600, font_size = 18, showlegend = False)
    fig.update_yaxes(title_text = "Cost burden (€)", row = 1, col =1)
    fig.update_yaxes(title_text = None, row = 1, col =2, title_standoff = 20)
    fig.update_xaxes(showticklabels = False)
    #fig.update_yaxes(title_text = "", row = 1, col = 2)
    fig.update_layout(paper_bgcolor = "#F3F4F6")
    fig.update_layout(plot_bgcolor = "#F3F4F6")
    fig.update_xaxes(tickprefix = " ")
    fig.update_annotations(yshift=40)
    fig.update_annotations(font_size=25)

    


    plot(fig)
    




def main():

    create_figure()


main()
    



