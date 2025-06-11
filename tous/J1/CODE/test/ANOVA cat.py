from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

# === 1. Charger les données ===
fichier_csv = r'C:\Users\Z35\Desktop\projet_python\DATA\data.csv'
df = pd.read_csv(fichier_csv)

# === 2. Nettoyer les données ===
# Remplacer les -1 par NaN
df.replace(-1, pd.NA, inplace=True)

# Créer une variable temps_total à partir des colonnes de temps disponibles
cols_temps = [col for col in df.columns if col.startswith("temps_code")]
df['temps_total'] = df[cols_temps].sum(axis=1)

# Filtrer les colonnes nécessaires pour le test ANOVA
df_anova = df[['temps_total', 'forme_juridique']].dropna()

# === 3. Test ANOVA ===
# Regrouper les valeurs de temps_total par forme_juridique
groupes = [group['temps_total'].values for _, group in df_anova.groupby('forme_juridique')]

# Appliquer le test ANOVA
f_stat, p_value = stats.f_oneway(*groupes)

print("=== Résultats du test ANOVA ===")
print(f"Statistique F : {f_stat:.4f}")
print(f"p-value       : {p_value:.4f}")

if p_value < 0.05:
    print("👉 Il existe une différence significative du temps total selon la forme juridique.")
else:
    print("👉 Aucune différence significative détectée selon la forme juridique.")

# === 4. Visualisation des résultats ===
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_anova, x='forme_juridique', y='temps_total')
plt.xticks(rotation=45)
plt.title('Distribution du temps total par forme juridique')
plt.tight_layout()
plt.show()
