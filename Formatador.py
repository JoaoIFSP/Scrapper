import pandas as pd
import re

def limpar_numeros(telefone, contador_duplicatas):
# Remove caracteres não numéricos e elimina números duplicados mantendo a ordem.
    if pd.notna(telefone):
        telefone_limpo = re.sub(r'\D', '', telefone)
        numeros = re.findall(r'\d+', telefone_limpo)
        numeros_unicos = sorted(set(numeros), key=numeros.index)
        contador_duplicatas[0] += len(numeros) - len(numeros_unicos)
        return ','.join(numeros_unicos)
    return telefone

def modificar_nome(_):
#    Substitui todos os nomes pelo valor fixo 'Punheteiros'.
    return "Punheteiro"

def processar_csv(arquivo_entrada, arquivo_saida):
#    Carrega, processa e salva o CSV com limpeza de telefone e modificação de nome.
    try:
        df = pd.read_csv(arquivo_entrada, dtype=str)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return

    # Verifica se as colunas existem
    if "Telefone-1" not in df.columns:
        print("Coluna 'Telefone-1' não encontrada no arquivo.")
        return
    if "Nome" not in df.columns:
        print("Coluna 'Nome' não encontrada no arquivo.")
        return

    # Contador de números duplicados removidos
    contador_duplicatas = [0]

    # Aplica as transformações
    df["Telefone-1"] = df["Telefone-1"].apply(lambda x: limpar_numeros(x, contador_duplicatas))
    df["Nome"] = df["Nome"].apply(modificar_nome)  # Todos os nomes serão "Punheteiros"

    # Salva o novo CSV
    df.to_csv(arquivo_saida, index=False)
    
    print(f"Arquivo salvo como '{arquivo_saida}'.")
    print(f"Total de números duplicados removidos: {contador_duplicatas[0]}")

# Caminhos do arquivo
arquivo_entrada = r"C:\Users\GEMTI\Desktop\Scrapper\data_virgens\Scrapper-db.csv"
arquivo_saida = r"C:\Users\GEMTI\Desktop\Scrapper\data_virgens\Clear_data\Scrapper-db-limpo.csv"

# Executa a função
processar_csv(arquivo_entrada, arquivo_saida)
