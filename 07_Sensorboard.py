import time
from Adafruit_PCA9685 import PCA9685
from board import SCL, SDA
import busio
import pandas as pd
import rystavariables as rysta

#Funktion um aktuelle Sensordaten auswerten zu können
def MostRecentData():
    while True:
        try:
            df = pd.read_csv("assets/Raw_Rysta_Data.csv", index_col=None)
            print("Extracting of Data successfull")
            break
        except:
            time.sleep(1)
    df[rysta.tst] = pd.to_datetime(df[rysta.tst])
    max_timestamp_row = df.loc[df[rysta.tst].idxmax()]
    return float(max_timestamp_row[rysta.mt6]), float(max_timestamp_row[rysta.mh6])

def control_channel(channel_to_activate, active_channel, channels):
    for channel in channels:
        if channel == channel_to_activate and active_channel != channel: 
            channel.duty_cycle = 0xFFFF
            print(f"Channel {channels.index(channel)} eingeschaltet")
        elif channel != channel_to_activate and active_channel == channel: 
            channel.duty_cycle = 0x0000
            print(f"Channel {channels.index(channel)} ausgeschaltet")
    return channel_to_activate

def turn_off_all_channels(channels):
    for channel in channels:
        channel.duty_cycle = 0x0000
    print("Alle Kanäle ausgeschaltet (Programm beendet)")

if __name__ == "__main__":
    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c)
    pca.frequency = 60

    channel_5 = pca.channels[5]  # Channel für Werte <= 21.00
    channel_4 = pca.channels[4]  # Channel für Werte > 21.00 & < 24.00
    channel_3 = pca.channels[3]  # Channel für Werte >=2 4.00
    channels_temp = [channel_5, channel_4, channel_3]
    active_channel_temp = None  
    last_value_temp = None
    channel_2 = pca.channels[2] # Channel für Werte > 37.00
    channel_1 = pca.channels[1] # Channel für Werte > 50.00
    channel_0 = pca.channels[0] # Channel für Werte > 60.00
    channels_rf = [channel_2, channel_1, channel_0] 
    active_channels_rf = [] 
    last_value_rf = None

    try:
        while True:
            #Zuordnung der letzen Temperatur und Luftfeuchtigkeit in die Variablen
            value_temp, value_rf = MostRecentData()
            if value_temp is not None and value_temp != last_value_temp:
                if 0 <= value_temp <= 21.00:
                    active_channel_temp = control_channel(channel_5, active_channel_temp, channels_temp)
                elif 21.00 < value_temp < 24.00:
                    active_channel_temp = control_channel(channel_4, active_channel_temp, channels_temp)
                elif value_temp >= 24.00:
                    active_channel_temp = control_channel(channel_3, active_channel_temp, channels_temp)

                last_value_temp = value_temp

            if value_rf is not None and value_rf != last_value_rf:
                channels_to_activate_rf = []
                if value_rf > 37.00:
                    channels_to_activate_rf.append(channel_0)
                if value_rf > 50.00:
                    channels_to_activate_rf.append(channel_1)
                if value_rf > 60.00:
                    channels_to_activate_rf.append(channel_2)

                for channel in channels_rf:
                    if channel in channels_to_activate_rf and channel not in active_channels_rf:
                        channel.duty_cycle = 0xFFFF
                        print(f"Channel {channels_rf.index(channel)} eingeschaltet")
                        active_channels_rf.append(channel)
                    elif channel not in channels_to_activate_rf and channel in active_channels_rf:
                        channel.duty_cycle = 0x0000
                        print(f"Channel {channels_rf.index(channel)} ausgeschaltet")
                        active_channels_rf.remove(channel)

                last_value_rf = value_rf

            time.sleep(10)

    except KeyboardInterrupt:
        print("\nProgramm wurde durch STRG+C beendet.")
    
    finally:
        turn_off_all_channels(channels_temp + channels_rf)
        pca.deinit()
        print("PCA9685 deaktiviert. Programm beendet.")
