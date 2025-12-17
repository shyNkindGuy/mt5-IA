import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import logging

class MT5Client:
    def __init__(self, account, password, server):
        self.account = account
        self.password = password
        if not mt5.initialize(login=account, password=password, server=server):
            raise Exception(f"MT5 init failed: {mt5.last_error()}")
        
        def get_rates(self, symbol, timeframe, bars=1000):
            #datos para analisis fvg
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df[['time', 'open', 'high', 'low', 'close', 'tick_volume']]
        
        def calculate_spread(self, symbol):
            # calculo spread par riesgo
            symbol_info = mt5.symbiol_info(symbol)
            return (symbol_info.ask - symbol_info.bid) / symbol_info.point
                