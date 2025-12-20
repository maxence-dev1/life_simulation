import main, pandas

liste_df = []
liste_liste_food = []

for i in range(2):
    res = main.main(100,1/5, 2000, 1000)
    liste_df.append(res[0])
    liste_liste_food.append(res[1])
    print(f"simulation {i+1} finie")




df_resistance = pandas.concat(
    df["resistance"] for df in liste_df).groupby(level=0)

print("moyenne : ", df_resistance.mean().mean())