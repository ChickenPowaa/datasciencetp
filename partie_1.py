import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

####Importation des packages et des données
# Liste pour stocker les données de toutes les parties de MOD1
mod1_data_list = []

# Charger les données pour la partie 1 de MOD1
mod1_part1 = pd.read_csv("datas/Libelium New/part1/mod1.txt", sep="\t", header=None, names=("Time","RH","Temperature","TGS4161","MICS2714","TGS2442","MICS5524","TGS2602","TGS2620"))
mod1_data_list.append(mod1_part1)

# Charger les données pour les parties 2 à 8 de MOD1
for i in range(2, 9):
    file_path = f"datas/Libelium New/part{i}/mod1.txt"
    if os.path.exists(file_path):  # Vérifier si le fichier existe
        mod1_part = pd.read_csv(file_path, sep="\t", header=None, names=("Time","RH","Temperature","TGS4161","MICS2714","TGS2442","MICS5524","TGS2602","TGS2620"))
        mod1_data_list.append(mod1_part)

# Concaténer les données de toutes les parties de MOD1
mod1_data = pd.concat(mod1_data_list)

# Convertir 'Time' en datetime et le mettre en UTC+01:00
mod1_data["Time"] = pd.to_datetime(mod1_data["Time"], dayfirst=True).dt.tz_localize('UTC+01:00', ambiguous='infer')

# Enregistrer le fichier final
mod1_data.to_csv("mod1_grouped.txt", index=False)


# Liste pour stocker les données de toutes les parties de MOD2
mod2_data_list = []

# Charger les données pour la partie 1 de MOD2
mod2_part1 = pd.read_csv("datas/Libelium New/part1/mod2.txt", sep="\t", header=None, names=("Time","RH","Temperature","TGS4161","MICS2714","TGS2442","MICS5524","TGS2602","TGS2620"))
mod2_data_list.append(mod2_part1)

# Charger les données pour les parties 2 à 8 de MOD2
for i in range(2, 9):
    file_path = f"datas/Libelium New/part{i}/mod2.txt"
    if os.path.exists(file_path):  # Vérifier si le fichier existe
        mod2_part = pd.read_csv(file_path, sep="\t", header=None, names=("Time","RH","Temperature","TGS4161","MICS2714","TGS2442","MICS5524","TGS2602","TGS2620"))
        mod2_data_list.append(mod2_part)

# Concaténer les données de toutes les parties de MOD2
mod2_data = pd.concat(mod2_data_list)

# Convertir 'Time' en datetime et le mettre en UTC+01:00
mod2_data["Time"] = pd.to_datetime(mod2_data["Time"], dayfirst=True).dt.tz_localize('UTC+01:00', ambiguous='infer')

# Enregistrer les données dans un fichier CSV
mod2_data.to_csv("mod2_grouped.txt", index=False)

####Importation et groupement des données pour les autres modules

# Pour les 8 parties deS PODS
def Pod_Save(Pod):
    pod_data = pd.concat([pd.read_csv(f"datas/PODs/{folder}/{file}", sep=";", skiprows=(1,2,3,4)).rename(columns={"date": "Time"}) for folder in ["14_nov-22_nov-Pods", "23_nov-12_dec-Pods", "fevrier_mars_2023_pods"] for file in pod_files])
    pod_data["Time"] = pd.to_datetime(pod_data["Time"], errors='coerce')


    # Vérifier si la colonne "Time" est de type datetime
    if pd.api.types.is_datetime64_any_dtype(pod_data["Time"]):
        pod_data["Time"] = pod_data["Time"].dt.tz_convert('Europe/Paris')
    else:
        print("La colonne 'Time' n'est pas de type datetime.")

    if pod_data["Time"].dt.tz is not None:
        pod_data["Time"] = pd.to_datetime(pod_data["Time"]).dt.tz_convert('UTC+01:00')
    else:
        pod_data["Time"] = pd.to_datetime(pod_data["Time"]).dt.tz_localize('UTC', ambiguous='infer').dt.tz_convert('UTC+01:00')

    # Supprimer les colonnes spécifiées si elles existent
    columns_to_drop = ["element", "aqi", "Unnamed: 12"]
    columns_to_drop = [col for col in columns_to_drop if col in pod_data.columns]  # Filtrer les colonnes existantes
    pod_data.drop(columns=columns_to_drop, inplace=True)


    # Enregistrer le fichier final
    pod_data.to_csv("pod_grouped.csv", index=False)
    return pod_data

pod_files = ["POD 200085.csv"]
POD_200085_data=Pod_Save(pod_files)
pod_files = ["POD 200086.csv"]
POD_200086_data=Pod_Save(pod_files)
pod_files = ["POD 200088.csv"]
POD_200088_data=Pod_Save(pod_files)

