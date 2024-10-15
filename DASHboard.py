import multiprocessing
import requests
import pytz
import time
import socket
import segno
import logging
import importlib

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

from datetime import datetime, timedelta
from dash import Dash, dcc, html, Input, Output, dash_table, callback

import rystavariables as rysta

def MPProcessExample(event):
    while not event.is_set():

        #Hier der Programmcode

        print("Waiting...")
        for _ in range(60):
            if event.is_set():
                break
            time.sleep(1)

def RystaDashboard():
    app = Dash(__name__)

    #Unterdrücken von Konsolenausgaben der Web-App
    #log = logging.getLogger('werkzeug')
    #log.setLevel(logging.ERROR)

    app.layout = html.Div(className="wrapper", children=[
            html.Div(className="app-header", children=[
                html.H1("Live Rysta Dashboard"),
                html.Div(className="timestamp", id='live-update-text'),
                dcc.Interval(
                    id='interval-component',
                    interval=10*1000,
                    n_intervals=0
                )
            ]),

            # html.P("Dieses Dashboard wurde von Studenten der Hochschule Esslingen entwickelt!"),

            # Diagramme
            html.Div(className="wrapper-graphs", children=[
                html.Div([
                    dcc.Graph(id='live-update-line-graph', config={'displaylogo': False}, style={'width': '100%'}),
                    dcc.Interval(
                        id='interval-line-graph',
                        interval=60*1000,
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
            html.Div(className="wrapper-table", children=[
                html.Div([
                        html.H4("Randdaten historischer Messwerte"),
                        dash_table.DataTable(
                            id='live-update-table',
                            columns=[],  # Die Spalten werden im Callback aktualisiert
                            data=[],     # Die Daten werden im Callback aktualisiert
                            #page_size=20  # Optional: Anzahl der Zeilen pro Seite
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

                ], style={'display': 'inline-block', 'width': '60%'}),
                html.Div([

                ], style={'display': 'inline-block', 'width': '40%'})
            ], style={'display': 'flex', 'width': '100%'}),

            html.Div(className="qr-code-wrapper", children=[
                html.Img(className="qr-code", id='live-update-qr', src='/assets/Dashboard.svg'),
                dcc.Interval(
                    id="interval-qr",
                    interval=60*1000,
                    n_intervals=0
                )
            ]),
            html.Div(className="dokumentation-wrapper", children=[
                html.H1("Dokumentation")
            ]),
        ]
    )
    

    @callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
    def update_timer(n):
        current_time = datetime.now()
        current_time = current_time.strftime("%d.%m.%Y %H:%M:%S") 
        style = {'padding': '5px', 'fontSize': '16px'}
        return[
            html.Span(f'Aktuelle Uhrzeit: {current_time}', style=style)
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
              Input('intervall-qr', 'n_intervals'))
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

        df = df.reset_index()

        columns = [{'name': col, 'id': col} for col in df.columns]
        data = df.to_dict('records')
    
        return columns, data

    #app.run(debug=False, host='0.0.0.0', port=8080)
    app.run(debug=False, port=8080)

def RystaPermaLoader(event):
    while not event.is_set():
        # Variablen neu laden
        importlib.reload(rysta)
        
        print(f"Starting Data Export. Daterange: {rysta.count_of_days} Days")

        response = requests.post(
            "https://rysta-api.com/api/v2/auth/login",
            headers = {'accept': 'application/json','Content-Type': 'application/json'},
            json={"email": rysta.email, "password": rysta.password}
        )
        token = response.json()

        today       = datetime.now().astimezone(pytz.timezone('Europe/Berlin'))
        toTime      = (today + timedelta(days=1)).strftime("%Y-%m-%d") + "T00%3A00%3A00%2B0200"
        fromTime    = (today - timedelta(days=rysta.count_of_days)).strftime("%Y-%m-%d") + "T00%3A00%3A00%2B0200"

        # Empty Metric Dataframes
        dfT6 = []
        dfB0 = []
        dfC1 = []
        dfH6 = []
        dfL0 = []
        dfP0 = []

        dataframes = [
            (dfT6, "T6", rysta.mt6), 
            (dfB0, "B0", rysta.mb0), 
            (dfC1, "C1", rysta.mc1),
            (dfH6, "H6", rysta.mh6),
            (dfL0, "L0", rysta.ml0), 
            (dfP0, "P0", rysta.mp0)
        ]

        for i, (dataframe, metric, metricname) in enumerate(dataframes):
            print(f"Extracting Metric: {metricname}")

            api = "https://rysta-api.com/api/v2/devices/"
            data = requests.get(
                    api + rysta.device + "/metrics/" + metric + "/data?fromTime="+ fromTime + "&toTime=" + toTime + "&apiKey=" + token,
                    headers = {'accept': 'application/json','Content-Type': 'application/json'}
            )
            data = data.json()
            df_temp = pd.DataFrame(data)
            df_temp = df_temp.sort_values(by='t', ascending=False)
            df_temp['t'] += 2*60*60
            df_temp.rename(columns={'t': rysta.tst, 'v': metricname}, inplace=True)
            df_temp[rysta.tst] = pd.to_datetime(df_temp[rysta.tst], unit='s')

            # Aktualisieren des ursprünglichen Dataframe in der übergebenen Liste
            dataframes[i] = (df_temp, metric, metricname)

        # Filled Metric Dataframes
        dfT6 = dataframes[0][0]
        dfB0 = dataframes[1][0]
        dfC1 = dataframes[2][0]
        dfH6 = dataframes[3][0]
        dfL0 = dataframes[4][0]
        dfP0 = dataframes[5][0]
            
        dataframes = [dfT6, dfB0, dfC1, dfH6, dfL0, dfP0]

        print("Combining extracted Dataframes")

        # DataFrames zusammenführen
        df = pd.concat(dataframes).filter([rysta.tst]).drop_duplicates()

        df = pd.merge(df, dfT6, on=rysta.tst, how='left')
        df = pd.merge(df, dfB0, on=rysta.tst, how='left')
        df = pd.merge(df, dfC1, on=rysta.tst, how='left')
        df = pd.merge(df, dfH6, on=rysta.tst, how='left')
        df = pd.merge(df, dfL0, on=rysta.tst, how='left')
        df = pd.merge(df, dfP0, on=rysta.tst, how='left')

        df[rysta.tst] = pd.to_datetime(df[rysta.tst]).dt.round('min')
        df = df.groupby(rysta.tst).mean().reset_index()
        df = df.sort_values(by=rysta.tst, ascending=False)

        min_timestamp = df[rysta.tst].min()
        max_timestamp = df[rysta.tst].max()

        print(f"Extracted Daterange from {min_timestamp} to {max_timestamp}")
        
        full_datetime_range = pd.DataFrame({rysta.tst: pd.date_range(start=min_timestamp, end=max_timestamp, freq='min')})
        df_temp = pd.merge(full_datetime_range, df, on=rysta.tst, how='left')

        df = df_temp

        print("Starting Final Formatting")

        #Aufbereiten der Daten
        df = df.sort_values(by=rysta.tst, ascending=False)
        df = df.interpolate().bfill().ffill().round(1)
        

        print("Saving Data")

        #Daten lokal abspeichern und 60 Sekunden warten für neuen Durchlauf

        excelfile = "assets/Raw_Rysta_Data.xlsx"

        with pd.ExcelWriter(excelfile) as writer:
            df.to_excel(writer, sheet_name="Full Data Export", index=False)

        print("Waiting...")
        for _ in range(60):
            if event.is_set():
                break
            time.sleep(1)

def SurfacePlotPermaPlotter(event):
    while not event.is_set():
        print("Creating and Saving new Surface Plot")

        # Daten aus Excel-Datenbank einlesen (Schleife bis IO)
        while True:
            try:
                df = pd.read_excel("assets/Raw_Rysta_Data.xlsx")
                print("Extracting of Data successfull")
                break
            except:
                time.sleep(1)

        # Zeitstempel zu DateTime konvertieren
        df[rysta.tst] = pd.to_datetime(df[rysta.tst])

        # Spalte 'Tag' und 'Stunde' aus Zeitstempel ableiten und Zeitstempel entfernen
        df['tag'] = df[rysta.tst].dt.date
        df['stunde'] = df[rysta.tst].dt.hour
        df.drop(labels=rysta.tst, axis=1, inplace=True)

        # Mittlere Messwerteerte pro Tag und Stunde berechnen
        df_grouped = df.groupby(['tag', 'stunde']).mean().reset_index()

        # Konvertiere die 'tag' und 'stunde' Spalten in eindeutige Werte
        unique_days = df_grouped['tag'].unique()
        unique_hours = df_grouped['stunde'].unique()

        # Erstelle ein Gitter mit allen Kombinationen aus Tagen und Stunden
        X, Y = np.meshgrid(unique_days, unique_hours)

        # Liste der verfügbaren Metriken aus der df-Spaltenauswahl
        available_metrics = [rysta.mt6, rysta.mb0, rysta.mc1, rysta.mh6, rysta.ml0, rysta.mp0]  # Liste der möglichen Metriken

        print("Create 3D-Graph")

        # Funktion zum Erstellen des Z-Wertes basierend auf der ausgewählten Metrik
        def get_z_values(metric):
            Z = np.zeros(X.shape)
            for i, day in enumerate(unique_days):
                for j, hour in enumerate(unique_hours):
                    value = df_grouped[(df_grouped['tag'] == day) & (df_grouped['stunde'] == hour)]
                    if not value.empty:
                        Z[j, i] = value[metric].values[0]
                    else:
                        Z[j, i] = np.nan
            return Z

        # Erstelle initialen Z-Wert mit einer Standardmetrik
        initial_metric = available_metrics[0]
        Z = get_z_values(initial_metric)

        # 3D-Surface Plot erstellen
        fig = go.Figure(data=[go.Surface(
            z=Z, x=X, y=Y,
            hovertemplate="Tag: %{x}<br>Stunde: %{y}<br>Messwert: %{z}<extra></extra>"
        )])

        # Achsentitel hinzufügen und Margin verkleinern
        fig.update_layout(
            title="Historische Messwerte",
            scene=dict(
                xaxis_title='Tag',
                yaxis_title='Stunde',
                zaxis_title='Messwerte (Mittel)'
            ),
            plot_bgcolor = 'rgba(0,0,0,0)',
            paper_bgcolor = '#2B2B30',
            font_color= '#FFFFFF',
            title_font_color= '#FFFFFF',
            margin=dict(
                l=10, 
                r=10, 
                t=40, 
                b=10),
        )

        # Dropdown-Buttons für die Auswahl der Metrik hinzufügen
        dropdown_buttons = [
            {
                'args': [{'z': [get_z_values(metric)]}], # Aktualisiere Z-Werte
                'label': metric,
                'method': 'restyle'
            }
            for metric in available_metrics
        ]

        # Dropdown zum Layout hinzufügen
        fig.update_layout(
            updatemenus=[{
                'buttons': dropdown_buttons,
                'direction': 'down',
                'showactive': True,
                'x': 0.95,
                'xanchor': 'right',
                'y': 1.15,
                'yanchor': 'top'
            }]
        )

        print("Saving 3D-Graph to .json-File")

        pio.write_json(fig, "assets/SurfacePlot.json", pretty=True)

        print("Waiting...")
        for _ in range(60):
            if event.is_set():
                break
            time.sleep(1)

def RystaPermaQR(event):
    while not event.is_set():
        print("Generatung QR-Code")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))

        ip = s.getsockname()[0]
        print(f"Current IP: {ip}")

        s.close()

        url = f"http://{ip}:{rysta.port}"

        qrcode = segno.make(url)

        print("Save QR-Code as .svg-File")

        qrcode.save('assets/Dashboard.svg')

        print("Waiting...")
        for _ in range(60):
            if event.is_set():
                break
            time.sleep(1)

def LinePlotPermaPlotter(event):
    # Excel-Datei einlesen und sicherstellen, dass die erste Spalte (Index) als Datum verwendet wird
    while not event.is_set():
        print("Creating and Saving new Surface Plot")

        # Daten aus Excel-Datenbank einlesen (Schleife bis IO)
        while True:
            try:
                df = pd.read_excel("assets/Raw_Rysta_Data.xlsx")
                print("Extracting of Data successfull")
                break
            except:
                time.sleep(1)

        print("Creating Line Graph")

        # Zeitstempel zu DateTime konvertieren
        df[rysta.tst] = pd.to_datetime(df[rysta.tst])

        # Diagramm erstellen mit Plotly
        fig = go.Figure()

        # CO²-Gehalt
        fig.add_trace(go.Scatter(x=df[rysta.tst], y=df[rysta.mc1], mode='lines', name=rysta.mc1, line=dict(color='#2d6774')))

        # Vorhersage
        fig.add_trace(go.Scatter(x=df[rysta.tst], y=df[rysta.mc1]+100, mode='lines', name='Vorhersage', line=dict(color='#bdbb00')))

        # Layout-Anpassungen
        fig.update_layout(
            title="CO2-Prognose",
            xaxis_title=rysta.tst,
            yaxis_title=rysta.mc1,
            #yaxis=dict(title=rysta.mc1, titlefont=dict(color='#2d6774'), tickfont=dict(color='#2d6774')),
            #yaxis2=dict(title='Vorhersage', titlefont=dict(color='#bdbb00'), tickfont=dict(color='#bdbb00'), overlaying='y', side='right'),
            yaxis=dict(title=rysta.mc1),
            yaxis2=dict(title='Vorhersage', overlaying='y', side='right'),
           legend=dict(x=0, y=1, traceorder='normal'),
            autosize=True,
            plot_bgcolor = 'rgba(0,0,0,0)',
            paper_bgcolor = '#2B2B30',
            font_color= '#FFFFFF',
            title_font_color= '#FFFFFF',
            margin=dict(
                l=10, 
                r=10, 
                t=40, 
                b=10
            )
        )
        
        print("Saving Line-Graph to .json-File")

        pio.write_json(fig, "assets/LinePlot.json", pretty=True)

        print("Waiting...")
        for _ in range(60):
            if event.is_set():
                break
            time.sleep(1)

def RystaDataDescriber(event):
    while not event.is_set():

        print("Describing Dataframe")
        
        # Daten aus Excel-Datenbank einlesen (Schleife bis IO)
        while True:
            try:
                df = pd.read_excel("assets/Raw_Rysta_Data.xlsx")
                print("Extracting of Data successfull")
                break
            except:
                time.sleep(1)

        df = df.describe()

        df.drop(rysta.tst, axis=1, inplace=True)
        df = df.round(1)

        df.drop(["std", "25%", "50%", "75%"], inplace=True)
        df = df.rename(index={'count': 'Anzahl', 'mean': 'Mittelwert', 'min': 'Minimum', 'max': 'Maximum'})

        df.to_json('assets/DataDescription.json', index=True)

        print("Waiting...")
        for _ in range(60):
            if event.is_set():
                break
            time.sleep(1)

if __name__ == '__main__':
    
    start = time.perf_counter()

    # Eventhandler
    event = multiprocessing.Event()

    #Prozesse definieren
    MPDashbaod = multiprocessing.Process(target=RystaDashboard)
    MPLoader = multiprocessing.Process(target=RystaPermaLoader, args=(event,))
    MPPlotter = multiprocessing.Process(target=SurfacePlotPermaPlotter, args=(event,))
    MPQRCode = multiprocessing.Process(target=RystaPermaQR, args=(event,))
    MPLinePLotter = multiprocessing.Process(target=LinePlotPermaPlotter, args=(event,))
    MPDescriptor = multiprocessing.Process(target=RystaDataDescriber, args=(event,))

    #Prozesse starten
    print("\nProzesse werden gestartet!")

    MPDashbaod.start()
    MPLoader.start()
    MPPlotter.start()
    MPQRCode.start()
    MPLinePLotter.start()
    MPDescriptor.start()

    # Handling des Programmabbruchs
    print("Type 'exit' for Shutdown:\n")
    while True:
        user_input = input()
        if user_input == 'exit':

            print("\nStop-Event set. Shutdown will commence")
            event.set()

            #Hier Dash Prozess terminieren
            #MPLoader.terminate()

            #Warten bis alle Prozess beendet sind
            MPLoader.join()
            MPPlotter.join()
            MPQRCode.join()
            MPLinePLotter.join()
            MPDescriptor.join()
            MPDashbaod.terminate() #Terminierung da keine Schleife im Programm verfügbar ist

            #Auswerten wie lange der Prozess gelaufen ist
            finish = time.perf_counter()
            print(f'Prozess Runtime: {round(finish-start, 2)} Seconds\n')

            #Schleife beenden
            break