import plotly.graph_objects as go
import pandas as pd
import numpy as np

class World:

    def __init__(self):
        representative_a_segment_vehicle_price = 19e3
        self.shareable_fixed_costs = np.random.triangular(0.5e9, 1.2e9, 2e9)
        self.volume = np.random.triangular(2e6, 3e6, 4e6)
        self.max_variable_saving = np.random.triangular(150, 350, 600)
        self.scale_speed = np.random.triangular(1.5, 3, 5)
        self.pass_through = np.random.triangular(0.5, 0.7, 0.85)
        significant_market_share_indicator = 0.40
        transition_sharpness = 40
        reference_share = 0.04
        market_share_steps = 2e5
        market_share_values = [100/market_share_steps*i for i in range(2001)]
        self.price_array = self.calculate_final_price(representative_a_segment_vehicle_price, self.shareable_fixed_costs, self.volume, self.max_variable_saving, self.scale_speed, self.pass_through, significant_market_share_indicator, transition_sharpness, reference_share, market_share_values)
        
    def fixed_cost_activation(self, transition_sharpness, market_share, significant_market_share_indicator):
        grad = 1/(1+np.exp(-transition_sharpness*(market_share-significant_market_share_indicator)))
        return grad
    
    def economies_of_fixed_cost_aborption(self, grad, shareable_fixed_costs, volume, reference_share, market_share):
        fixed_cost_saving = grad * (shareable_fixed_costs/volume) * ((1/reference_share)-(1/(market_share+reference_share)))
        return fixed_cost_saving
    
    def variable_cost_savings(self, max_variable_saving, scale_speed, market_share):
        var_savings = max_variable_saving * (1-np.exp(-scale_speed*market_share)) 
        return var_savings

    def calculate_final_price(self, representative_a_segment_vehicle_price, shareable_fixed_costs, volume, max_variable_saving, scale_speed, pass_through, significant_market_share_indicator, transition_sharpness, reference_share, market_share_values):
        
        final_price_array = []
        
        for market_share in market_share_values:

            grad = self.fixed_cost_activation(transition_sharpness, market_share, significant_market_share_indicator)
            
            fixed_cost_saving = self.economies_of_fixed_cost_aborption(grad, shareable_fixed_costs, volume, reference_share, market_share)
            variable_cost_saving = self.variable_cost_savings(max_variable_saving, scale_speed, market_share)
            final_price = representative_a_segment_vehicle_price - pass_through*(fixed_cost_saving + variable_cost_saving)

            final_price_array.append(final_price)

        return final_price_array
    

class Plot:

    def __init__(self, market_share_values):
        self.market_share_values = market_share_values
        self.data = [World() for i in range(300)]
        self.create_figure(fig_title = "Monte Carlo", yaxis_title = "A-segment vehicle price (€)", xaxis_title= "Joint Venture Market Share (%)")


    def create_figure(self, fig_title, yaxis_title, xaxis_title):
        fig = go.Figure().update_layout(template ="plotly_white", title = fig_title, title_x = 0.5, title_y = 0.94, title_font_weight = 600)
        fig.update_layout(width = 1000, height = 800)
        fig.update_yaxes(tickprefix = " ", title = yaxis_title)
        fig.update_xaxes(title = xaxis_title)
    
    



def main():
    market_share_steps = 2e5
    market_share_values = [100/market_share_steps*i for i in range(2001)]
    plot = Plot(market_share_values)



    #print(sim1.price_array[0])
    #print(sim1.price_array[-1])

    #np.savetxt("sim1.txt", sim1.price_array)

main()