# Chemins des fichiers pour Piano THICK
piano_thick_files = [f"datas/Piano/{folder}/IMT_Thick.csv" for folder in ["14_nov-22_nov-Piano", "23_nov-12_dec-Piano", "fevrier_mars_2023_piano"]]
# Charger et concaténer les données des fichiers
piano_thick_data = pd.concat([pd.read_csv(file, sep=";", skiprows=(1,2,3,4)).rename(columns={"date": "Time"}) for file in piano_thick_files])

# Supprimer la colonne 'element'
piano_thick_data.drop(columns=["element"], inplace=True)

# Renommer la colonne 'date' en 'Time'
piano_thick_data.rename(columns={"date": "Time"}, inplace=True)

# Convertir la colonne 'Time' en datetime
piano_thick_data["Time"] = pd.to_datetime(piano_thick_data["Time"], format="%Y-%m-%d %H:%M:%S%z", errors='coerce')

# Enregistrer le fichier final
piano_thick_data.to_csv("piano_thick_grouped.csv", index=False)

# Chemins des fichiers pour Piano THIN
piano_thin_files = [f"datas/Piano/{folder}/IMT_Thin.csv" for folder in ["14_nov-22_nov-Piano", "23_nov-12_dec-Piano", "fevrier_mars_2023_piano"]]
# Charger et concaténer les données des fichiers
piano_thin_data = pd.concat([pd.read_csv(file, sep=";", skiprows=(1,2,3,4)).rename(columns={"date": "Time"}) for file in piano_thin_files])

# Supprimer la colonne 'element'
piano_thin_data.drop(columns=["element"], inplace=True)

# Renommer la colonne 'date' en 'Time'
piano_thin_data.rename(columns={"date": "Time"}, inplace=True)

# Convertir la colonne 'Time' en datetime
piano_thin_data["Time"] = pd.to_datetime(piano_thin_data["Time"], format="%Y-%m-%d %H:%M:%S%z", errors='coerce')

# Enregistrer le fichier final
piano_thin_data.to_csv("piano_thin_grouped.csv", index=False)

# Chemins des fichiers pour IMT PICO
pico_files = [f"datas/Piano/{folder}/IMT_PICO.csv" for folder in ["14_nov-22_nov-Piano", "23_nov-12_dec-Piano", "fevrier_mars_2023_piano"]]
# Charger et concaténer les données
pico_data = pd.concat([pd.read_csv(file, sep=";", skiprows=(1,2,3,4)).rename(columns={"date": "Time"}) for file in pico_files])

# Supprimer les colonnes inutiles
columns_to_drop = [col for col in pico_data.columns if 'aqi' in col.lower() or 'qai' in col.lower() or 'iaq' in col.lower() or col == 'element' or 'Unnamed' in col]
pico_data.drop(columns=columns_to_drop, inplace=True)

# Renommer la colonne "date" en "Time"
pico_data.rename(columns={"date": "Time"}, inplace=True)

# Convertir 'Time' en datetime
pico_data["Time"] = pd.to_datetime(pico_data["Time"], format="%Y-%m-%d %H:%M:%S%z", errors='coerce')

# Enregistrer le fichier final
pico_data.to_csv("piano_pico_grouped.csv", index=False)

plt.figure(figsize=(15, 10))  # Plot overview of the files
date_format = mdates.DateFormatter('%d-%b')

plt.subplot(3, 2, 1)  # MOD1
plt.subplots_adjust(top=8)
plt.title("MOD1 (Temperature x Time)")
plt.plot(mod1_data['Time'], mod1_data['Temperature'])
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)

plt.subplot(3, 2, 2)  # MOD2
plt.subplots_adjust(top=8)
plt.title("MOD2 (Temperature x Time)")
plt.plot(mod2_data['Time'], mod2_data['Temperature'])
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)

plt.subplot(3, 2, 3)  # POD 200085
plt.subplots_adjust(top=8)
plt.title("POD 200085 (Temperature x Time)")
plt.plot(POD_200085_data['Time'], POD_200085_data['temperature'])
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)

plt.subplot(3, 2, 4)  # Piano PICO
plt.subplots_adjust(top=8)
plt.title("PICO (Temperature x Time)")
plt.plot(pico_data['Time'], pico_data['bme68x_temp'])
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)

plt.subplot(3, 2, 5)  # Piano Thick
plt.subplots_adjust(top=8)
plt.title("THICK (TGS2620 x Time)")
plt.plot(piano_thick_data['Time'], piano_thick_data['piano_TGS2620I00'])
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)

plt.subplot(3, 2, 6)  # Piano Thin
plt.subplots_adjust(top=8)
plt.title("THIN (GM102B x Time)")
plt.plot(piano_thin_data['Time'], piano_thin_data['piano_GM102BI00'])
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()