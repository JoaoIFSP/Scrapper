import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Notebook
# chrome_path = r"C:\Users\M032\Desktop\chrome-win64\chrome-win64\chrome.exe"
# chromedriver_path = r"C:\Users\M032\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"
# csv_path = r"C:\Users\M032\Desktop\Scrapper\data\Scrapper-db.csv"

# Pc da firma 
# chrome_path = r"C:\Users\GEMTI\Desktop\chrome-win64\chrome-win64\chrome.exe"
# chromedriver_path = r"C:\Users\GEMTI\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"
# csv_path = r"C:\Users\GEMTI\Desktop\Scrapper\data_pechinchou\Scrapper-db.csv"

# Pc vô 
# chrome_path = r"D:\Users\User\Desktop\chrome-win64\chrome-win64\chrome.exe"
# chromedriver_path = r"D:\Users\User\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"
# csv_path = r"D:\Users\User\Desktop\Scrapper\data_pechinchou\Scrapper-db.csv"

# Caminhos atual
chrome_path = r"C:\Users\GEMTI\Desktop\chrome-win64\chrome-win64\chrome.exe"
chromedriver_path = r"C:\Users\GEMTI\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"
csv_path = r"C:\Users\GEMTI\Desktop\Scrapper\data_pechinchou\Scrapper-db.csv"

# Configurar opções do Chrome
options = webdriver.ChromeOptions()
options.binary_location = chrome_path

# Iniciar o driver com o caminho do ChromeDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# Registrar o tempo de início
start_time = time.time()

# Abrir o WhatsApp Web
driver.get("https://web.whatsapp.com")

# Aguardar o usuário escanear o QR Code
print("Escaneie o QR Code e pressione Enter...")
time.sleep(40)

try:
    # Esperar até que o título do grupo esteja disponível
    print("Aguardando a página carregar...")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//span[@dir='auto']"))
    )

    # Capturar o nome do grupo
    nome_grupo = driver.find_element(By.XPATH, "//span[@dir='auto']").text.strip()
    print(f"Nome do grupo capturado: {nome_grupo}")

    # Encontrar e clicar no botão "Dados de perfil"
    div = driver.find_element(By.XPATH, "//div[@title='Dados de perfil']")
    div.click()
    print("Botão de 'Dados de perfil' clicado!")

    # Esperar um tempo para o conteúdo carregar
    time.sleep(2)

    # Localizar a div com "Ver tudo" e clicar nela
    div_ver_tudo = driver.find_element(By.XPATH, "//div[contains(text(), 'Ver tudo')]")
    div_ver_tudo.click()
    print("Botão de 'Ver tudo' clicado!")

    # Esperar o conteúdo carregar
    time.sleep(3)

    # Agora, procurar a div com data-animate-modal-body="true"
    modal_div = driver.find_element(By.XPATH, "//div[@data-animate-modal-body='true']")
    
    telefones = set()  # Usamos um conjunto para evitar números duplicados na captura
    telefone_regex = re.compile(r"[\d\+\(\)\-\s]+")  # Permite números, +, (, ), - e espaço
    total_telefones = 0  # Contador de números encontrados

    tentativas_sem_novos_contatos = 0  # Contador para detectar fim da lista
    max_tentativas = 20  # Número de tentativas sem encontrar novos contatos antes de parar

    while tentativas_sem_novos_contatos < max_tentativas:
        # Dentro da modal, tentar encontrar os elementos de telefone visíveis
        try:
            telefone_elements = modal_div.find_elements(By.XPATH, ".//span[@dir='auto' and contains(@class, '_ao3e')]")
            
            if not telefone_elements:  # Se não encontrar nenhum telefone
                print("Nenhum telefone encontrado na iteração atual.")
            else:
                novos_encontrados = 0  # Contador de novos números encontrados nesta iteração

                for telefone in telefone_elements:
                    telefone_texto = telefone.text.strip()

                    # Verifica se o texto contém apenas caracteres válidos de telefone (números e caracteres especiais)
                    if telefone_regex.fullmatch(telefone_texto) and telefone_texto not in telefones:
                        telefones.add(telefone_texto)
                        total_telefones += 1  # Atualiza o contador
                        novos_encontrados += 1
                        print(f"Número encontrado: {telefone_texto} (Total: {total_telefones})")
                        novos_dados = pd.DataFrame({
                            "Nome": [nome_grupo] * len(telefones),
                            "Telefone-1": list(telefones),
                            "Var": ["tosend"] * len(telefones)
                        })

                        # Verificar se o arquivo CSV já existe
                        try:
                            df_existente = pd.read_csv(csv_path, encoding='utf-8-sig')

                            # Contar quantos números já existem no banco antes da remoção de duplicatas
                            duplicados = df_existente["Telefone-1"].isin(novos_dados["Telefone-1"]).sum()

                            # Concatenar os novos dados com os existentes e remover duplicatas
                            df_final = pd.concat([df_existente, novos_dados]).drop_duplicates(subset=["Telefone-1"], keep="first")
                        except FileNotFoundError:
                            df_final = novos_dados  # Se o arquivo não existir, apenas salvar os novos dados
                            duplicados = 0  # Nenhum duplicado se não há arquivo existente

                        # Salvar o DataFrame atualizado no CSV
                        df_final.to_csv(csv_path, index=False, encoding='utf-8-sig')
                
                # Se não encontrou nenhum novo número, aumenta o contador de tentativas sem novos contatos
                if novos_encontrados == 0:
                    tentativas_sem_novos_contatos += 1
                else:
                    tentativas_sem_novos_contatos = 0  # Reseta o contador se encontrar novos contatos

        except NoSuchElementException:
            # Caso o elemento não seja encontrado, apenas ignora e continua o loop
            print("Elemento de telefone não encontrado, continuando...")
        
        # Pressionar seta para baixo globalmente
        webdriver.ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(0.05)  # Pequeno delay para carregar novos contatos

    print("Fim da lista detectado!")

    # Criar um DataFrame com os dados coletados
    novos_dados = pd.DataFrame({
        "Nome": [nome_grupo] * len(telefones),
        "Telefone-1": list(telefones),
        "Var": ["tosend"] * len(telefones)
    })

    # Verificar se o arquivo CSV já existe
    try:
        df_existente = pd.read_csv(csv_path, encoding='utf-8-sig')

        # Contar quantos números já existem no banco antes da remoção de duplicatas
        duplicados = df_existente["Telefone-1"].isin(novos_dados["Telefone-1"]).sum()

        # Concatenar os novos dados com os existentes e remover duplicatas
        df_final = pd.concat([df_existente, novos_dados]).drop_duplicates(subset=["Telefone-1"], keep="first")
    except FileNotFoundError:
        df_final = novos_dados  # Se o arquivo não existir, apenas salvar os novos dados
        duplicados = 0  # Nenhum duplicado se não há arquivo existente

    # Salvar o DataFrame atualizado no CSV
    df_final.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"Dados atualizados no banco de dados CSV: {csv_path}")
    print(f"Total de números duplicados encontrados: {duplicados}")

except Exception as e:
    print("Erro:", e)

finally:
    # Registrar o tempo de término
    end_time = time.time()

    # Calcular o tempo de execução total
    total_time = end_time - start_time
    print(f"Tempo total de execução: {total_time:.2f} segundos")

    print(f"Total de {total_telefones} números encontrados e processados.")
    print(nome_grupo)

    # Fechar o navegador após a execução
    driver.quit()
