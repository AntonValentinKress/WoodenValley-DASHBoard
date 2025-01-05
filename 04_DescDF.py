import time
import pandas as pd
import rystavariables as rysta

def RystaDataDescriber():
    print("Describing Dataframe")
    # Daten aus Excel-Datenbank einlesen (Schleife bis IO)
    while True:
        try:
            df = pd.read_csv("assets/Raw_Rysta_Data.csv", index_col=None)
            print("Extracting of Data successfull")
            break
        except:
            time.sleep(1)

    df.drop(rysta.tst, axis=1, inplace=True)

    df = df.describe()
    
    df = df.round(1)

    df.drop(["count", "std", "25%", "50%", "75%"], inplace=True)
    df = df.rename(index={'mean': 'Mittelwert', 'min': 'Minimum', 'max': 'Maximum'})

    print("Saving Dataframe to .json-File")

    df.to_json('assets/DataDescription.json', index=True, indent=4)

    print("Waiting...")

RystaDataDescriber()