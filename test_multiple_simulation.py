import main, pandas
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.widgets import Button, RadioButtons
import numpy as np
#Ici
liste_df = []
liste_liste_food = []

best_list = []
worst_list = []


for nb_minos in range(2,20): #Je veux récuperer le meilleur et le pire de chaque simulation pour voir les avantages et tout 
    for ratio in range(1,10):
        res = main.main(nb_minos,1/ratio, 2500, 1400)
        best_list.append(res[0].loc[res[0]["time_lived"].idxmax()])
        worst_list.append(res[0].loc[res[0]["time_lived"].idxmin()])
        print(f"simulation avec {nb_minos} minos et 1/{ratio} ratio. best_time : {res[0]["time_lived"].max()}, worst_time : {res[0]["time_lived"].min()}")


resistance_best = [float((df["time_lived"] for df in best_list))]
resistance_worst = [float((df["time_lived"] for df in worst_list))] 

print(resistance_best)
print(resistance_worst)