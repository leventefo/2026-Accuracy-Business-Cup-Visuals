import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np



def get_data(file):
    df = pd.read_csv(file)
    return df


def create_figure(title):
    fig = go.Figure().update_layout(template ="plotly_white", title = title, title_x = 0.5, title_y = 0.925, title_font_weight = 600)
    fig.update_layout(width = 1500, height = 600)

    return fig



def touch_up(fig):

    fig.update_layout(margin=dict(t=100, b=80, l=80, r=60))
    fig.update_layout(font_family = "Georgia", font_weight = 600, font_size = 16)
    # fig.update_yaxes(title_text = "pp (YoY)", row = 1, col = 1)
    # fig.update_yaxes(title_text = "pp (YoY)", row = 2, col = 1)
    fig.update_layout(paper_bgcolor = "#F3F4F6")
    fig.update_layout(plot_bgcolor = "#F3F4F6")
    fig.update_traces(mode='markers', marker=dict(sizemode='area', line_width=2,
                                                  sizeref = 0.02 ))
    
    fig.update_layout(
    title=dict(text='Tariff exposure vs market relevance by OEM',
               subtitle = dict(text = "Bubble size = # carlines")),
    xaxis=dict(
        title=dict(text='Average % of imported parts'),
        gridcolor='white',
        type='log',
        gridwidth=2,
    ),
    yaxis=dict(
        title=dict(text='Market share (%)'),
        gridcolor='white',
        gridwidth=2,
    ),
    paper_bgcolor='#F3F4F6',
    plot_bgcolor='#F3F4F6',
)
    fig.update_layout(legend = dict(orientation = "h", x = 0.13, y = -0.2, 
                                    font = dict(size = 14)))
    fig.update_xaxes(range = [0,110], type = "linear")


    fig.add_vline(x=70, line_width = 3, line_dash = "dash", line_color = "#01346C", opacity = 0.5)
    fig.add_hline(y = 5, line_width = 3, line_dash = "dash", line_color = "#01346C", opacity = 0.5)


    fig.add_annotation(x=100, y=14,
            text="High market share, high % of imported parts",
            showarrow=False,
            font = dict(color = "#01346C", size = 12))
    
    fig.add_annotation(x=15, y=14,
            text="High market share, low % of imported parts",
            showarrow=False,
            font = dict(color = "#01346C", size = 12))
    
    fig.add_annotation(x=100, y=-1,
            text="Low market share, high % of imported parts",
            showarrow=False,
            font = dict(color = "#01346C", size = 12))
    
    fig.add_annotation(x=15, y=-1,
            text="Low market share, low % of imported parts",
            showarrow=False,
            font = dict(color = "#01346C", size = 12))


def plot(fig, df):

    df.set_index("brand", inplace = True)
    df["brand"] = df.index

    counter1, counter2 = 0, 0

    print([i for i in range(26)])

    for index, row in df.iterrows():



        print(row["brand"])
        fig.add_trace(go.Scatter(x=[row["imported_parts_content_proxy_avg_pct"]],
                                 legendgroup = "leg_group" + str(counter2),
                                 y=[row["market_share_pct"]],
                                 marker_size = row["aala_carlines_count"],
                                 name = row["brand"],
                                 marker = dict(showscale = False)))
        
        counter1 +=1

        if counter1 % 3 == 0:
            counter2 += 1
    # fig.add_trace(go.Scatter(
    #     x = df["imported_parts_content_proxy_avg_pct"],
    #     y = df["market_share_pct"],
    #     marker_size = df["aala_carlines_count"]
    # ))


def main():
    df = get_data("market_share_vs_imported_parts_MY2025_AALA_v2.csv")
    fig = create_figure("Temp")
    plot(fig, df)
    touch_up(fig)
    #fig.show(renderer = "browser")
    fig.write_image("tariff_exposure.png", width = 1500, height = 600, scale = 6)
    #print(df)

main()