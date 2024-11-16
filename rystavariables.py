"""
Diese Datei enthält die für die Arbeit mit dem Rysta Sensor benötigten Variablen.
"""

#Gerät
#device = "PQRCUSC3" #HomeOffice - Anton Kreß
device = "LHSQREC3" #HomeOffice Raum OG - Robert Böker
#device = "XCUHSXC3" #HomeOffice Raum EG - Robert Böker

#Nutzerdaten
email = "ankrgl00@hs-esslingen.de"
password = "Ankrgl00"

#Zeitspanne die geladen wird (in Tagen)
count_of_days = 30

#Metrikbezeichnungen
tst = "Zeitstempel"
mt6 = "Lufttemperatur"
mb0 = "Helligkeit"
mc1 = "CO2-Gehalt"
mh6 = "Luftfeuchtigkeit"
ml0 = "Lautstärke"
mp0 = "Luftdruck"

#Dashboard
port = 8099
public = 1 #1 = Netzwerkweit; 0 = Lokaler Rechner