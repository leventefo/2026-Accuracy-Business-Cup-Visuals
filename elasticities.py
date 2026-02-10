import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import requests
import statsmodels.api as sm
import datetime as dt

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
        #print(data["value"])
        try:
            data["value"] = data["value"].astype(float)
        except:
            pass
            print("ValueError: likely percent")
        data.drop(columns = ["realtime_start", "realtime_end"], axis =1, inplace = True)
        data.rename(columns = {"value":series_id}, inplace=True)

    return data


def recursive_df_merge(lst):
    if len(lst) == 1:
        return lst[0]
    else:
        lst[1] = lst[0].merge(right=lst[1], how = "left", on = "date")
        lst.pop(0)
        return recursive_df_merge(lst)
    

def calculate_YoY_change(df):
    cols = df.columns.copy()
    #print(cols[:])
    for col in cols:
        if col not in ["FEDFUNDS", "UNRATE"]:
            df[col + str(" YoY Change")] = np.nan
            for date, val in zip(df.index, df[col].values):
                try:
                    df.loc[date + pd.offsets.DateOffset(years=1), col + " YoY Change"] = (df.loc[date + pd.offsets.DateOffset(years=1), col] - val)
                except KeyError:
                    pass
                #print("Key error: final date likely reached.")


    cols = list(cols.to_numpy())
    cols.remove("FEDFUNDS")
    cols.remove("UNRATE")
    #print(cols)

    #cols = cols.to_numpy().remove("FEDFUNDS")
    df.drop(columns = cols, inplace = True)
    df.dropna(inplace= True)

    return df



def create_relative_price(df):

    df["CPIAUCSL"] = pd.to_numeric(df["CPIAUCSL"], errors = "coerce")

    df.fillna(method = "ffill", inplace=True)

    df["Relative Price"] = df["CUSR0000SETA01"] - df["CPIAUCSL"]

    return df
    # print(df)
    #df.to_csv("log_changes.csv")
    #print(df)
    #return df.drop(columns = cols, inplace = True).dropna(inplace = True)

    #print(df)


def format(df, col):
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df.fillna(method = "ffill", inplace=True)
    #print(df)
    return df


def create_figure(title):
    fig = make_subplots(rows = 1, cols = 2, shared_yaxes=True,
                        subplot_titles=("Pre-Covid (2012 - 2019)", "Post-Covid (2021-Present)"),
                        horizontal_spacing=0.07).update_layout(template ="plotly_white", title = title, title_x = 0.5, title_y = 0.94, title_font_weight = 600)
    fig.update_layout(width = 1500, height = 450)

    return fig

def touch_up(fig):
    fig.update_layout(margin=dict(t=50, b=120, l=200, r=60))
    fig.update_layout(margin = dict(autoexpand = False))
    fig.update_layout(paper_bgcolor = "#F3F4F6")
    fig.update_layout(plot_bgcolor = "#F3F4F6")
    fig.update_layout(font_family = "Georgia", font_weight = 600, font_size = 18)
    #fig.update_layout(xaxis_title = "Coefficient")
    fig.update_yaxes(tickfont = dict(size = 13, weight = 600))
    fig.update_xaxes(title_font = dict(size = 15), col = 1, row = 1, title_text = "Coefficient")
    fig.update_xaxes(title_font = dict(size = 15), col = 2, row = 1, title_text = "Coefficient")
    fig.update_layout(legend4 = dict(orientation = "h", y = -0.2, x = 0.3))
    fig.update_layout(title_font = dict(size = 20))


