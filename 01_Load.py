import rystavariables as rysta

import pandas as pd
import pytz
import requests
import time
from datetime import datetime, timedelta
import importlib
import json

def RystaPermaLoader():
    
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
        (dfT6, "T", rysta.mt6), 
        (dfB0, "B", rysta.mb0), 
        (dfC1, "C", rysta.mc1),
        (dfH6, "H", rysta.mh6),
        (dfL0, "L", rysta.ml0), 
        (dfP0, "P", rysta.mp0)
    ]

    for i, (dataframe, metric, metricname) in enumerate(dataframes):
        print(f"Extracting Metric: {metricname}")

        #Alte API - Wurde deaktiviert
        # api = "https://rysta-api.com/api/v2/devices/"
        # data = requests.get(
        #         api + rysta.device + "/metrics/" + metric + "/data?fromTime="+ fromTime + "&toTime=" + toTime + "&apiKey=" + token,
        #         headers = {'accept': 'application/json','Content-Type': 'application/json'}
        # )

        api = "https://rysta-api.com/api/v2/beta/entities/Device/"
        data = requests.get(
            api + rysta.device + "/" + metric + "/data?fromTime="+ fromTime + "&toTime=" + toTime + "&regularize=" + rysta.reg + "&apiKey=" + token,
            headers = {'accept': 'application/json','Content-Type': 'application/json'}
        )

        data = data.json()
        data = [{"t": entry["t"], "v": entry["v"]} for entry in data["data"]]
        df_temp = pd.DataFrame(data)
        df_temp = df_temp.sort_values(by='t', ascending=False)
        df_temp['t'] += 1*60*60
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

    file = "assets/Raw_Rysta_Data.csv"

    # with pd.ExcelWriter(file) as writer:
    #     df.to_excel(writer, sheet_name="Full Data Export", index=False)

    df.to_csv(file, index=False)  # Speichert die Datei ohne Index

    print("Waiting...")

if __name__ == "__main__":
    RystaPermaLoader()