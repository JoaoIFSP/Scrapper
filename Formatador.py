import pandas as pd
import re

# eu tenho fimmoze
arquivo_entrada = r"C:\Users\GEMTI\Desktop\Scrapper\data_pechinchou\Scrapper-db.csv"
arquivo_saida = r"C:\Users\GEMTI\Desktop\Scrapper\data_pechinchou\Clear_data\Scrapper-db-limpo.csv"

def limpar_numeros(telefone, contador_duplicatas):
    if pd.notna(telefone):
        telefone_limpo = re.sub(r'\D', '', telefone)
        numeros = re.findall(r'\d+', telefone_limpo)
        numeros_unicos = sorted(set(numeros), key=numeros.index)
        contador_duplicatas[0] += len(numeros) - len(numeros_unicos)
        return ','.join(numeros_unicos)
    return telefone

def modificar_nome(_):
    return "Punheteiro"

def processar_csv(arquivo_entrada, arquivo_saida):

    try:
        df = pd.read_csv(arquivo_entrada, dtype=str)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return

    if "Telefone-1" not in df.columns:
        print("Coluna 'Telefone-1' não encontrada no arquivo.")
        return
    if "Nome" not in df.columns:
        print("Coluna 'Nome' não encontrada no arquivo.")
        return

    contador_duplicatas = [0]

    df["Telefone-1"] = df["Telefone-1"].apply(lambda x: limpar_numeros(x, contador_duplicatas))
    df["Nome"] = df["Nome"].apply(modificar_nome) 
    df.to_csv(arquivo_saida, index=False)

    print(f"Arquivo salvo como '{arquivo_saida}'.")
    print(f"Total de números duplicados removidos: {contador_duplicatas[0]}")

processar_csv(arquivo_entrada, arquivo_saida)
