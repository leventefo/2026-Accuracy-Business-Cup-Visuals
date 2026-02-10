import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from plotly.colors import n_colors
import statistics


def create_figure(title):
    fig = go.Figure().update_layout(template ="plotly_white", title = title, title_x = 0.5, title_y = 0.95, title_font_weight = 600)
    fig.update_layout(width = 800, height = 600)

    return fig



def plot(fig, lst):

    fig.add_trace(go.Waterfall(
      measure = ["absolute", "relative", "relative", "relative", "relative", "total"],
      x = ["Baseline gross profit", "Tariff cost", "Pass-through",
           "Mitigation savings",
           "New gross profit"],
           y = lst,
           connector = {"line": {"color" : "red"}},
           text = ["8469$", "-16260$", "+4065$", "+4000$", 'Total'],
                      textposition="outside",
           decreasing = {"marker":{"color":"Maroon", "line":{"color":"red", "width":2}}},
            increasing = {"marker":{"color":"Teal"}},
             totals = {"marker":{"color":"deep sky blue", "line":{"color":"blue", "width":3}}}))


def touch_up(fig):
    
    fig.update_layout(margin=dict(t=60, b=80, l=130, r=80))
    fig.update_layout(font_family = "Georgia", font_weight = 600, font_size = 16)
    fig.update_yaxes(title_text = "Gross profit impact ($ / vehicle)")
    #fig.update_yaxes(title_text = "", row = 1, col = 2)
    fig.update_layout(paper_bgcolor = "#F3F4F6")
    fig.update_layout(plot_bgcolor = "#F3F4F6")
    fig.update_xaxes(tickprefix = " ")



def main():
    average_sale_price = 0.042344
    percent_imported_parts = 0.24
    cogs_percent_of_revenue = 0.8
    tariff_rate = 2
    tariff_absorption = 0.75
    pass_through_percent = 1 - tariff_absorption
    baseline_gp = average_sale_price * (1-cogs_percent_of_revenue)
    tariff_cost = average_sale_price * cogs_percent_of_revenue * percent_imported_parts * tariff_rate
    pass_through = tariff_cost * pass_through_percent
    mitigation = 20
    new_gp = baseline_gp - tariff_cost + pass_through + mitigation

    fig = create_figure("Representative Toyota “standard vehicle”")
    plot(fig, [8469, -16260, 4065, 4000, 274])

    touch_up(fig)

    #fig.show(renderer = "browser")
    fig.write_image("Tariff_pass_through.png", width = 900, height = 800, scale = 6)


main()
