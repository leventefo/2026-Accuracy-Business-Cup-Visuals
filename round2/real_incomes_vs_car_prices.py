import plotly.graph_objects as go
import pandas as pd




def pull_data(file):
    df_data = pd.read_csv(file)
    df_data["Date"] = pd.to_datetime(df_data['Date'].str.split(' ').apply(lambda x: ''.join(x[::-1])))
    df_data.set_index("Date", inplace = True)
    
    print(df_data)

def main():
    df_real_income = pull_data("Quarterly change in households disposable income.csv")
    #Format and tranform 



main()
