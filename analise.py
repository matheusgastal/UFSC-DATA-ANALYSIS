import pandas as pd  

df = pd.read_json("cortes_ufsc_2025.json")                 
df_pesos = pd.read_json("pesos_ufsc.json")   

#uma verdadeira por questão, teriamos esse resultado:
portugues = [1.0, 0.6, 0.6, 0.571, 0.571, 0.75, 0.667, 0.8, 0.8, 0.667, 0.833, 0.5]
segunda_lingua = [0.667, 0.667, 0.667, 0.833, 0.8, 0.8, 0.6, 1.0]
matematica = [0.8, 0.8, 0.6, 0.6, 0.6, 0.4, 0.8, 0.6, 0.8, 0.6]
biologia = [0.6, 0.714, 0.714, 0.6, 0.833, 0.571, 0.667, 0.667, 0.571, 0.429]
ciencias_humanas = [0.714, 0.833, 0.667, 0.8, 0.571, 0.714, 0.571, 0.667, 0.6, 0.8, 0.667, 0.714, 0.833, 0.833, 0.667, 0.667, 0.571, 0.571, 0.667, 0.667]
fisica = [0.6, 0.6, 0.667, 0.714, 0.667, 0.667, 0.6, 0.667, 0.8, 0.333]
quimica = [0.833, 0.833, 0.667, 0.667, 0.833, 0.571, 0.8, 0.4, 0.833, 0.833]
nota_red = 7
nota_discursivas = 5

notas_brutas = {
    "PLI": sum(portugues),       
    "SLI": sum(segunda_lingua), 
    "MTM": sum(matematica),      
    "BLG": sum(biologia),        
    "QMC": sum(quimica),         
    "FSC": sum(fisica),          
    "CHS": sum(ciencias_humanas),            
    "RDC": nota_red,                   
    "DSC": nota_discursivas                    
}



for i in range(2,6):
    df = pd.read_json(f"cortes_ufsc_202{i}.json")                 
    df_pesos = pd.read_json("pesos_ufsc.json")   

    # função auxiliar
    def to_float_safe(x):
        try:
            return float(str(x).replace(",", "."))
        except:
            return 0.0

    # calcular nota final por curso
    hash_cursos = {}
    for j in range(len(df_pesos)):
        codigo = str(df_pesos.loc[j, "Código"])
        pesos = df_pesos.loc[j, "pesos"]   # já vem como dict
        pmc = to_float_safe(df_pesos.loc[j, "PMC"])
        # cálculo da média ponderada
        nota_final = sum(notas_brutas[m] * to_float_safe(pesos.get(m, 0)) for m in notas_brutas)

        curso_match = df[df["Código"].astype(str) == codigo]
        if not curso_match.empty:
            curso_nome = curso_match.iloc[0]["Curso"]
            hash_cursos[codigo] = {
                "Nome": curso_nome,
                "nota_final": nota_final * 100 / pmc if pmc > 0 else 0
            }

    # verificar aprovação
    passaria = 0
    passaria_primeiro = 0
    nao_passaria = 0
    nao_passa = []
    diff = []
    for k in range(len(df)):
        codigo = str(df.loc[k, "Código"])  
        nome = df.loc[k, "Curso"]

        if codigo not in hash_cursos:
            continue  # pular cursos sem peso/PMC

        nota_final = hash_cursos[codigo]["nota_final"]
        nota_primeiro = float(df.loc[k, "Nota_Primeiro"])
        nota_ultimo = float(df.loc[k, "Nota_Último"])

        if nota_final > nota_primeiro:
            passaria += 1
            passaria_primeiro += 1
        elif nota_final > nota_ultimo:
            passaria += 1
        else:
            diferenca = nota_ultimo - nota_final
            diff.append(diferenca)
            nao_passa.append(f"{nome}")
            nao_passaria += 1
    print("=======================================================================")
    print(f"ANO DE 202{i}")
    print(f"Não passaria em {nao_passaria} cursos:")
    for z in range(len(nao_passa)):
        print(f"  -{nao_passa[z]} por {str(round(diff[z],2))} pontos")
    print(f"Passaria em {passaria} cursos")
    print(f"Passaria em primeiro lugar em {passaria_primeiro} cursos")
    if(i == 5):
        print("=======================================================================")