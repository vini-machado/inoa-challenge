import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


class StockChart:
    def __init__(self, stock_data: pd.DataFrame) -> None:
        self.stock_data = stock_data

    def __subplots(self):
        properties =  {
            'cols': 1, 
            'rows': 2, 
            'shared_xaxes': True, 
            'vertical_spacing': 0.04, 
            'subplot_titles': ('Prices', 'Volume'), 
            'row_width': [0.2, 0.7]
        }

        return make_subplots(**properties)

    def __candlestick_graph(self):
        return go.Candlestick(
                    x    = self.stock_data["Datetime"],
                    open = self.stock_data["Open"],
                    high = self.stock_data["High"],
                    low  = self.stock_data["Low"],
                    close= self.stock_data["Close"],
                    name = "Price"
                )
    def __volume_graph(self):
        return go.Bar(
                x = self.stock_data['Datetime'],
                y = self.stock_data['Volume'],
                showlegend=False
            )

    def __remove_closed_market_datetimes(self, fig):
        return fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]), #hide weekends
                    dict(bounds=[17, 10], pattern="hour"), #hide hours outside of 9am-5pm
                ]
            )      
    
    def __figure(self):
        candlestick = self.__candlestick_graph()
        volume      = self.__volume_graph()
        
        fig = self.__subplots()
        fig.add_trace(candlestick, row = 1, col = 1)
        fig.add_trace(volume,      row = 2, col = 1)

        fig = self.__remove_closed_market_datetimes(fig)

        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(height=800)

        return fig

    def plot(self):
        fig    = self.__figure()
        config = dict(displayModeBar=True, responsive=True)
        
        return fig.to_html(full_html=False, config=config) 