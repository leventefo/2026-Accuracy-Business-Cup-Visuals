import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests



def format_and_get_data(file_name):

    if file_name == "automotive_trends.csv":

        df = pd.read_csv(file_name)
        df_pivot = pd.pivot_table(df, values = "Production Share",
                                                    index = "Model Year",
                                                    columns = "Vehicle Type",
                                                    aggfunc = "sum")
        
        df_pivot = df_pivot.iloc[:-1]
        df_pivot.index = pd.to_datetime(df_pivot.index)
        df_pivot = df_pivot.apply(pd.to_numeric)
        df_pivot = df_pivot.apply(lambda x: x*100, axis = 1)
        df_pivot = df_pivot[df_pivot.index >= "2000-January"]

        #df_pivot = df.iloc[:-8]
        #df_pivot.index = pd.to_datetime(df_pivot.index)
        
        #print(df_pivot.tail())
        #print(df_pivot)

        return df_pivot
    
    else:
        df = pd.read_csv(file_name)
        df_pivot = pd.pivot_table(df, columns = "Fuel Code",
                                  index = "Model Year",
                                  aggfunc = "count")
        

        
        #df_pivot.index = pd.to_datetime(df_pivot.index)
        df_pivot.index = df_pivot.index.map(lambda x: str(x))
        df_pivot.index = pd.to_datetime(df_pivot.index)
        df_pivot = df_pivot[df_pivot.index >= "2000-January"]
        #print(df_pivot)


        return df_pivot["Vehicle ID"]

def create_figure(title):
    fig = make_subplots(rows = 1, cols = 2, subplot_titles = ["Vehicle type", "Fuel type"],
                        shared_yaxes = True,
                        horizontal_spacing = 0.05).update_layout(template ="plotly_white", title = title, title_x = 0.5, title_y = 0.92, title_font_weight = 600)
    fig.update_layout(width = 1460, height = 600)
    #fig.update_yaxes(range = [-0.75748, 17.338017], row = 1, col = 1)
    #fig.update_yaxes(range = [-1.176565, 17.338017], row = 2, col = 1)
    return fig



def plot_bar(df, fig, names: list, colors, loc, show_leg, leg_name):
    counter = 0
    for col in df.columns[0:]:
        #print(names[counter])
        fig.add_trace(go.Bar(name = names[counter], x=df.index, 
                             y = df[col], marker_color = colors[counter],
                             legendgroup="group" + str(loc) + str(counter), showlegend=show_leg, legend = leg_name),
                             row = 1, col = loc)
        counter +=1

    fig.update_layout(barmode = "relative")



def create_other(df):
    df.loc[:,"Other"] = df[["LPG", "H2", "CNG_GSLN", "LPG_GSLN", "M85_GSLN"]].sum(axis = 1)
    df.drop(columns = ["LPG", "H2", "CNG_GSLN", "LPG_GSLN", "M85_GSLN"], inplace = True)
    return df
    #df.to_csv("fuel_split_with_other.csv")


def convert_to_percentage_contribution(df):
    df = df.fillna(0)
    counter = 0
    for row in df.values:
        row_sum = row.sum()
        update_lst = []
        for value in row:
            p_value = (value/row_sum) *100
            update_lst.append(p_value)
        df.iloc[counter] = update_lst
        counter +=1

    return df



def touch_up(fig):
    
    fig.update_layout(margin=dict(t=60, b=80, l=90, r=80))
    fig.update_layout(font_family = "Georgia", font_weight = 600, font_size = 16)
    fig.update_yaxes(title_text = "% Share", row = 1, col = 1)
    fig.update_yaxes(title_text = "", row = 1, col = 2)
    fig.update_layout(paper_bgcolor = "#F3F4F6")
    fig.update_layout(plot_bgcolor = "#F3F4F6")
    fig.update_layout(legend1 = dict(orientation = "h", x = 0.005,
                                     y = -0.06,
                                     font = dict(size = 13)))
    
    fig.update_layout(legend2 = dict(orientation = "h", x = 0.525,
                                     y = -0.06,
                                     font = dict(size = 13)))

    
    fig.update_yaxes(ticksuffix = " ")
    fig["layout"]["annotations"][0]["font_size"] = 18
    fig["layout"]["annotations"][1]["font_size"] = 18


def main():
    df_automotive_trends_pivot = format_and_get_data("automotive_trends.csv")
    df_automotive_trends_pivot.drop(columns = ["All", "All Car", "All Truck"], inplace = True)
    df_light_duty_vehicles_fuel_split = format_and_get_data("light-duty-vehicles-2026-02-02.csv")
    #df_light_duty_vehicles_fuel_split.to_csv("fuel_split.csv")
    #print(df_light_duty_vehicles_fuel_split)
    #print(df_light_duty_vehicles_fuel_split)
    #print(df_automotive_trends_pivot)
    df_automotive_trends_pivot = df_automotive_trends_pivot[["Truck SUV", 
                                                             "Sedan/Wagon", 
                                                             "Pickup",
                                                             "Minivan/Van",
                                                             "Car SUV"
                                                             ]]
    
    #print(df_automotive_trends_pivot)
    fig = create_figure("")
    plot_bar(df_automotive_trends_pivot, fig, ["Truck SUV", 
                                                             "Sedan/Wagon", 
                                                             "Pickup",
                                                             "Minivan/Van",
                                                             "Car SUV"
                                                             ], 
             ["#012F68", "#1B4F9A", "#2778C0", "#5DA9E6", "#C8E0F5"], 
             1, True, "legend1")
    
    df_light_duty_vehicles_fuel_split_simplied_p_contribtuion = convert_to_percentage_contribution(create_other(df_light_duty_vehicles_fuel_split))
    #df_light_duty_vehicles_fuel_split_simplied_p_contribtuion.to_csv("final.csv")

    df_light_duty_vehicles_fuel_split_simplied_p_contribtuion = df_light_duty_vehicles_fuel_split_simplied_p_contribtuion[["E85_GSLN", "CNG", "BD", "Other", "ELEC", "PHEV", "HYBR"]]
    
    plot_bar(df_light_duty_vehicles_fuel_split_simplied_p_contribtuion, fig, df_light_duty_vehicles_fuel_split_simplied_p_contribtuion.columns,
             ["#012F68", "#1B4F9A", "#2778C0", "#1F8A70", "#C99700", "#D06B00", "#6A4C93"],
             2, True, "legend2")
    
    touch_up(fig)
    
    fig.write_image("Light_weight_vehicle_mix2.png", width = 1460, height = 600, scale = 6)
    
    
    
    #fig.show(renderer = "browser")


main()