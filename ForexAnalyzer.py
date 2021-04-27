from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd

class ForexAnalyzer:

    def __init__(self, forex_pair):
    
        self._forex_pair = forex_pair

        self._time_style = {
            'Minute_1' : mt5.TIMEFRAME_M1,
            'Hour_1': mt5.TIMEFRAME_H1,
            'Day_1': mt5.TIMEFRAME_D1
        }

        self._start_mt5()

    def __del__(self):
        mt5.shutdown()

    def _start_mt5(self):
        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()

    def get_current_time(self):
        return datetime.today()

    def _find_minutes_elapsed(self):

        self._start_mt5()

        current = self.get_current_time()
        start_day = datetime(current.year, current.month, current.day)

        time_delta = (current - start_day)
    
        return int(time_delta.total_seconds()/60)

    def get_daily_stats(self, timeframe):

        rates = mt5.copy_rates_from(
            self._forex_pair, 
            self._time_style[timeframe], 
            self.get_current_time(), 
            self._find_minutes_elapsed()
        )

        rates_frame = pd.DataFrame(rates)
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

        return rates_frame.copy()

    def get_d1_stats(self, timeframe):

        d1_rates = mt5.copy_rates_from(
            self._forex_pair,
            self._time_style[timeframe],
            self.get_current_time(),
            1
        )

        stats_dict = pd.DataFrame(d1_rates).to_dict('records')[0]

        stats_dict['width_candlestick'] = int((stats_dict['high'] - stats_dict['low']) * 10**5)
        stats_dict['gap_open_high'] = int((stats_dict['high'] - stats_dict['open']) * 10**5)
        stats_dict['gap_open_low'] = int((stats_dict['open'] - stats_dict['low']) * 10**5)
        stats_dict['gap_open_close'] = int((stats_dict['open'] - stats_dict['close']) * 10**5)
        
        return stats_dict
