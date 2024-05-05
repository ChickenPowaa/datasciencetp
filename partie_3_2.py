import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define a function to calculate the average signature
def averageSignature(instances, total_length):
    # Concaténer toutes les instances d'activités
    all_activities = pd.concat(instances)
    
    # Filtrer les colonnes numériques
    numeric_cols = all_activities.select_dtypes(include=[np.number]).columns
    
    # Remplacer les valeurs non numériques par NaN
    all_activities[numeric_cols] = all_activities[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    # Remplacer les NaN par la moyenne de chaque colonne, en excluant les colonnes de date
    all_activities[numeric_cols] = all_activities[numeric_cols].fillna(all_activities[numeric_cols].mean())
    
    # Nombre d'échantillons par activité
    num_samples = len(instances)
    
    # Normaliser la longueur de chaque instance d'activité
    normalized_activities = []
    for instance in instances:
        instance_length = len(instance)
        normalized_instance = instance.copy()
        if instance_length < total_length:
            # Si l'instance est plus courte, répéter les données jusqu'à la longueur totale
            num_repeats = total_length // instance_length
            remainder = total_length % instance_length
            normalized_instance = pd.concat([instance] * num_repeats + [instance.iloc[:remainder]], ignore_index=True)
        elif instance_length > total_length:
            # Si l'instance est plus longue, tronquer jusqu'à la longueur totale
            normalized_instance = instance.iloc[:total_length]
        normalized_activities.append(normalized_instance)
    
    # Convertir les colonnes en nombres si possible
    normalized_activities = [instance.apply(pd.to_numeric, errors='coerce') for instance in normalized_activities]
    
    # Concaténer et calculer la moyenne des instances normalisées
    average_activity = pd.concat(normalized_activities).mean()
    
    return average_activity


# Charger le dataset database_with_activities.csv
labelled_dataset = pd.read_csv("database_with_activities.csv")

# Créer une liste pour stocker les instances par label
instances_by_label = [[] for _ in range(1, 11)]
tags = ["AS1", "Oeuf", "SdB", "Asp", "Nett", "Saber", "Bougie", "Aera", "BricoP", "BricoC"]

# Diviser le dataset par label
for label in range(1, 11):
    instances_by_label[label - 1] = labelled_dataset[labelled_dataset['Activity'] == tags[label - 1]].drop(columns='Activity')

# Tags et noms de capteurs
sensor_names = labelled_dataset.drop(columns='Activity').columns

# Calculer les moyennes des signatures pour chaque activité
averages = []
for tag, instances_for_label in zip(tags, instances_by_label):
    print(f"Calcul de la moyenne de la signature pour l'activité : {tag}")
    # Convertir le DataFrame instances_for_label en une liste de DataFrames
    instances_list = [instances_for_label]
    avg_signature = averageSignature(instances_list, len(instances_for_label))
    averages.append(avg_signature)

# Créer un graphique pour chaque activité
for tag, avg_signature in zip(tags, averages):
    # Extraire la moyenne de la réponse de chaque activité
    avg_response = avg_signature.values
    
    # Créer un nouveau graphique
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Tracer la moyenne de la réponse de chaque activité sur l'axe y supérieur
    ax1.plot(sensor_names, avg_response, marker='o', color='b')
    
    # Ajouter des titres et des labels pour l'axe y supérieur
    ax1.set_title(f"Average Response of {tag} on Sensor's Measurement")
    ax1.set_xlabel("Sensor Measurement")
    ax1.set_ylabel("Average Response", color='b')
    
    # Faire pivoter les noms des capteurs pour une meilleure lisibilité
    ax1.tick_params(axis='x', rotation=45)
    
    # Afficher la grille pour l'axe y supérieur
    ax1.grid(True)

    # Créer un axe y inférieur partagé avec l'axe y supérieur
    ax2 = ax1.twiny()
    
    # Tracer les échantillons sur l'axe y inférieur
    ax2.plot(range(len(avg_response)), avg_response, color='r', alpha=0)
    
    # Ajouter des labels et masquer les ticks de l'axe y inférieur
    ax2.set_xlabel("Samples")
    ax2.tick_params(axis='x', bottom=False)

    # Afficher le graphique
    plt.tight_layout()
    plt.show()
