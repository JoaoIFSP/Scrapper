import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Caminhos personalizados
chrome_path = r"C:\Users\GEMTI\Desktop\chrome-win64\chrome-win64\chrome.exe"
chromedriver_path = r"C:\Users\GEMTI\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Configurar opções do Chrome
options = webdriver.ChromeOptions()
options.binary_location = chrome_path

# Iniciar o driver com o caminho do ChromeDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# Abrir o WhatsApp Web
driver.get("https://web.whatsapp.com")

# Aguardar o usuário escanear o QR Code
print("Escaneie o QR Code e pressione Enter...")
time.sleep(30)

try:
    # Esperar até que o botão "Dados de perfil" esteja disponível
    print("Aguardando a página carregar...")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[@title='Dados de perfil']"))
    )

    # Encontrar e clicar no botão de "Dados de perfil"
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

    # Agora, vamos procurar a div com data-animate-modal-body="true"
    modal_div = driver.find_element(By.XPATH, "//div[@data-animate-modal-body='true']")
    
    telefones = set()  # Usamos um conjunto para evitar números duplicados
    telefone_regex = re.compile(r"[\d\+\(\)\-\s]+")  # Permite números, +, (, ), - e espaço
    total_telefones = 0  # Variável para armazenar a quantidade de números salvos

    while True:
        # Dentro da modal, encontrar os elementos de telefone visíveis
        telefone_elements = modal_div.find_elements(By.XPATH, ".//span[@dir='auto' and contains(@class, '_ao3e')]")

        for telefone in telefone_elements:
            telefone_texto = telefone.text.strip()

            # Verifica se o texto contém apenas caracteres válidos de telefone (números e caracteres especiais)
            if telefone_regex.fullmatch(telefone_texto) and telefone_texto not in telefones:
                telefones.add(telefone_texto)
                total_telefones += 1  # Atualiza o contador
                print(f"Número encontrado: {telefone_texto} (Total: {total_telefones})")

        # Pressionar seta para baixo globalmente
        webdriver.ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(1)  # Pequeno delay para carregar novos contatos

except Exception as e:
    print("Erro:", e)

finally:
    print(f"Total de {total_telefones} números encontrados:")
    for telefone in telefones:
        print(telefone)

    # Fechar o navegador após a execução
    driver.quit()
