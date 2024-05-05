import pandas as pd

# Charger les données des différents modules
mod1_data = pd.read_csv("mod1_grouped.txt")
mod2_data = pd.read_csv("mod2_grouped.txt")
pod_data = pd.read_csv("pod_grouped.csv")
piano_thick_data = pd.read_csv("piano_thick_grouped.csv")
piano_thin_data = pd.read_csv("piano_thin_grouped.csv")
pico_data = pd.read_csv("piano_pico_grouped.csv")

# Arrondir les vecteurs de temps des modules MOD1 et MOD2
mod1_data['Time'] = pd.to_datetime(mod1_data['Time']).dt.round('10s')
mod2_data['Time'] = pd.to_datetime(mod2_data['Time']).dt.round('10s')

# Convertir la colonne 'Time' des autres données en datetime
pod_data['Time'] = pd.to_datetime(pod_data['Time'])
piano_thick_data['Time'] = pd.to_datetime(piano_thick_data['Time'])
piano_thin_data['Time'] = pd.to_datetime(piano_thin_data['Time'])
pico_data['Time'] = pd.to_datetime(pico_data['Time'])

# Regrouper les données MOD1 et MOD2 par les échantillons avec le même vecteur de temps
mod1_grouped = mod1_data.groupby('Time').mean().reset_index()
mod2_grouped = mod2_data.groupby('Time').mean().reset_index()

# Fusionner les données des modules en utilisant la fonction pd.merge()
merged_data = pd.merge(pod_data, piano_thick_data, on='Time', how='outer', suffixes=('_pod', '_piano_thick'))
merged_data = pd.merge(merged_data, piano_thin_data, on='Time', how='outer', suffixes=('_piano_thin', ''))
merged_data = pd.merge(merged_data, pico_data, on='Time', how='outer', suffixes=('_pico', ''))
merged_data = pd.merge(merged_data, mod1_grouped, on='Time', how='outer', suffixes=('_mod1', ''))
merged_data = pd.merge(merged_data, mod2_grouped, on='Time', how='outer', suffixes=('_mod2', ''))

# Enregistrer les données fusionnées dans un fichier CSV
merged_data.to_csv("merged_data.csv", index=False)