def coefficient_plot(res, fig, loc, leg_show_primary):
    variables = list(res.params.to_dict().keys())
    coefficients = res.params
    pval = res.pvalues
    ci = res.conf_int()
    ci_low = ci[0]
    ci_high = ci[1]
    sig_flag = pval < 0.05

    df = pd.DataFrame(index = variables)

    df["term"] = variables
    df["coef"] = coefficients
    df["ci_low"] = ci_low
    df["ci high"] = ci_high

    df["err_left"] = df["coef"] - df["ci_low"]
    df["err_right"] = df["ci high"] - df["coef"]
    df["pval"] = pval

    df.drop(["const"], axis = 0, inplace = True)


    sig_count = 0
    insig_count = 0

    for index, row in df.iterrows():
        if row["pval"] < 0.05:
            name = "Significant"
            color = "#9C2225"

            if sig_count == 0:
                leg_add = "legend1"
                leg_show = True
            else:
                leg_add = "legend2"
                leg_show = False
            sig_count += 1
        else:
            name = "Not significant"
            color = "#012F68"

            if insig_count == 0:
                leg_add = "legend1"
                leg_show = True
            else:
                leg_add = "legend2"
                leg_show = False
            insig_count += 1

        
        if leg_show_primary != None:
            leg_add = "legend3"
            leg_show = False

        #print(loc, leg_show, leg_add)


        fig.add_trace(go.Scatter(x=[row["coef"]], y=row[["term"]],
                             mode = "markers",
                             error_x = dict(type="data",
                                            symmetric = False,
                                            array = [row["err_left"]],
                                            arrayminus = [row["err_right"]],
                                            width = 6,
                                            thickness = 3),
                            showlegend = False,
                            line = dict(width = 10,
                                        color = color),
                                        name = name,
                                        legend = "legend2"),
                                        row = 1,
                                        col = loc)
        

    fig.add_trace(go.Scatter(x=[None], y = [None],
                                 mode = "markers",
                                 name = "Significant",
                                 marker = dict(color = "#9C2225"),
                                 legend = "legend4",
                                 showlegend=leg_show_primary,
                                 ), row = 1,
                                 col = 1)
        
    fig.add_trace(go.Scatter(x=[None], y = [None],
                                 mode = "markers",
                                 name = "Not significant",
                                 marker = dict(color = "#012F68"),
                                 legend = "legend4",
                                 showlegend=leg_show_primary,
                                 ), row = 1,
                                 col =1)


    # colors = []
    # sig_rows = []
    # ins_sig_rows = []

    # for index, row in df.iterrows():
    #     if row["pval"] < 0.05:
    #         sig_rows.append(row)
    #     else:
    #         ins_sig_rows.append(row)


    # fig.add_trace(go.Scatter(x=[element["coef"] for element in sig_rows], y=[element["term"] for element in sig_rows],
    #                          mode = "markers",
    #                          error_x = dict(type="data",
    #                                         symmetric = False,
    #                                         array = [element["err_left"] for element in sig_rows],
    #                                         arrayminus = [element["err_right"] for element in sig_rows],
    #                                         width = 6,
    #                                         thickness = 3),
    #                         showlegend = leg_show,
    #                         line = dict(width = 10,
    #                                     color = "#9C2225"),
    #                                     name = "Significant",
    #                                     legend = leg_add),
    #                                     row = 1,
    #                                     col = loc)

    # fig.add_trace(go.Scatter(x=[element["coef"] for element in ins_sig_rows], y=[element["term"] for element in ins_sig_rows],
    #                          mode = "markers",
    #                          error_x = dict(type="data",
    #                                         symmetric = False,
    #                                         array = [element["err_left"] for element in ins_sig_rows],
    #                                         arrayminus = [element["err_right"] for element in ins_sig_rows],
    #                                         width = 6,
    #                                         thickness = 3),
    #                         showlegend = leg_show,
    #                         line = dict(width = 10,
    #                                     color = "#012F68"),
    #                                     name = "Not significant",
    #                                     legend = leg_add),
    #                                     row = 1,
    #                                     col = loc)

    

    fig.add_vline(x=0,
                        line = dict(width = 3, dash = "dash"),
                        opacity = 0.5,
                        annotation_text = "Null",
                        annotation_position = "top",
                        annotation_font = dict(size = 13),
                        row = 1,
                        col = loc)

    fig.update_yaxes(autorange = "reversed")

    touch_up(fig)
    

    
