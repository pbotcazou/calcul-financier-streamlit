import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Charger les données
fichier_csv = r'C:\Users\Z35\Desktop\projet_python\data.csv'
df = pd.read_csv(fichier_csv)
df.replace(-1, pd.NA, inplace=True)
df_numeric = df.select_dtypes(include='number').dropna()

# Corrélations
corr_matrix = df_numeric.corr()
paires = []
seen = set()

for col1 in corr_matrix.columns:
    for col2 in corr_matrix.columns:
        if col1 != col2 and ('temps' in col1 or 'temps' in col2):
            pair = tuple(sorted((col1, col2)))
            if pair not in seen:
                seen.add(pair)
                corr = corr_matrix.loc[col1, col2]
                if abs(corr) > 0.75:
                    paires.append((pair[0], pair[1], corr))

# Interface avec Tkinter
root = tk.Tk()
root.title("Graphiques de régression (scrollable)")

canvas_frame = tk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(canvas_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas = tk.Canvas(canvas_frame, yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=canvas.yview)

plot_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=plot_frame, anchor="nw")

# Création des graphes dans la fenêtre
fig, axes = plt.subplots(len(paires), 1, figsize=(10, 5 * len(paires)))
if len(paires) == 1:
    axes = [axes]

for i, (x, y, corr) in enumerate(paires):
    sns.regplot(x=x, y=y, data=df_numeric, ax=axes[i], line_kws={'color': 'red'})
    axes[i].set_title(f"{x} vs {y} (corr = {corr:.2f})")
    axes[i].set_xlabel(x)
    axes[i].set_ylabel(y)

fig.tight_layout()

canvas_fig = FigureCanvasTkAgg(fig, master=plot_frame)
canvas_fig.draw()
canvas_fig.get_tk_widget().pack()

# Mise à jour du scroll
plot_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()
