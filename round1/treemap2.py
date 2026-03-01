import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests


def get_data():
    pass


def create_figure(title):
    fig = make_subplots(specs = [[{"type": "domain"}]]).update_layout(template ="plotly_white", title = title, title_x = 0.5, title_y = 0.96, title_font_weight = 600,
                                                                      title_font_size = 45)
    fig.update_layout(width = 800, height = 800)
    #fig.update_xaxes(range=[pd.Timestamp("2019-01-01"), pd.Timestamp("2026-01-01")])
    #fig.update_yaxes(range = [miny, maxy])
    return fig




def touch_up(fig):
    
    fig.update_layout(margin=dict(t=180, b=20, l=20, r=20))
    #fig.update_layout(font_family = "Georgia", font_weight = 600, font_size = 10)
    fig.update_layout(title = dict(font = dict(family = "Georgia", weight = 600)))
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
                             values = df["Percentage"].to_numpy(),
                             #textinfo = "label+percen root",
                             texttemplate = "%{label}: %{value}%",
                             insidetextfont = dict(size = 40, family = "Georgia", weight = 600),
                             #textinfo = "value",
                             marker = dict(colorscale = "Blues",
                                           colorbar = dict(title = "", orientation = "h",
                                                           tickfont = dict(size = 30, family = 'Georgia',
                                                                           weight = "bold")))))
    

def main():
    df = pd.read_csv("hybrid_registrations_share_aug_2025_cytd.csv")
    fig = create_figure("CYTD Market Share %")
    #convert_to_percentage_contribution(df)
    #df.to_csv("percents.csv")
    plot(df, fig)
    touch_up(fig)
    #fig.show(renderer = "browser")
    fig.write_image("Tree_map2.png", width = 800, height = 800, scale = 6)
    

main()