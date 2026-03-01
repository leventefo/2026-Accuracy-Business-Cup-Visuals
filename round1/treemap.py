import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests


def get_data():
    pass


def create_figure(title):
    fig = make_subplots(specs = [[{"type": "domain"}]]).update_layout(template ="plotly_white", title = title, title_x = 0.5, title_y = 0.98, title_font_weight = 600,
                                                                      title_font_size = 40)
    fig.update_layout(width = 800, height = 800)
    #fig.update_xaxes(range=[pd.Timestamp("2019-01-01"), pd.Timestamp("2026-01-01")])
    #fig.update_yaxes(range = [miny, maxy])
    return fig




def touch_up(fig):
    
    fig.update_layout(margin=dict(t=150, b=20, l=20, r=20))
    fig.update_layout(font_family = "Georgia", font_weight = 600, font_size = 35)
    fig.update_layout(paper_bgcolor = "#F3F4F6")
    fig.update_layout(plot_bgcolor = "#F3F4F6")


def convert_to_percentage_contribution(df):
    divisor = df.iloc[43,3]
    update_lst = []
    for value in df["YTD_2025_units"]:
        update_lst.append(round((value/divisor)*100,0))
    df["YTD_2025_units"] = update_lst

    #print(df["YTD_2025_units"])

def plot(df, fig):
    #values = list(range())
    df = df.iloc[:-1]
    #print(df["Brand"].to_numpy())
    fig.add_trace(go.Treemap(labels = df["Brand"],
                             parents = ["" for element in df["Brand"].to_numpy()],
                             values = df["YTD_2025_units"].to_numpy(),
                             root_color = "red",
                             #textinfo = "label+percen root",
                             texttemplate = "%{label}: %{value}%",
                             #textinfo = "value",
                             marker = dict(colorscale = "Balance",
                                           colorbar = dict(title = "", orientation = "h"))))
    

def main():
    df = pd.read_csv("tree_map_data.csv")
    fig = create_figure("YTD Market Share %")
    convert_to_percentage_contribution(df)
    df.to_csv("percents.csv")
    plot(df, fig)
    touch_up(fig)
    fig.show(renderer = "browser")
    #fig.write_image("Tree_map.png", width = 950, height = 800, scale = 6)
    

main()