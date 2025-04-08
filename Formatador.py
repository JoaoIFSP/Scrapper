import pandas as pd
import re

def limpar_coluna_csv(arquivo_entrada, arquivo_saida):
    # Lê o arquivo CSV
    df = pd.read_csv(arquivo_entrada, dtype=str)

    # Verifica se a coluna "Telefone-1" existe
    if "Telefone-1" not in df.columns:
        print("Coluna 'Telefone-1' não encontrada no arquivo.")
        return

    total_duplicatas = 0  # Contador de números duplicados removidos

    # Função para limpar e remover números duplicados
    def limpar_numeros(telefone):
        nonlocal total_duplicatas  # Permite modificar a variável externa
        if pd.notna(telefone):
            # Remove tudo que não for número
            telefone_limpo = re.sub(r'\D', '', telefone)
            # Separa números individuais (caso haja múltiplos números na mesma célula)
            numeros = re.findall(r'\d+', telefone_limpo)
            # Remove duplicatas mantendo a ordem original
            numeros_unicos = sorted(set(numeros), key=numeros.index)
            # Contabiliza as duplicatas removidas
            total_duplicatas += len(numeros) - len(numeros_unicos)
            return ','.join(numeros_unicos)
        return telefone

    # Aplica a função na coluna
    df["Telefone-1"] = df["Telefone-1"].apply(limpar_numeros)

    # Salva o novo CSV
    df.to_csv(arquivo_saida, index=False)

    print(f"Arquivo salvo como '{arquivo_saida}'.")
    print(f"Total de números duplicados removidos: {total_duplicatas}")

# Caminhos do arquivo
arquivo_entrada = r"C:\Users\GEMTI\Desktop\Scrapper\data_virgens\Scrapper-db.csv"
arquivo_saida = r"C:\Users\GEMTI\Desktop\Scrapper\data_virgens\Clear_data\Scrapper-db-limpo.csv"

# Executa a função
limpar_coluna_csv(arquivo_entrada, arquivo_saida)