def main():
    base_url = "https://api.stlouisfed.org/fred/"
    end_point = "series/observations"
    api_key = read_api_key("fred_key.txt")
    file_type = "json"
    
    df_light_vehicle_sales = pull_data(base_url, end_point, "ALTSALES", api_key, file_type, "1999-01-01", "2025-12-31", "m", "log")
    df_new_vehicle_CPI = pull_data(base_url, end_point, "CUSR0000SETA01", api_key, file_type, "1999-01-01", "2025-12-31", "m", "log")
    df_real_disposable_personal_income = pull_data(base_url, end_point, "DSPIC96", api_key, file_type, "1999-01-01", "2025-12-31", "m", "log")
    df_all_items_CPI = pull_data(base_url, end_point, "CPIAUCSL", api_key, file_type, "1999-01-01", "2025-12-31", "m", "log")
    df_FEDFUNDS = pull_data(base_url, end_point, "FEDFUNDS", api_key, file_type, "1999-01-01", "2025-12-31", "m", "")
    df_unemployment_rate =  format(pull_data(base_url, end_point, "UNRATE", api_key, file_type, "1999-01-01", "2025-12-31", "m", ""), "UNRATE")
    df_used_vehicle_CPI = pull_data(base_url, end_point, "CUSR0000SETA02", api_key, file_type, "1999-01-01", "2025-12-31", "m", "log")
    


    df_light_vehicle_sales_post_covid = pull_data(base_url, end_point, "ALTSALES", api_key, file_type, "1999-01-01", "2025-12-31", "m", "log")
    df_new_vehicle_CPI_post_covid = pull_data(base_url, end_point, "CUSR0000SETA01", api_key, file_type, "1999-01-01", "2025-12-31", "m", "log")
    df_real_disposable_personal_income_post_covid = pull_data(base_url, end_point, "DSPIC96", api_key, file_type, "1999-01-01", "2025-12-31", "m", "log")
    df_all_items_CPI_post_covid = pull_data(base_url, end_point, "CPIAUCSL", api_key, file_type, "1999-01-01", "2025-12-31", "m", "log")
    df_FEDFUNDS_post_covid = pull_data(base_url, end_point, "FEDFUNDS", api_key, file_type, "1999-01-01", "2025-12-31", "m", "")
    df_unemployment_rate_post_covid = format(pull_data(base_url, end_point, "UNRATE", api_key, file_type, "1999-01-01", "2025-12-31", "m", ""), "UNRATE")
    df_used_vehicle_CPI_post_covid = pull_data(base_url, end_point, "CUSR0000SETA02", api_key, file_type, "1999-01-01", "2025-12-31", "m", "log")


    df_supply_tightness = pd.read_csv("gscpi_data.csv")
    df_supply_tightness = df_supply_tightness[["Date", "GSCPI"]]
    df_supply_tightness.dropna(inplace = True)
    df_supply_tightness.set_index("Date", inplace=True)
    df_supply_tightness.index.rename("date", inplace = True)
    df_supply_tightness.index = pd.to_datetime(df_supply_tightness.index)
    df_supply_tightness.index = df_supply_tightness.index.map(lambda x: pd.offsets.MonthBegin().rollback(x))
    #print(df_supply_tightness.index)
    #df_supply_tightness.rename(index = {"Date": "date"}, inplace = True)
    #print(df_supply_tightness)
    df_combined = recursive_df_merge([df_light_vehicle_sales, 
                                      df_new_vehicle_CPI, 
                                      df_real_disposable_personal_income, 
                                      df_all_items_CPI,
                                      df_supply_tightness,
                                      df_FEDFUNDS,
                                      df_unemployment_rate,
                                      df_used_vehicle_CPI])
    
    df_combined.dropna(inplace = True)

    df_combined = create_relative_price(df_combined)

    df_combined = calculate_YoY_change(df_combined)

    df_combined_post_covid = recursive_df_merge([df_light_vehicle_sales_post_covid, 
                                                 df_new_vehicle_CPI_post_covid, 
                                                 df_real_disposable_personal_income_post_covid, 
                                                 df_all_items_CPI_post_covid,
                                                 df_supply_tightness, 
                                                 df_FEDFUNDS_post_covid, 
                                                 df_unemployment_rate_post_covid,
                                                 df_used_vehicle_CPI_post_covid])
    

    df_combined_post_covid.dropna(inplace = True)

    df_combined_post_covid = create_relative_price(df_combined_post_covid)

    df_combined_post_covid = calculate_YoY_change(df_combined_post_covid)


    df_restricted_post_covid = df_combined_post_covid[df_combined_post_covid.index >= "2021-07-01"]
    #df_combined.to_csv("everything.csv")

    #print(df_combined.columns)

    df_restricted_post_covid.rename(columns = {"Relative Price YoY Change": "Rel. vehicle price (YoY)",
                                    "DSPIC96 YoY Change": "Real income (YoY)",
                                    "FEDFUNDS": "Policy rate",
                                    "GSCPI YoY Change": "GSCPI (YoY)",
                                    "CUSR0000SETA01 YoY Change": "New vehicle price (YoY)"},
                                    inplace = True)
    

    y_post_covid =  df_restricted_post_covid["ALTSALES YoY Change"]

    x_post_covid = df_restricted_post_covid[["New vehicle price (YoY)", 
                     "Real income (YoY)", 
                     "Policy rate",
                     "GSCPI (YoY)"]]
    
    x_post_covid = sm.add_constant(x_post_covid)

    results_post_covid = sm.OLS(y_post_covid, x_post_covid).fit()


    df_restricted = df_combined[(df_combined.index.year >= 2012) & (df_combined.index <= "2019-12-01")]

    #print(df_restricted)

    df_restricted.rename(columns = {"Relative Price YoY Change": "Rel. vehicle price (YoY)",
                                    "DSPIC96 YoY Change": "Real income (YoY)",
                                    "FEDFUNDS": "Policy rate",
                                    "GSCPI YoY Change": "GSCPI (YoY)",
                                    "CUSR0000SETA01 YoY Change": "New vehicle price (YoY)"},
                                    inplace = True)
    

    #print(df_restricted)

    y = df_restricted["ALTSALES YoY Change"]


    print(df_restricted.columns)

    x = df_restricted[["New vehicle price (YoY)", 
                     "Real income (YoY)", 
                     "Policy rate",
                     "GSCPI (YoY)"]]
    
    

    x = sm.add_constant(x)

    results = sm.OLS(y, x).fit()

    
    fig = create_figure("")


    with open("pre_covid_regression_summary.csv", "w") as f:
        f.write(results.summary().as_csv())


    with open("post_covid_regression_summary.csv", "w") as f:
        f.write(results_post_covid.summary().as_csv())


    

    

    # coefficient_plot(results, fig, 1, False)
    # coefficient_plot(results_post_covid, fig, 2, True)


    

    #fig.show(renderer  = "browser")
    #fig.write_image("Regresssion_analysis2.png", width = 1800, height = 450, scale = 6)
    #print(results.summary())


    #print(df_combined)

    



    #

    

    #df_combined.to_csv("everything_YoY.csv")





    #df_combined.to_csv("everything.csv")
    
    #df_combined.to_csv("everything.csv")
    
    #print(df_combined)
    #print(df_supply_tightness)

    #df_combined = recursive_df_merge([df_light_vehicle_sales, df_new_vehicle_CPI, df_real_disposable_personal_income, df_all_items_CPI, df_FEDFUNDS, df_supply_tightness])

    #print(df_combined)



    #df_combined = recursive_df_merge([df_light_vehicle_sales, df_new_vehicle_CPI, df_real_disposable_personal_income])
    #df_combined = calculate_YoY_log_change(df_combined.copy())

    # ALTSALES_YoY_Log_Change = df_combined[df_combined.columns[0]].to_numpy()
    # CUSR0000SETA01_YoY_Log_Change = df_combined[df_combined.columns[1]].to_numpy()
    # CUSR0000SETA01_YoY_Log_Change = sm.add_constant(CUSR0000SETA01_YoY_Log_Change)


    #result = sm.OLS(ALTSALES_YoY_Log_Change, CUSR0000SETA01_YoY_Log_Change).fit()
    #print(result.summary())
    #print(df_combined)
    #print(df_combined)
    # df_light_vehicle_sales.to_csv("light_vehicle_sales.csv")
    # df_new_vehicle_CPI.to_csv("new_vehicle_CPI.csv")
    # df_real_disposable_personal_income.to_csv("real_disposable_personal_income.csv")

    #fig.show(renderer = "browser")
    #fig.write_image("Light_Weight_Vehicle_Sales_Autos_and_Light_Trucks_with_value.png", width = 800, height = 375, scale = 6)
main()