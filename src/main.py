import requests
from bs4 import BeautifulSoup

# Web sitesinin URL'si
url = 'https://www.nesine.com/iddaa/canli-skor/futbol'

# HTTP GET isteği gönder
response = requests.get(url)

# İstek başarılı olduysa devam et
if response.status_code == 200:
    # BeautifulSoup kullanarak HTML içeriğini analiz et
    soup = BeautifulSoup(response.text, 'html.parser')

    # class'ı "league-list-content" olan section etiketlerini bul
    match_list_div = soup.find('div', class_='match-list futbol')

    # Her bir section etiketini yazdır
    print(match_list_div.prettify())

    #for section in league_list_sections:
        #print(section.prettify())

else:
    # İstek başarısız olduysa hata mesajını yazdır
    print(f'Hata: {response.status_code}')

