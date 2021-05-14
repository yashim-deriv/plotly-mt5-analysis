import dash_core_components as dcc
import dash_html_components as html

def _loading_figure_layout(fig_id):
    return dcc.Loading(
        type="default",
        children=html.Div([
            dcc.Graph(
                id=fig_id
            )
        ])
    )

def _generate_profit_pip_calculator():

    field_list = ['profit_target','leverage','minimum_trade']

    return html.Div(
        [
            html.Div([
                dcc.Input(
                    id=f"input_{field}",
                    type="text",
                    placeholder=f"{field}",
                    style={"margin-right": "15px"}
                ) for field in field_list
            ]),

            html.Button(
                'Calculate pip count', 
                id='start-calculation', 
                style={'margin-top': 10}
            ),

            html.Div(
                id='average-pip-text',
                children='Average pip per trade: 0',
                style={'margin-top': 10}
            )
        ]
    )

def _generate_dropdown():

    forex_list = ['GBPUSD','EURGBP','EURUSD','AUDUSD','AUDJPY','USDJPY']

    dropdown_options = [{'label': currency, 'value': currency} for currency in forex_list]

    return html.Div(
        [
            dcc.Dropdown(
                id='currency-dropdown',
                options=dropdown_options,
                clearable=False,
                value='GBPUSD'
            ),
            dcc.Store(id='current-currency',data='GBPUSD')
        ],
            style={"width": "10%"}
    )

def generate_layout():

    return html.Div([
        _generate_profit_pip_calculator(),
        html.Hr(),
        _generate_dropdown(),
        _loading_figure_layout('candlestick-30d-fig'),
        _loading_figure_layout('candlestick-fullday-fig'),
        html.Hr(),
        _loading_figure_layout('tick-volatility-fig'),
        _loading_figure_layout('pip-size-histogram-fig'),
        html.Hr(),
        _loading_figure_layout('heatmap-changes-fig'),
        _loading_figure_layout('percentage-changes-fig'),
        _loading_figure_layout('close-price-histogram-fig'),
        html.Hr(),
        _loading_figure_layout('candlestick-today-fig'),
        _loading_figure_layout('rsi-fig'),
        _loading_figure_layout('bull-bear-fig')
    ])