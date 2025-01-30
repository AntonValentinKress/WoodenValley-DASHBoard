import time
import pandas as pd
import json
import rystavariables as rysta


def MostRecentData():
    print("Evaluating most recent data")

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

    max_timestamp_row = df.loc[df[rysta.tst].idxmax()]
    
    print("Evaluating Data")

    eval_json = {}

    for header, value in max_timestamp_row.items():
        eval = "FEHLER"
        match header:
            case rysta.tst:
                #Zeitstempel ist nicht relevant
                continue
                
            case rysta.mt6:
                #Temperatur
                match value:
                    case _ if value >= 26:
                        eval = "sehr hoch! Risiko für Überhitzung. Viel trinken, Raum kühlen."
                    case _ if  26 <= value < 31:
                        eval = "hoch. Unwohlsein möglich. Lüften oder Ventilator nutzen."
                    case _ if 19 <= value < 26:
                        eval = "angenehm. Optimale Bedingungen für Innenräume."
                    case _ if 15 <= value < 19:
                        eval = "kalt. Etwas kühl, leichte Heizung empfehlenswert."
                    case _:
                        eval = "sehr kalt. Risiko für Unbehagen. Heizung nutzen, Raum isolieren."

                message = f"Die Temperatur im Raum ist {eval}"

                eval_json[rysta.mt6] = {
                    "value": f"{value} °C",
                    "message": f"{message}"
                }

            case rysta.mb0:
                #Helligkeit
                match value:
                    case _ if value >= 3.5:
                        eval = "hell. Geeignet für Arbeit oder Aktivitäten. Blendung vermeiden."
                    case _:
                        eval = "dunkel. Beleuchtung einschalten für Komfort und Sicherheit."

                message = f"Helligkeit ({value} Lux) im Raum ist {eval}"

            case rysta.mc1:
                #CO2
                match value:
                    case _ if value >= 2200:
                        eval = "sehr hoch! Risiko für Konzentrationsprobleme. Dringend lüften."
                    case _ if 2000 <= value < 2200:
                        eval = "hoch. Luftqualität beeinträchtigt. Lüften empfohlen."
                    case _ if 1500 <= value < 2000:
                        eval = "kritisch. Konzentration kann leiden. Regelmäßig lüften."
                    case _:
                        eval = "ideal. Gute Luftqualität."

                message = f"Der CO²-Gehalt im Raum ist {eval}"

                eval_json[rysta.mc1] = {
                    "value": f"{value} ppm",
                    "message": f"{message}"
                }
            
            case rysta.mh6:
                #Luftfeuchtigkeit
                match value:
                    case _ if value >= 70:
                        eval = "sehr hoch! Risiko für Schimmelbildung. Entfeuchter oder Lüften empfohlen."
                    case _ if 60 <= value < 70:
                        eval = "hoch. Luftfeuchtigkeit könnte unangenehm sein. Lüften oder Entfeuchter nutzen."
                    case _ if 40 <= value < 60:
                        eval = "ideal. Gute Luftfeuchtigkeit für angenehmes Raumklima."
                    case _ if 30 <= value < 40:
                        eval = "niedrig. Kann die Haut austrocknen. Feuchtigkeit zuführen."
                    case _:
                        eval = "sehr niedrig. Gefahr für trockene Luft. Luftbefeuchter empfehlen."

                message = f"Die Luftfeuchtigkeit im Raum ist {eval}"

                eval_json[rysta.mh6] = {
                    "value": f"{value} %",
                    "message": f"{message}"
                }
            
            case rysta.ml0:
                #Lautstärke
                match value:
                    case _ if value >= 80:
                        eval = "sehr laut! Kann störend wirken. Lärmschutz oder Dämpfung erforderlich."
                    case _ if 60 <= value < 80:
                        eval = "laut. Kann unangenehm sein. Ohrenschutz oder Schallschutz empfohlen."
                    case _ if 45 <= value < 60:
                        eval = "moderat. Akzeptabel für normale Aktivitäten."
                    case _ if 30 <= value < 45:
                        eval = "leise. Angenehm für ruhige Umgebungen."
                    case _:
                        eval = "sehr leise. Ideal für Konzentration und Ruhe."

                message = f"Die Lautstärke im Raum ist {eval}"
  
                eval_json[rysta.ml0] = {
                    "value": f"{value} dB",
                    "message": f"{message}"
                }

            case rysta.mp0:
                #Luftdruck
                match value:
                    case _ if value >= 1020:
                        eval = "hoch. Schönes Wetter, stabil und ruhig. Keine Wetteränderung zu erwarten."
                    case _ if 1010 <= value < 1020:
                        eval = "normal. Gutes Wetter, keine extremen Bedingungen."
                    case _ if 1000 <= value < 1010:
                        eval = "tief. Mögliche Wetteränderung. Es könnte windig werden oder es ziehen Wolken auf."
                    case _ if 990 <= value < 1000:
                        eval = "sehr tief. Unwettergefahr. Starker Wind und Niederschläge möglich."
                    case _:
                        eval = "extrem tief. Starkes Unwetter oder Sturm zu erwarten."

                message = f"Der Luftdruck im Raum ist {eval}"

                eval_json[rysta.mp0] = {
                    "value": f"{value} hPa",
                    "message": f"{message}"
                }

            case _:
                "Fehler!"

    print("Save Data to json-File")
    
    with open("assets/CurrentData.json", "w", encoding="utf-8") as file:
        json.dump(eval_json, file, ensure_ascii=False, indent=4)

    print("Waiting...")

if __name__ == "__main__":
    MostRecentData()