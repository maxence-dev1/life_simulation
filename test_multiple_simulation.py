import main, pandas
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.widgets import Button, RadioButtons
import numpy as np
import pandas as pd
import csv

#Ici
liste_df = []
liste_liste_food = []


#But pour ML, remplir csv avec environ 5000 lignes. Faire varier le ratio food et le nombre de minos sur X simulations + rajouter food collected et distance_traveleld


big_data = []

first = True
for i in range(10):
    for nb_minos in range(10,500,30): 
        for ratio in range(1,20,4):
            res = main.main(nb_minos,1/ratio)
            df_sim = res[0]
            df_sim["nb_minos"] = nb_minos
            df_sim["ratio_food"] = 1/ratio
            big_data.append(df_sim)
            print(f"simulation avec {nb_minos} minos et 1/{ratio} ratio. time : {res[0]["time_lived"].max()}")


final_big_df = pd.concat(big_data)
final_big_df.to_csv("data.csv",header= True, index=False)



