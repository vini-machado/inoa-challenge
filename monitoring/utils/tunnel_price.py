import pandas as pd
from ..models import UserStock
from warnings import filterwarnings

filterwarnings('ignore')

class TunnelPrice:
    def __init__(self, current_high_low: pd.DataFrame) -> None:
        self.userstocks   = UserStock
        self.current_high_low = current_high_low

    @property
    def userstock_df(self) -> pd.DataFrame:
        user_stocks = self.userstocks.objects.all().values('user__email', 'stock__ticker', 'max_price', 'min_price')

        df = pd.DataFrame(user_stocks, columns=['user__email', 'stock__ticker', 'max_price', 'min_price'])
        df.columns = ['email', 'Ticker', 'max_price', 'min_price']
        return df
    
    def __merge_userstock__current_high_low(self):
        return self.userstock_df.merge(self.current_high_low, how = 'left', on = 'Ticker')

    def __filter_tunnel_conditions(self):
        merged_data = self.__merge_userstock__current_high_low()

        conditions = (
            merged_data['High'].isna(),
            merged_data['Low'].isna(),
            merged_data['max_price'] == 0,
            merged_data['min_price'] == 0,
        )

        for condition in conditions:
            merged_data = merged_data.drop(merged_data[condition].index)

        return merged_data
    
    @property
    def data(self):
        return self.__filter_tunnel_conditions()

    @property
    def actions(self) -> pd.DataFrame:
        td = self.data.copy()
        td['action'] = '-'

        td.loc[td['High'] > td['max_price'], 'action'] = 'Sell'
        td.loc[td['Low'] < td['min_price'] , 'action'] = 'Buy'

        return td.loc[td['action'] != '-', ['email', 'Ticker', 'action']]