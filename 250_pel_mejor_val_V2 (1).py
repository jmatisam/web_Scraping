import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# URL de la página IMDb Top 250
url = 'https://m.imdb.com/chart/top/?ref_=nv_mv_250'

# Headers para la solicitud HTTP
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Realizar la solicitud HTTP
response = requests.get(url, headers=headers)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el HTML con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar la sección que contiene la información de las películas
    movies_section = soup.find('ul', {'class': 'ipc-metadata-list'})

    # Listas para almacenar los datos
    titles = []
    years = []
    durations = []
    ratings = []

    # Iterar sobre los elementos de la lista
    for movie_item in movies_section.find_all('li', {'class': 'ipc-metadata-list-summary-item'}):
        # Encontrar elementos dentro de cada ítem de la lista
        title = movie_item.find('h3', {'class': 'ipc-title__text'}).text.strip()
        year = int(movie_item.find('span', {'class': 'sc-479faa3c-8'}).text.strip())
        duration = movie_item.find_all('span', {'class': 'sc-479faa3c-8'})[1].text.strip()

        # Extraer solo el valor numérico de la calificación IMDb
        rating_element = movie_item.find('span', {'class': 'ipc-rating-star--imdb-rating'})
        print(rating_element)
        rating_text = rating_element.find('span', {'class': 'ipc-rating-star__rating'}).text.strip() if rating_element else None
        rating = float(rating_text) if rating_text else None


        titles.append(title)
        years.append(year)
        durations.append(duration)
        ratings.append(rating)

    # Crear un DataFrame de pandas
    data = {'Title': titles, 'Year': years, 'Duration': durations, 'Rating': ratings}
    df = pd.DataFrame(data)

    # Descargar los datos en un archivo CSV
    df.to_csv('imdb_top250.csv', index=False)

    # Imprimir información sobre el DataFrame
    print("Información del DataFrame:")
    print(df.info())

    # Mostrar las primeras entradas del DataFrame
    print("\nPrimeras entradas del DataFrame:")
    print(df.head())

else:
    print("Error al obtener la página:", response.status_code)

print(rating_element)
