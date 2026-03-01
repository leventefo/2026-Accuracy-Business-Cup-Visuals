import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests

def read_api_key(file):
    with open(file, "r") as f:
        key = f.readline()

    return key

def pull_data(base_url, end_point, series_id, api_key, file_type, observation_start, observation_end, frequency, units):
    params = {
        "series_id" : series_id,
        "api_key" : api_key,
        "file_type" : file_type,
        "observation_start" : observation_start,
        "observation_end" : observation_end,
        "frequency" : frequency,
        "units" : units
    }
    response = requests.get(base_url + end_point, params = params)

    if response.status_code == 200:
        res_data = response.json()
        data = pd.DataFrame(res_data["observations"])
        data["date"] = pd.to_datetime(data["date"])
        data.set_index("date", inplace = True)
        data["value"] = data["value"].astype(float)
        data.drop(columns = ["realtime_start", "realtime_end"], axis =1, inplace = True)

    return data



def calculate_average_between_two_dates(df, start_date, end_date):
    mask = (df.index >= pd.Timestamp(start_date)) & (df.index <= pd.Timestamp(end_date))
    #print(mask)
    df_restricted = df.loc[mask]
    return (df_restricted["value"].sum() / df_restricted["value"].count())


    #return (restricted_df.sum() / restricted_df["value"].count())


def create_figure(title):
    fig = make_subplots(specs=[[{"secondary_y": True}]]).update_layout(template ="plotly_white", title = title, title_x = 0.5, title_y = 0.94, title_font_weight = 600)
    fig.update_layout(width = 800, height = 375)
    fig.update_xaxes(range=[pd.Timestamp("2019-01-01"), pd.Timestamp("2026-01-01")])
    #fig.update_yaxes(range = [miny, maxy])
    return fig



def plot(df, line_width, fig, color, name, col, line_type = None, secondary_y = "False"):
    fig.add_trace(go.Scatter(x=df.index, y=df[col], 
                             line = dict(width = line_width, color = color, dash = line_type),
                             name = name, showlegend=True),
                             secondary_y = secondary_y)
    


def legend_setting(fig):
    fig.update_layout(legend = dict(orientation = "h", y = -0.2, x = 0.02))


def rolling_mean(df, window):
    df_rolling = df
    df_rolling["value"] = df_rolling["value"].rolling(window, center = False).mean()
    return df_rolling
    


def touch_up(fig):
    legend_setting(fig)
    fig.update_layout(margin=dict(t=90, b=80, l=80, r=60))
    fig.update_layout(margin = dict(autoexpand = False))
    fig.update_layout(paper_bgcolor = "#F3F4F6")
    fig.update_layout(plot_bgcolor = "#F3F4F6")
    fig.update_layout(font_family = "Georgia", font_weight = 600, font_size = 18)
    fig.update_layout(yaxis_title = "M units")
    fig.update_yaxes(tickprefix = " ", title = "B dollars", secondary_y=True)
    fig.update_yaxes(ticksuffix = " ", secondary_y=False)
    


def main():
    base_url = "https://api.stlouisfed.org/fred/"
    end_point = "series/observations"
    api_key = read_api_key("fred_key.txt")
    file_type = "json"
    df_light_vehicle_sales = pull_data(base_url, end_point, "ALTSALES", api_key, file_type, "2019-01-01", "2025-12-31", "m", "")
    df_light_vehicle_sales_1_year_earlier = pull_data(base_url, end_point, "ALTSALES", api_key, file_type, "2010-01-01", "2025-12-31", "m", "")
    df_new_motor_vehicle_sales = pull_data(base_url, end_point, "AB67RC1Q027SBEA", api_key, file_type, "2018-01-01", "2025-12-31", "q", "")
    
    df_copy = df_light_vehicle_sales_1_year_earlier.copy()
    fig = create_figure("Light Weight Vehicle Sales: Autos and Light Trucks")
    plot(df_light_vehicle_sales, 4, fig, "#01346C", "Volume", "value", None, False)
    df_new_motor_vehicle_sales_moving_average = rolling_mean(df_new_motor_vehicle_sales.copy(), 3)
    #print(df_new_motor_vehicle_sales)
    plot(df_new_motor_vehicle_sales, 4, fig, "#215F9A", "Value", "value", None, True)
    
    df_light_vehicle_sales_moving_average = rolling_mean(df_light_vehicle_sales_1_year_earlier, 12)
    #print(df_copy)
    #print(df_copy.loc[df_copy.index, pd.Timestamp("2015-01-01")])
    plot(df_light_vehicle_sales_moving_average, 4, fig, "#4E95D9", "12M MA Volume", "value", "dot", False)
    average_2015_2019 = calculate_average_between_two_dates(df_copy, "2015-01-01", "2019-01-01")
    #print(average_2015_2019)
    #average_2015_2019 = 17.3 #must debug
    dates = df_light_vehicle_sales.index.to_numpy()
    h_line_dict = {"date" : dates, "value" : [average_2015_2019 for element in dates]}
    h_line_df = pd.DataFrame(data=h_line_dict)
    h_line_df.set_index("date", inplace=True)
    plot(h_line_df, 4, fig, "#A6CAEC", "pre-Covid AVG", "value", "dash", False)
    fig.add_vrect(x0 = "2020-02-01", x1 = "2020-06-01", annotation_text = "Recession", annotation_position = "top left",
                  fillcolor = "grey", opacity = 0.25, line_width = 0, secondary_y = False)
    
    fig["layout"]["annotations"][0]["font_size"] = 12
    
    touch_up(fig)
    #fig.show(renderer = "browser")
    fig.write_image("Light_Weight_Vehicle_Sales_Autos_and_Light_Trucks_with_value.png", width = 800, height = 375, scale = 6)
    

main()