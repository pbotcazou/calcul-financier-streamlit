from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Charger les données
fichier_csv = r'C:\Users\Z35\Desktop\projet_python\data.csv'  # Assurez-vous que le chemin est correct
df = pd.read_csv(fichier_csv)

# Remplacer les valeurs -1 par NaN pour éviter les anomalies
df.replace(-1, pd.NA, inplace=True)

# Sélectionner uniquement les colonnes numériques et supprimer les lignes avec des valeurs manquantes
df_numeric = df.select_dtypes(include='number').dropna()

# Sélectionner les variables d'entrée (code1, code3, code4, code5, code6) et la cible (temps_total)
X = df[['code1', 'code3', 'code4', 'code5', 'code6']]  # Variables explicatives
y = df['temps_total']  # Variable cible

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normaliser les données (StandardScaler)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Créer et entraîner le modèle de régression linéaire
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Effectuer des prédictions sur l'ensemble de test
y_pred = model.predict(X_test_scaled)

# Afficher les coefficients du modèle
coefficients = model.coef_
print("Coefficients du modèle :")
for i, coef in enumerate(coefficients):
    print(f"{X.columns[i]}: {coef}")

# Visualisation des coefficients
plt.figure(figsize=(10, 6))
sns.barplot(x=X.columns, y=coefficients, palette='viridis')
plt.title('Coefficients du modèle de régression linéaire', fontsize=14)
plt.xlabel('Variables', fontsize=12)
plt.ylabel('Coefficients', fontsize=12)
plt.grid(True)
plt.show()

# Visualiser la comparaison entre valeurs réelles et prédites
plt.figure(figsize=(12, 6))
plt.plot(y_test.index, y_test, label='Valeurs réelles', color='blue', marker='o', linestyle='-', markersize=4)
plt.plot(y_test.index, y_pred, label='Valeurs prédites', color='red', linestyle='--', linewidth=2)
plt.title('Comparaison entre valeurs réelles et prédites', fontsize=14)
plt.xlabel('Index des données', fontsize=12)
plt.ylabel('Temps Total', fontsize=12)
plt.legend()
plt.grid(True)

# Ajuster dynamiquement l'échelle de l'axe des ordonnées
min_value = min(y_test.min(), y_pred.min()) - 10
max_value = max(y_test.max(), y_pred.max()) + 10
plt.ylim(min_value, max_value)

# Afficher le graphique
plt.show()

# Afficher les métriques d'évaluation du modèle
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nÉvaluation du modèle :")
print(f"Erreur absolue moyenne (MAE) : {mae:.2f}")
print(f"Erreur quadratique moyenne (MSE) : {mse:.2f}")
print(f"R² : {r2:.2f}")
