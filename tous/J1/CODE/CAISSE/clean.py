import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Charger les données
df = pd.read_csv(r'C:\Users\Z35\Desktop\projet_python\DATA\data1.csv')

# Colonnes à vérifier
cols = ['temps_code5', 'nb_lignes_produits', 'nb_lignes_charges', 'nb_lignes_banque']

for col in cols:
    df = df[(df[col] != 0) & (df[col] != -1)]

# Compter les 0 et -1
for col in cols:
    nb_zeros = (df[col] == 0).sum()
    nb_minus_ones = (df[col] == -1).sum()
    print(f"{col} : {nb_zeros} zéros | {nb_minus_ones} valeurs à -1")


# Conserver uniquement les colonnes utiles et supprimer les lignes NA
df_model = df[cols].dropna()

# === 3. Fonction de régression simple ===
def simple_regression(df, x_var, y_var='temps_code5', log=False):
    df_clean = df.copy()

    if log:
        df_clean = df_clean[df_clean[x_var] > 0].copy()  # sécurité supplémentaire
        df_clean[f'log_{x_var}'] = np.log(df_clean[x_var])
        X = df_clean[[f'log_{x_var}']]
        x_label = f"log({x_var})"
    else:
        X = df_clean[[x_var]]
        x_label = x_var

    y = df_clean[y_var]
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)

    # Affichage console
    print(f"\n--- Régression : {y_var} ~ {x_label} ---")
    print(f"Coef       : {model.coef_[0]:.4f}")
    print(f"Intercept  : {model.intercept_:.4f}")
    print(f"R²         : {r2:.4f}")

    # Affichage graphique
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x=X.iloc[:, 0], y=y)
    sns.lineplot(x=X.iloc[:, 0], y=y_pred, color='red')
    plt.title(f"{y_var} ~ {x_label}")
    plt.xlabel(x_label)
    plt.ylabel(y_var)
    plt.tight_layout()
    plt.show()

# === 4. Régressions simples ===
simple_regression(df_model, 'nb_lignes_charges')
simple_regression(df_model, 'nb_lignes_banque')
simple_regression(df_model, 'nb_lignes_produits')

simple_regression(df_model, 'nb_lignes_charges', log=True)
simple_regression(df_model, 'nb_lignes_banque', log=True)
simple_regression(df_model, 'nb_lignes_produits', log=True)

# === 5. Régression multiple ===
X_multi = df_model[['nb_lignes_produits', 'nb_lignes_banque', 'nb_lignes_charges']]
y_multi = df_model['temps_code5']

model_multi = LinearRegression()
model_multi.fit(X_multi, y_multi)
y_pred_multi = model_multi.predict(X_multi)
r2_multi = r2_score(y_multi, y_pred_multi)

# Résumé du modèle
a, b, c = model_multi.coef_
d = model_multi.intercept_

print("\n=== Régression multiple : temps_code5 ~ nb_produits + nb_banque + nb_charges ===")
print("Equation :")
print(f"temps_code5 = {a:.4f} * nb_produits + {b:.4f} * nb_banque + {c:.4f} * nb_charges + {d:.4f}")
print(f"✅ R² global : {r2_multi:.4f}")

# === 6. Visualisation du modèle multiple ===
plt.figure(figsize=(6, 4))
sns.scatterplot(x=y_multi, y=y_pred_multi)
plt.plot([y_multi.min(), y_multi.max()], [y_multi.min(), y_multi.max()], '--', color='red')
plt.xlabel("Temps réel (code5)")
plt.ylabel("Temps prédit (modèle multiple)")
plt.title("Temps réel vs Temps prédit — Régression multiple")
plt.tight_layout()
plt.show()
