import pandas as pd
for i in range(2,6):
    df = pd.read_json(f"cortes_ufsc_202{i}.json")                 
    df_pesos = pd.read_json("pesos_ufsc.json")   
    print(df_pesos.shape)