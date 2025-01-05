import pandas as pd
import rystavariables as rysta
import numpy as np
import time
import plotly.graph_objects as go
import plotly.io as pio

def SurfacePlotPermaPlotter():
    print("Creating and Saving new Surface Plot")

    # Daten aus Excel-Datenbank einlesen (Schleife bis IO)
    while True:
        try:
            df = pd.read_csv("assets/Raw_Rysta_Data.csv", index_col=None)
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
        paper_bgcolor = 'rgba(0,0,0,0)',
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

SurfacePlotPermaPlotter()
