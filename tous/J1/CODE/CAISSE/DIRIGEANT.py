import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# === 1. Chargement des données ===
fichier_csv = r'C:\Users\Z35\Desktop\projet_python\DATA\data.csv'
df = pd.read_csv(fichier_csv)
df.replace(-1, pd.NA, inplace=True)

# === 2. Construction de 'temps_total' ===
cols_temps = [col for col in df.columns if col.startswith("temps_code")]
df['temps_total'] = df[cols_temps].sum(axis=1)

# === 3. Sélection des variables catégorielles pertinentes ===
# On garde les colonnes de type object ou catégorie avec peu de modalités (entre 2 et 10)
colonnes_categorique = [
    col for col in df.select_dtypes(include='object').columns
    if 2 <= df[col].nunique() <= 10 and df[col].notna().sum() > 30
]

# === 4. Test ANOVA sur chaque variable catégorielle ===
resultats_anova = []

for col in colonnes_categorique:
    df_temp = df[[col, 'temps_total']].dropna()
    groupes = [grp['temps_total'].values for _, grp in df_temp.groupby(col)]
    if len(groupes) >= 2:
        f_stat, p_value = stats.f_oneway(*groupes)
        resultats_anova.append((col, f_stat, p_value))

# Trier les résultats par p-value
resultats_anova.sort(key=lambda x: x[2])
top_resultats = resultats_anova[:5]

# === 5. Affichage propre des résultats ===
print("\n=== Résultats ANOVA pertinents (top 5) ===\n")
for col, f, p in top_resultats:
    sig = "✅" if p < 0.05 else "❌"
    print(f"{sig} {col:<30} | F = {f:.2f} | p = {p:.4f}")

# === 6. Visualisation (max 3 plots) ===
for col, f, p in top_resultats[:3]:
    if p < 0.05:
        plt.figure(figsize=(10, 5))
        sns.boxplot(data=df[[col, 'temps_total']].dropna(), x=col, y='temps_total')
        plt.title(f"temps_total selon {col} (p = {p:.4f})", fontsize=14)
        plt.xticks(rotation=25)
        plt.xlabel(col)
        plt.ylabel("temps_total")
        plt.tight_layout()
        plt.show()
