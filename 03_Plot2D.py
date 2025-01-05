import time
import rystavariables as rysta
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from datetime import timedelta
import xgboost as xgb
import pickle

def CreateAiDataFrame(df:pd.DataFrame):
    min_timestamp = df[rysta.tst].min()
    max_timestamp = df[rysta.tst].max()

    df = df.set_index(rysta.tst)

    future = pd.date_range(max_timestamp, max_timestamp + timedelta(hours=1), freq="min")
    future_df = pd.DataFrame(index=future)

    future_df["isFuture"] = True
    df["isFuture"] = False

    df_and_future = pd.concat([df, future_df])

    df = df_and_future.copy()
    df = df.sort_index()

    #Time-Features
    #df = df.copy()
    df['hour'] = df.index.hour
    df['minute'] = df.index.minute
    df['dayofweek'] = df.index.dayofweek

    #Data-Features
    target_map_C1 = df[rysta.mc1].to_dict()
    target_map_T6 = df[rysta.mt6].to_dict()
    target_map_L0 = df[rysta.ml0].to_dict()
    target_map_B0 = df[rysta.mb0].to_dict()
    target_map_P0 = df[rysta.mp0].to_dict()
    """
    Informationen von Messwerten vor 1 - 5 Stunden. Nicht unter 1 Stunde da dann
    keine Prognose möglich ist. Wird später der Prognosehorizont verringert
    kann hier auch angepasst werden.
    """
    #C1
    df["C1 060 min"] = (df.index - pd.Timedelta("61 minutes")).map(target_map_C1)
    df["C1 090 min"] = (df.index - pd.Timedelta("90 minutes")).map(target_map_C1)
    df["C1 120 min"] = (df.index - pd.Timedelta("120 minutes")).map(target_map_C1)

    #T6
    df["T6 060 min"] = (df.index - pd.Timedelta("61 minutes")).map(target_map_T6)
    df["T6 090 min"] = (df.index - pd.Timedelta("90 minutes")).map(target_map_T6)
    df["T6 120 min"] = (df.index - pd.Timedelta("120 minutes")).map(target_map_T6)

    #B0
    df["B0 060 min"] = (df.index - pd.Timedelta("61 minutes")).map(target_map_B0)
    df["B0 090 min"] = (df.index - pd.Timedelta("90 minutes")).map(target_map_B0)
    df["B0 120 min"] = (df.index - pd.Timedelta("120 minutes")).map(target_map_B0)

    #L0
    df["L0 060 min"] = (df.index - pd.Timedelta("61 minutes")).map(target_map_L0)
    df["L0 090 min"] = (df.index - pd.Timedelta("90 minutes")).map(target_map_L0)
    df["L0 120 min"] = (df.index - pd.Timedelta("120 minutes")).map(target_map_L0)

    #P0
    df["P0 060 min"] = (df.index - pd.Timedelta("61 minutes")).map(target_map_P0)
    df["P0 090 min"] = (df.index - pd.Timedelta("90 minutes")).map(target_map_P0)
    df["P0 120 min"] = (df.index - pd.Timedelta("120 minutes")).map(target_map_P0)

    return df
    

def LinePlotPermaPlotter():
    # Excel-Datei einlesen und sicherstellen, dass die erste Spalte (Index) als Datum verwendet wird

    print("Creating and Saving new Line-Plot")

    # Daten aus Excel-Datenbank einlesen (Schleife bis IO)
    while True:
        try:
            df = pd.read_csv("assets/Raw_Rysta_Data.csv", index_col=None)
            print("Extracting of Data successfull")
            break
        except:
            time.sleep(1)

    print("Creating Line Graph")

    # Zeitstempel zu DateTime konvertieren
    df[rysta.tst] = pd.to_datetime(df[rysta.tst])

    # DF auf erste X Datensätze kürzen
    plotdf = df.head(rysta.past_minutes_shown)

    # Diagramm erstellen mit Plotly
    fig = go.Figure()

    # CO²-Gehalt
    fig.add_trace(go.Scatter(x=plotdf[rysta.tst], y=plotdf[rysta.mc1], mode='lines', name=rysta.mc1, line=dict(color='#2d6774')))

    # Vorhersage
    # DF anpassen
    df = CreateAiDataFrame(df)
    # KI

    file_name = "assets/reg.pkl"
        
    clf = xgb.XGBRegressor()
    clf = pickle.load(open(file_name, "rb"))
    FEATURES = [
        "hour","minute","dayofweek",
        "C1 060 min","C1 090 min","C1 120 min",
        "T6 060 min","T6 090 min","T6 120 min",
        "B0 060 min","B0 090 min","B0 120 min",
        "L0 060 min","L0 090 min","L0 120 min",
        "P0 060 min","P0 090 min","P0 120 min"
    ]
    df["CO²-Forecast"] = clf.predict(df[FEATURES])

    plotdf = df.tail(rysta.past_minutes_shown + 60)
    fig.add_trace(go.Scatter(x=plotdf.index, y=plotdf["CO²-Forecast"], mode='lines', name='Vorhersage', line=dict(color='#bdbb00')))

    # Layout-Anpassungen
    fig.update_layout(
        title="CO2-Prognose",
        xaxis_title=rysta.tst,
        yaxis_title=rysta.mc1,
        yaxis=dict(title=rysta.mc1),
        yaxis2=dict(title='Vorhersage', overlaying='y', side='right'),
        legend=dict(x=0, y=1, traceorder='normal'),
        autosize=True,
        plot_bgcolor = 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)',
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

LinePlotPermaPlotter()