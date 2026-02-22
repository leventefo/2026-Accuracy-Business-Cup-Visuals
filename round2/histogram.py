import plotly.graph_objects as go
import plotly.express as px
from itertools import cycle
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots

class World:

    def __init__(self):
        self.values = self.simulate()

    def draw(self):
        representative_a_segment_vehicle_price = 19e3
        self.shareable_fixed_costs = np.random.triangular(0.5e9, 1.2e9, 2e9)
        self.volume = np.random.triangular(2e6, 3e6, 4e6)
        self.max_variable_saving = np.random.triangular(150, 350, 600)
        self.scale_speed = np.random.triangular(1.5, 3, 5)
        self.pass_through = np.random.triangular(0.4, 0.6, 0.7)
        significant_market_share_indicator = 0.40
        transition_sharpness = 40
        reference_share = 0.04
        market_share_value = np.random.beta(11,9)

        return representative_a_segment_vehicle_price, self.shareable_fixed_costs, self.volume, self.max_variable_saving, self.scale_speed, self.pass_through, significant_market_share_indicator, transition_sharpness, reference_share, market_share_value        
        
    def fixed_cost_activation(self, transition_sharpness, market_share, significant_market_share_indicator):
        grad = 1/(1+np.exp(-transition_sharpness*(market_share-significant_market_share_indicator)))
        return grad
    
    def economies_of_fixed_cost_aborption(self, grad, shareable_fixed_costs, volume, reference_share, market_share):
        fixed_cost_saving = grad * (shareable_fixed_costs/volume) * ((1/reference_share)-(1/(market_share+reference_share)))
        return fixed_cost_saving
    
    def variable_cost_savings(self, max_variable_saving, scale_speed, market_share):
        var_savings = max_variable_saving * (1-np.exp(-scale_speed*market_share)) 
        return var_savings

    def simulate(self):
        
        values = []

        for i in range(10000):

            representative_a_segment_vehicle_price, shareable_fixed_costs, volume, max_variable_saving, scale_speed, pass_through, significant_market_share_indicator, transition_sharpness, reference_share, market_share_value = self.draw()

            grad = self.fixed_cost_activation(transition_sharpness, market_share_value, significant_market_share_indicator)
            
            fixed_cost_saving = self.economies_of_fixed_cost_aborption(grad, shareable_fixed_costs, volume, reference_share, market_share_value)
            variable_cost_saving = self.variable_cost_savings(max_variable_saving, scale_speed, market_share_value)
            final_price = representative_a_segment_vehicle_price - pass_through*(fixed_cost_saving + variable_cost_saving)

            values.append(final_price)

        return values

class Plot:

    def __init__(self):
        data = World()
        self.values = data.values
        self.create_figure(fig_title = "", yaxis_title = "Frequency", xaxis_title= "5-year A-segment vehicle price (€)")


    def create_figure(self, fig_title, yaxis_title, xaxis_title):
        fig = make_subplots(rows = 2, shared_xaxes = True).update_layout(template ="plotly_white", title = fig_title, title_x = 0.5, title_y = 0.94, title_font_weight = 600)
        fig.update_layout(width = 1000, height = 500)
        fig.update_layout(font_family = "Georgia", font_weight = 600, font_size = 18)
        fig.update_layout(paper_bgcolor = "#F3F4F6")
        fig.update_layout(plot_bgcolor = "#F3F4F6")
        fig.update_yaxes(ticksuffix = " ", title = yaxis_title, title_standoff = 20)
        fig.update_layout(margin=dict(t=0, b=65, l=0, r=0), showlegend = False)
        fig.update_xaxes(title = xaxis_title, title_standoff = 20, row = 2)
        self.plot_data(fig, self.values)

    def plot_data(self, fig, dataset):
        fig.add_trace(go.Histogram(x = dataset, marker_color = "#2A3F5F"), row = 2, col = 1)
        fig.add_trace(go.Box(x=dataset, marker_color = "#8B0000"), row = 1, col = 1)
        fig.add_shape(type="line", x0=15000, y0=0, x1=15000, y1=400, line=dict(color="#ce1719", width=3, dash="dash"), row = 2, col = 1)
        fig.add_annotation(x=16200, y=380, text='"Affordable"', showarrow=False, font = dict(size = 16, color = "#ce1719"), row = 2, col = 1)
        fig.add_annotation(x=13500, y=190, text="72%", showarrow=False, font = dict(size = 37, color = "#ce1719"), row = 2, col = 1)
        fig.add_annotation(x=15700, y=80, text="28%", showarrow=False, font = dict(size = 18, color = "#ce1719"), row = 2, col = 1)

        #fig.add_vline(x=15000, line_dash="dash", line_color = "#ce1719", line_width = 3)
        fig.update_yaxes(title_text = None, showticklabels=False, row = 1, col = 1)
        fig.write_image("A-segment vehicle price simulation - Histogram.png", width = 1000, height = 500, scale = 6)
        #fig.show(renderer = "browser")


def main():
    plot = Plot()
main()