import main, pandas

liste_df = []
liste_liste_food = []

for i in range(100):
    res = main.main(100,0)
    liste_df.append(res[0])
    liste_liste_food.append(res[1])
    print(f"simulation {i+1} finie")




df_resistance = pandas.concat(
    df["resistance"] for df in liste_df).groupby(level=0)

print("moyenne : ", df_resistance.mean().mean())