import pandas as pd

# Charger le fichier CSV dans un DataFrame
fichier_csv = r'C:\Users\Z35\Desktop\projet_python\data.csv'  # Assure-toi que le chemin est correct
df = pd.read_csv(fichier_csv)


# Statistiques descriptives pour les colonnes numériques
#   print(df.describe())


# Matrice de corrélation
import seaborn as sns
import matplotlib.pyplot as plt

# Sélectionner uniquement les colonnes numériques
numeric_columns = df.select_dtypes(include=['number'])

# Calculer la matrice de corrélation
plt.figure(figsize=(12, 8))
sns.heatmap(numeric_columns.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Matrice de Corrélation')
plt.show()


