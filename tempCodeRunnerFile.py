for nb_minos in range(10,200,30): 
    #     for ratio in range(1,20,4):
    #         res = main(nb_minos,1/ratio)
    #         df_sim = res[0]
    #         df_sim["nb_minos"] = nb_minos
    #         df_sim["ratio_food"] = 1/ratio
    #         big_data.append(df_sim)
    #         print(f"simulation avec {nb_minos} minos et 1/{ratio} ratio. time : {res[0]["time_lived"].max()}")