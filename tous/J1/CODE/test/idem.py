import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Chargement des fichiers
df_data = pd.read_csv(r'C:\Users\Z35\Desktop\projet_python\DATA\data.csv')
df_meg_raw = pd.read_csv(r'C:\Users\Z35\Desktop\projet_python\DATA\meg.csv', encoding='latin1')

# Colonnes client dans chaque fichier
client_col_meg = 'Numéro du Client :'
client_col_data = 'NoClient'

# Création de la liste des clients dans MEG
meg_clients = set(df_meg_raw[client_col_meg].unique())

# Fonction pour indiquer présence dans MEG
def is_in_meg(client):
    return 1 if client in meg_clients else 0

# Ajout de la colonne 'meg' dans df_data
df_data['meg'] = df_data[client_col_data].apply(is_in_meg)

# Sauvegarder le dataframe modifié
df_data.to_csv(r'C:\Users\Z35\Desktop\projet_python\DATA\data_with_meg.csv', index=False)

# 1. Boxplot de temps_total selon meg
plt.figure(figsize=(8,6))
sns.boxplot(x='meg', y='temps_total', data=df_data)
plt.title('Boxplot de temps_total selon présence dans MEG')
plt.xlabel('meg (0 = absent, 1 = présent)')
plt.ylabel('temps_total')
plt.show()

# 2. Test t pour comparer les moyennes
group0 = df_data[df_data['meg'] == 0]['temps_total'].dropna()
group1 = df_data[df_data['meg'] == 1]['temps_total'].dropna()

stat, pvalue = ttest_ind(group0, group1, equal_var=False)  # test de Welch

print(f"Test t de Welch : t-statistic = {stat:.4f}, p-value = {pvalue:.4f}")
if pvalue < 0.05:
    print("Différence significative entre les groupes meg=0 et meg=1")
else:
    print("Pas de différence significative entre les groupes meg=0 et meg=1")

# 3. Régression linéaire simple : temps_total ~ meg
model = smf.ols('temps_total ~ meg', data=df_data).fit()
print(model.summary())
