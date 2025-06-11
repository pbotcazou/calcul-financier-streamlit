import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Charger le fichier CSV dans un DataFrame
fichier_csv = r'C:\Users\Z35\Desktop\projet_python\data.csv'
df = pd.read_csv(fichier_csv)

# Remplacer les valeurs -1 par NaN
df.replace(-1, pd.NA, inplace=True)

# Convertir les dates en datetime
df['RefDate'] = pd.to_datetime(df['RefDate'], errors='coerce')
df['AutoCloseDate'] = pd.to_datetime(df['AutoCloseDate'], errors='coerce')

# Ajouter une colonne pour l'année
df['year'] = df['RefDate'].dt.year

# Filtrer uniquement les années entre 2018 et 2023
df_filtered = df[(df['year'] >= 2018) & (df['year'] <= 2023)]

# Regrouper et compter les enregistrements par année
df_yearly = df_filtered.groupby('year').size()

# Tracer la tendance
plt.figure(figsize=(10, 6))
df_yearly.plot(kind='line', marker='o')
plt.title("Nombre d'enregistrements par année (2018–2023)")
plt.xlabel("Année")
plt.ylabel("Nombre d'enregistrements")
plt.grid(True)
plt.xticks(df_yearly.index)  # Afficher uniquement les années filtrées
plt.tight_layout()
plt.show()
