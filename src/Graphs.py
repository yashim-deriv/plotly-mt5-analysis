from tapy import Indicators

import plotly.graph_objects as go
import numpy as np

class Graphs:

    def __init__(self, currency=None):
        self._currency = currency

    def update_currency(self, currency):
        self._currency = currency

        return None

    def _draw_hline(self, fig, y_val, line_dash, line_col, annotation=None):

        fig.add_hline(
            y=y_val,
            line_dash=line_dash,
            line_color=line_col,
            annotation_text=annotation or '',
            line_width=0.5
        )
        
        return None

    def _draw_vline(self, fig, x_val, line_dash, line_col):
        
        fig.add_vline(
            x=x_val,
            line_dash=line_dash,
            line_color=line_col,
            line_width=0.75
        )
        
        return None

    def plot_candlestick_today(self, data):

        info_text = f"Candlestick width: {data['width_candlestick']}<br>" + \
            f"Gap (High-Open): {data['gap_high_open']}<br>" + \
            f"Gap (Low-Open): {data['gap_open_low']}<br>" + \
            f"Current gap (Open-close): {data['gap_close_open']}"

        candlestick_today_fig = go.Figure(
            data=[
                go.Candlestick(
                    x=[data['time']],
                    open=[data['open']], 
                    high=[data['high']],
                    low=[data['low']], 
                    close=[data['close']],
                    text=info_text,
                    hoverinfo='text'
                )
            ]
        )

        candlestick_today_fig.update_layout(
            title=f"{self._currency} - Today",
            yaxis_title="Price",
            hovermode='x',
            yaxis_tickformat='.5f',
            xaxis_rangeslider_visible=False,
            showlegend=False,
        )

        return candlestick_today_fig

    def plot_candlesticks_weekly(self, data):

        def _create_info(data_row):

            return f"Open: {data_row['open']:.5f}<br>" + \
                f"High: {data_row['high']:.5f}<br>" + \
                f"Low: {data_row['low']:.5f}<br>" + \
                f"Close: {data_row['close']:.5f}<br>" + \
                f"Width: {data_row['pip_difference']}"

        hover_list= data.apply(lambda data_row: _create_info(data_row), axis=1)

        candlestick_week_fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data['time'],
                    open=data['open'], 
                    high=data['high'],
                    low=data['low'], 
                    close=data['close'],
                    text=hover_list,
                    hoverinfo='text'
                )
            ]
        )

        candlestick_week_fig.update_layout(
            title=f"{self._currency} - Series for last 100 working days",
            xaxis_title="Date",
            yaxis_title="Price",
            hovermode='x',
            yaxis_tickformat='.5f',
            xaxis_rangeslider_visible=False,
            showlegend=False,
        )

        return candlestick_week_fig

    def plot_histogram_fullday(self, data, day_stats):

        histogram_fig = go.Figure(
            data=[
                go.Histogram(
                    x=data['close'],
                    opacity=0.4,
                    bingroup='bar'
                )
            ]
        )

        self._draw_vline(histogram_fig, day_stats['close'], "solid", "black")

        histogram_fig.update_layout(
            title=f"{self._currency} - Close price counts (Current close price (Black): <b>{day_stats['close']:.5f}</b>)",
            xaxis_title="Price range",
            yaxis_title="Counts",
            hovermode='x',
            yaxis_tickformat='k',
            bargap=0.20
        )

        return histogram_fig

    def plot_tick_volume_fullday(self, data, start_time):

        tick_vol_fig = go.Figure([
            go.Scatter(
                x=data['time'], 
                y=data['tick_volume'],
                opacity=0.5,
                line=dict(width=1)
            )
        ])

        self._draw_vline(tick_vol_fig, start_time, "solid", "black")
        
        tick_vol_fig.add_hrect(
            y0=30, 
            y1=0,
            fillcolor="#D55A5A",
            annotation_text="Average Volatility",
            annotation_position="outside top right",
            layer="below", 
            opacity=0.25
        )

        tick_vol_fig.update_layout(
            title=f"{self._currency} - Tick Volume for today",
            xaxis_title="Time",
            yaxis_title="Volume",
            hovermode='x',
            yaxis_tickformat='k'
        )

        return tick_vol_fig

    def plot_heatmap_fullday(self, data, start_time):

        info_text = 'Time: %{x}<br><br>' + \
            'Open price: %{customdata[0]:.5f}<br>' + \
            'Close price: %{customdata[1]:.5f}<br>' + \
            '% Change: %{z:.3f}<br><br>' + \
            'High price: %{customdata[2]:.5f}<br>' + \
            'Low price: %{customdata[3]:.5f}<br><extra></extra>'
            
        customdata_list = np.dstack(
            (data['open'], data['close'], data['high'], data['low'])
        )

        heatmap_fig = go.Figure(
            data=go.Heatmap(
                customdata=customdata_list,
                z=[data['percentage_change']],
                y=None,
                x=data['time'],
                zmin=-0.25,
                zmax=0.25,
                colorscale='rdylgn',
                hovertemplate= info_text
            )
        )

        heatmap_fig.update_layout(
            title=f"{self._currency} - Heatmap for price changes today",
            xaxis_title="Time",
            hovermode='x',
        )

        self._draw_vline(heatmap_fig, start_time, "solid", "black")

        heatmap_fig.update_yaxes(showticklabels=False)

        return heatmap_fig

    def plot_percentage_change(self, data, start_time):

        percentage_change_fig = go.Figure([
            go.Scatter(
                x=data['time'], 
                y=data['percentage_change'],
                mode='lines+markers',
                opacity=0.5
            )
        ])

        percentage_change_fig.update_layout(
            title=f"{self._currency} - Percentage Change for today",
            xaxis_title="Time",
            yaxis_title="Percentage change",
            hovermode='x',
            yaxis_tickformat='.3f'
        )

        self._draw_hline(percentage_change_fig, 0, "solid", "black")
        self._draw_vline(percentage_change_fig, start_time, "solid", "black")

        percentage_change_fig.add_hrect(
            y0=0.03, 
            y1=-0.03,
            fillcolor="#D55A5A",
            annotation_text="Less activity zone",
            annotation_position="outside bottom left",
            layer="below", 
            opacity=0.25
        )

        return percentage_change_fig

    def plot_candlesticks_fullday(self, data_day, overall_day, start_time, indicators_df):

        candlesticks_minute_fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data_day['time'],
                    open=data_day['open'], 
                    high=data_day['high'],
                    low=data_day['low'], 
                    close=data_day['close'],
                    name=""
                ),
                go.Scatter(
                    x=indicators_df['time'], 
                    y=indicators_df['sma'],
                    line=dict(color='black', width=5),
                    name=""
                )
            ]
        )

        self._draw_hline(
            candlesticks_minute_fig,
            overall_day['open'],
            "dot",
            'darkmagenta',
            f"Open"
        )

        self._draw_vline(candlesticks_minute_fig, start_time, "solid", "black")

        candlesticks_minute_fig.update_layout(
            title=f"{self._currency} - Series for today",
            xaxis_title="Time",
            yaxis_title="Price",
            hovermode='x',
            yaxis_tickformat='.5f',
            xaxis_rangeslider_visible=False,
            showlegend=False
        )

        return candlesticks_minute_fig

    def plot_rsi_figure(self, rsi_today, start_time):

        rsi_fig = go.Figure([
            go.Scatter(
                x=rsi_today['time'], 
                y=rsi_today['value'],
                line=dict(width=0.5)
            )
        ])

        self._draw_hline(rsi_fig, 50, "solid", "#9A5132", "Balanced")
        self._draw_hline(rsi_fig, 30, "solid", "black", "Oversold")
        self._draw_hline(rsi_fig, 70, "solid", "black", "Overbought")

        self._draw_vline(rsi_fig, start_time, "solid", "black")

        rsi_fig.update_layout(
            xaxis_title="Time",
            yaxis_title="RSI Value",
            hovermode='x',
            yaxis_tickformat='.2f'
        )

        rsi_fig.add_hrect(
            y0=0, 
            y1=30,
            fillcolor="palegreen",
            layer="below", 
            opacity=0.25
        )

        rsi_fig.add_hrect(
            y0=100, 
            y1=70,
            fillcolor="palegreen",
            layer="below", 
            opacity=0.25
        )

        return rsi_fig

    def plot_bull_bears_graph(self, indicators_df, start_time):

        bull_bear_power_fig = go.Figure(
            data=[
                go.Scatter(
                    x=indicators_df['time'],
                    y=indicators_df['bears_power'],
                    name='Bear Power',
                    marker_color='#EC8888'
                ),
                go.Scatter(
                    x=indicators_df['time'],
                    y=indicators_df['bulls_power'],
                    name='Bull Power',
                    marker_color='#888CEC'
                )
            ]
        )

        self._draw_vline(bull_bear_power_fig, start_time, "solid", "black")
        self._draw_hline(bull_bear_power_fig,0,'solid','black')

        bull_bear_power_fig.update_layout(
            template='simple_white',
            title=f"{self._currency} - Bull-Bear measurement (30 minute intervals)",
            hovermode='x',
            yaxis_tickformat='.3f'
        )

        return bull_bear_power_fig

    def plot_pip_difference_graph(self, day_stats):
        
        histogram_fig = go.Figure(
            data=[
                go.Histogram(
                    x=day_stats['pip_difference'],
                    opacity=0.4,
                    bingroup='bar'
                )
            ]
        )

        ongoing_pip_size = day_stats['pip_difference'].iloc[-1]

        histogram_fig.update_layout(
            title=f"{self._currency} - Pip size counts (Ongoing Pip differnece: {ongoing_pip_size})",
            xaxis_title="Pip size",
            yaxis_title="Counts",
            hovermode='x',
            yaxis_tickformat='k',
            bargap=0.20
        )

        self._draw_vline(histogram_fig, ongoing_pip_size, "solid", "black")
        self._draw_vline(histogram_fig, ongoing_pip_size, "solid", "black")

        return histogram_fig