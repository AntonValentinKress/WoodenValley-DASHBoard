from dash import Dash, dcc, html, Input, Output, dash_table, callback
import pandas as pd
import time
from datetime import datetime
import plotly.io as pio
import json
import rystavariables as rysta

def RystaDashboard():
    app = Dash(__name__)
    app.layout = html.Div(className="wrapper", children=[
        html.Div(className="app-header", children=[
            html.Div(className="logo-container", children=[
                html.Img(src=r"assets/WV_woodii_Logo_Website.png", alt='image', style={'height':'5vh'}),
            ]),
            html.Div(className="center-container", children=[
                html.H1("W∞d.ii Live-Dashboard", className="header-title"),
                html.Div(className="timestamp", id='live-update-text', style={'color': 'white'}),
                dcc.Interval(
                    id='interval-component',
                    interval=1*1000,
                    n_intervals=0
                )
            ]),


            html.Div(className="qr-code-container", children=[
                html.Img(className="qr-code", id='live-update-qr', src='/assets/Dashboard.svg'),
                dcc.Interval(
                    id="interval-qr",
                    interval=60*1000,
                    n_intervals=0
                )
            ])
        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between'}),

            # Diagramme
            html.Div(className="wrapper-graphs", children=[
                html.Div([
                    dcc.Graph(id='live-update-line-graph', config={'displaylogo': False}, style={'width': '100%'}),
                    dcc.Interval(
                        id='interval-line-graph',
                        interval=300*1000,
                        n_intervals=0
                    )
                ], style={'display': 'inline-block', 'width': '60%'}),
                html.Div([
                    dcc.Graph(id='live-update-graph', config={'displaylogo': False}, style={'width': '100%', 'margin-left': '5px'}),
                    dcc.Interval(
                        id='interval-surface-graph',
                        interval=300*1000,
                        n_intervals=0
                    )
                ], style={'display': 'inline-block', 'width': '40%'})
            ], style={'display': 'flex', 'width': '100%'}),

            #Tabellenkomponenten und Handlungsempfehlungen
            html.Div([
                #html.H4("Aktuelle Messwerte", style={'color': 'white'}),
                html.Div(className="wrapper-tips", children=[
                    html.Div([
                        html.Div([
                            html.Span(rysta.mt6),  # Titel der Metrik
                            html.Span(id="value-Lufttemperatur", className="value-Lufttemperatur")  # Wert der Metrik
                        ]),
                        html.Div(id="message-Lufttemperatur", className="message-Lufttemperatur")  # Nachricht
                    ]),
                    html.Div([
                        html.Div([
                            html.Span(rysta.mc1),  # Titel der Metrik
                            html.Span(id="value-CO2-Gehalt", className="value-CO2-Gehalt")  # Wert der Metrik
                        ]),
                        html.Div(id="message-CO2-Gehalt", className="message-CO2-Gehalt")  # Nachricht
                    ]),
                    html.Div([
                        html.Div([
                            html.Span(rysta.mh6),  # Titel der Metrik
                            html.Span(id="value-Luftfeuchtigkeit", className="value-Luftfeuchtigkeit")  # Wert der Metrik
                        ]),
                        html.Div(id="message-Luftfeuchtigkeit", className="message-Luftfeuchtigkeit")  # Nachricht
                    ]),
                    html.Div([
                        html.Div([
                            html.Span(rysta.ml0),  # Titel der Metrik
                            html.Span(id="value-Lautstärke", className="value-Lautstärke")  # Wert der Metrik
                        ]),
                        html.Div(id="message-Lautstärke", className="message-Lautstärke")  # Nachricht
                    ]),
                    html.Div([
                        html.Div([
                            html.Span(rysta.mp0),  
                            html.Span(id="value-Luftdruck", className="value-Luftdruck")  # Wert der Metrik
                        ]),
                        html.Div(id="message-Luftdruck", className="message-Luftdruck")  # Nachricht
                    ])
                ], style={'display': 'inline-block', 'width': '60%'}),
                dcc.Interval(
                    id='interval-mrd',
                    interval=60*1000,
                    n_intervals=0
                ),
                
                html.Div([
                    html.H4("Randdaten historischer Messwerte", style={'color': 'white'}),
                    dash_table.DataTable(
                        id='live-update-table',
                        columns=[],  
                        data=[],    
                        style_as_list_view=True,
                        style_cell={'padding': '5px', 'backgroundColor': '#2B2B30'},
                        style_header={
                            'backgroundColor': '#303030',
                            'fontWeight': 'bold'
                        },
                    ),
                    dcc.Interval(
                        id='interval-table',
                        interval=60*1000,
                        n_intervals=0
                    )

                ], style={'display': 'inline-block', 'width': '40%', 'padding': '10px'})
            ], style={'display': 'flex', 'width': '100%', 'height': '100%'})
        ],style={'height': '100%', 'width': 'auto'}
    )
    

    @callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
    def update_timer(n):
        current_time = datetime.now()
        current_time = current_time.strftime("%d.%m.%Y %H:%M:%S") 
        style = {'padding': '5px', 'fontSize': '16px'}
        return[
            html.Span(f'({current_time})', style=style)
        ]

    @callback(Output('live-update-graph', 'figure'),
                Input('interval-surface-graph', 'n_intervals'))
    def update_graph_live(n):
        plot = 'assets/SurfacePlot.json'

        while True:
            try:
                with open(plot, 'r') as f:
                    fig = pio.from_json(f.read())
                    break
            except:
                time.sleep(1)
        
        return fig
    
    @callback(Output('live-update-line-graph', 'figure'),
                Input('interval-line-graph', 'n_intervals'))
    def update_graph_live(n):
        plot = 'assets/LinePlot.json'

        while True:
            try:
                with open(plot, 'r') as f:
                    fig = pio.from_json(f.read())
                    break
            except:
                time.sleep(1)
        
        return fig

    @callback(Output('live-update-qr', 'src'),
              Input('interval-qr', 'n_intervals'))
    def update_qr(n):
        timestamp = int(time.time())
        return f'/assets/Dashboard.svg?t={timestamp}'

    @app.callback(Output('live-update-table', 'columns'), Output('live-update-table', 'data'),
        Input('interval-table', 'n_intervals')
    )
    def update_table(n):
        table_data = "assets/DataDescription.json"
        while True:
            try:
                df = pd.read_json(table_data)
                break
            except:
                time.sleep(1)

        df = df.transpose()
        df = df.reset_index()
        df = df.rename(columns={"index": "Metrik"})


        columns = [{'name': col, 'id': col} for col in df.columns]
        data = df.to_dict('records')
    
        return columns, data
    
    @app.callback(
        Output("value-Lufttemperatur", "children"),
        Output("message-Lufttemperatur", "children"),
        Output("value-CO2-Gehalt", "children"),
        Output("message-CO2-Gehalt", "children"),
        Output("value-Luftfeuchtigkeit", "children"),
        Output("message-Luftfeuchtigkeit", "children"),
        Output("value-Lautstärke", "children"),
        Output("message-Lautstärke", "children"),
        Output("value-Luftdruck", "children"),
        Output("message-Luftdruck", "children"),
        Input("interval-mrd", "n_intervals")
    )
    def update_current_metrics(n):
        eval_data = "assets/CurrentData.json"
        while True:
            try:
                with open(eval_data, "r", encoding="utf-8") as file:
                    data = json.load(file)

                df = pd.DataFrame([
                    {"metric": metric, "value": details["value"], "message": details["message"]}
                    for metric, details in data.items()
                ])
                break
            except:
                time.sleep(1)

        # Hilffunktion um Daten aus Dataframe zu extrahieren
        def get_metric_value(metric_name):
            row = df[df['metric'] == metric_name]
            if not row.empty:
                return row.iloc[0]['value'], row.iloc[0]['message']
            return "N/A", "Keine Daten verfügbar"

        lufttemperatur_value, lufttemperatur_message = get_metric_value("Lufttemperatur")
        co2_value, co2_message = get_metric_value("CO2-Gehalt")
        luftfeuchtigkeit_value, luftfeuchtigkeit_message = get_metric_value("Luftfeuchtigkeit")
        lautstärke_value, lautstärke_message = get_metric_value("Lautstärke")
        luftdruck_value, luftdruck_message = get_metric_value("Luftdruck")   

        return (
            lufttemperatur_value, lufttemperatur_message,
            co2_value, co2_message,
            luftfeuchtigkeit_value, luftfeuchtigkeit_message,
            lautstärke_value, lautstärke_message,
            luftdruck_value, luftdruck_message
        )   

    app.run(debug=rysta.debug, host='0.0.0.0', port=rysta.port)

RystaDashboard()