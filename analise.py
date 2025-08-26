import pandas as pd 
import json

with open("notas_por_ano.json", "r", encoding="utf-8") as f:
    notas_anuais = json.load(f)

df_pesos = pd.read_json("pesos_ufsc.json")


RDC = 8 #redacao (max 10)
DSC = 7. #descritivas da prova (max 10)

# função auxiliar
def to_float_safe(x):
    try:
        return float(str(x).replace(",", "."))
    except:
        return 0.0

for i in range(2,6):
    ano = f"202{i}"
    df = pd.read_json(f"cortes_ufsc_{ano}.json")

    notas_brutas = notas_anuais[ano].copy()
    notas_brutas["RDC"] = RDC
    notas_brutas["DSC"] = DSC

    hash_cursos = {}
    for j in range(len(df_pesos)):
        codigo = str(df_pesos.loc[j, "Código"])
        pesos = df_pesos.loc[j, "pesos"]   
        pmc = to_float_safe(df_pesos.loc[j, "PMC"])
        nota_final = sum(
            notas_brutas[m] * to_float_safe(pesos.get(m, 0))
            for m in notas_brutas
        )

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
            continue

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
            nao_passa.append(nome)
            nao_passaria += 1

    print("=======================================================================")
    print(f"ANO DE {ano}")
    print(f"Não passaria em {nao_passaria} cursos:")
    for z in range(len(nao_passa)):
        print(f"  - {nao_passa[z]} por {round(diff[z],2)} pontos")
    print(f"Passaria em {passaria} cursos")
    print(f"Passaria em primeiro lugar em {passaria_primeiro} cursos")
    if i == 5:
        print("=======================================================================")
