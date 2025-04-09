import requests

url = "https://gruposwhats.app/"  # Mude para qualquer site que esteja raspando
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

with open("pagina_exemplo.html", "w", encoding="utf-8") as file:
    file.write(response.text)

print("Página salva como 'pagina_exemplo.html'. Abra no navegador e veja a estrutura.")
