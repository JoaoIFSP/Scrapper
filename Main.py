import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

chrome_path = r"C:\Users\GEMTI\Desktop\chrome-win64\chrome-win64\chrome.exe"
chromedriver_path = r"C:\Users\GEMTI\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"
csv_path = r"C:\Users\GEMTI\Desktop\Scrapper\data_pechinchou\Scrapper-db.csv"
#csv_path = r"C:\Users\GEMTI\Desktop\Scrapper\data_virgens\Scrapper-db.csv"
#csv_path = r"C:\Users\GEMTI\Desktop\Scrapper\data_promos\Scrapper-db.csv"


# O CÓDIGO NÃO SERÁ COMENTADO PQ MEU PÊNIS É MUITO GRANDE
# muito.



options = webdriver.ChromeOptions()
options.binary_location = chrome_path

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

start_time = time.time()

driver.get("https://web.whatsapp.com")

print("Escaneie o QR Code e pressione Enter...")
time.sleep(40)

while True:

    try:
        print("Aguardando a página carregar...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//span[@dir='auto']"))
        )

        nome_grupo = driver.find_element(By.XPATH, "//span[@dir='auto']").text.strip()
        print(f"Nome do grupo capturado: {nome_grupo}")

        driver.find_element(By.XPATH, "//div[@title='Dados de perfil']").click()
        print("Botão de 'Dados de perfil' clicado!")

        time.sleep(2)

        driver.find_element(By.XPATH, "//div[contains(text(), 'Ver tudo')]").click()
        print("Botão de 'Ver tudo' clicado!")

        time.sleep(3)

        modal_div = driver.find_element(By.XPATH, "//div[@data-animate-modal-body='true']")

        telefones = set()
        telefone_regex = re.compile(r"[\d\+\(\)\-\s]+")
        total_telefones = 0
        tentativas_sem_novos_contatos = 0
        max_tentativas = 20

        while tentativas_sem_novos_contatos < max_tentativas:
            try:
                telefone_elements = modal_div.find_elements(By.XPATH, ".//span[@dir='auto' and contains(@class, '_ao3e')]")
                
                novos_encontrados = 0
                for telefone in telefone_elements:
                    try:
                        telefone_texto = telefone.text.strip()

                        if telefone_regex.fullmatch(telefone_texto) and telefone_texto not in telefones:
                            telefones.add(telefone_texto)
                            total_telefones += 1
                            novos_encontrados += 1
                            print(f"Número encontrado: {telefone_texto} (Total: {total_telefones})")
                            novos_dados = pd.DataFrame({
                                "Nome": [nome_grupo] * len(telefones),
                                "Telefone-1": list(telefones),
                                "Var": ["tosend"] * len(telefones)
                            })

                            try:
                                df_existente = pd.read_csv(csv_path, encoding='utf-8-sig')
                                df_final = pd.concat([df_existente, novos_dados]).drop_duplicates(subset=["Telefone-1"], keep="first")
                            except FileNotFoundError:
                                df_final = novos_dados  

                            df_final.to_csv(csv_path, index=False, encoding='utf-8-sig')
                    
                    except StaleElementReferenceException:

                        continue  

                if novos_encontrados == 0:
                    tentativas_sem_novos_contatos += 1
                else:
                    tentativas_sem_novos_contatos = 0

            except NoSuchElementException:
                print("Elemento de telefone não encontrado, continuando...")


            webdriver.ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
            time.sleep(0.05)  

        print("Fim da lista detectado!")


        print(f"Dados salvos no banco de dados CSV: {csv_path}")

    except Exception as e:
        print("Erro:", e)

    finally:
        end_time = time.time()
        print(f"Tempo total de execução: {end_time - start_time:.2f} segundos")
        print(f"Total de {total_telefones} números encontrados e processados.")

        cabo = input("Já acabou zé?")
        if cabo == "0":
            print("Vamos rodar dnv então")
        else:
            break

print("ACABO")
    
driver.quit()
    # BUCETINHA GAMES BRASIL #