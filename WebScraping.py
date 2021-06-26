# Igor de Sousa
# igor_sk98@hotmail.com

import pandas as pd 
from bs4 import BeautifulSoup
import requests
 
# Extração dos nomes dos produtos
def get_titulo(soup):
     
    try:
        
        titulo = soup.find("span", attrs={"id":'productTitle'})
 
        titulo_valor = titulo.string
 
        titulo_string = titulo_valor.strip()
 
    except AttributeError:
        titulo_string = ""   
 
    return titulo_string
 
# Extração dos preços dos produtos
def get_preco(soup):
 
    try:
        preco = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()
 
    except AttributeError:
 
        try:
            
            preco = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()
 
        except:     
            preco = "Sem valor informado"  
 
    return preco  

# Função para armazenar dados numa planilha do Excel
def excel():
    df = pd.DataFrame({'Produto':produtos,'Preco':precos}) 
    df.to_excel('produtos.xlsx', index=False, encoding='utf-8')     

if __name__ == '__main__':
 
    # Headers
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US'})
 
    # URL da página
    URL = "https://www.amazon.com.br/s?k=iphone&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_2"
     
    webpage = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(webpage.content, "lxml")

    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
 
    # Arrays para armazenar títulos e preços
    links_lista = []
    produtos = []
    precos = []

    print ('Gerando Excel, aguarde...')

    print ('Esse processo demora cerca de 2 minutos...')
    
    for link in links:
        links_lista.append(link.get('href'))
    
    for link in links_lista:
 
        new_webpage = requests.get("https://www.amazon.com.br" + link, headers=HEADERS)
 
        new_soup = BeautifulSoup(new_webpage.content, "lxml")
         
        produtos.append(get_titulo(new_soup))
        precos.append(get_preco(new_soup))


excel()      