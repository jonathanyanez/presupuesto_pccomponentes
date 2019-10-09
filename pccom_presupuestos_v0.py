#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys
import requests
import urllib.request
from bs4 import BeautifulSoup
from tabulate import tabulate

"""
float(",1".replace(",","."))
componentes=[['GRAFICA','asrock', 123.1231],['MONITOR','memencio', 12.12],['RATON', 'targus',16.68],['TARJETA DE SONIDO','babieco',67.819]];
print(tabulate(componentes, headers=['COMPONENT','PRODUCT NAME', 'PRICE']))
"""
def product_data(url, component_type):
    try:
        response=requests.get(url)
    except requests.exceptions.RequestException as e:
        print("ERROR EN CONEXION: ")
        print(e)
        print("--------------------")
        sys.exit(-1)

    document=BeautifulSoup(response.text, "html.parser")
    product_name=document.find("title").text
    #Resulta que el HTML de pccomponentes tiene el precio separado en dos tags:
    #<span>parte entera</span>
    #<span>parte decimal</span>
    #Esto explica las siguientes 3 lineas de codigo.
    integer_price=document.find('span', {'class':'baseprice'}).text
    decimal_price=document.find('span', {'class':'cents'}).text
    if decimal_price=="":
        decimal_price=",0"
    product_price=float(integer_price)+float(decimal_price.replace(',','.'))
    return [component_type, product_name, product_price]





products_data=[]
while(True):
    url=input("URL del producto: ")
    if (not url.startswith('https://www.pccomponentes.com/')):
        break
    component_type=input("tipo de componente: ")
    products_data.append(product_data(url, component_type))

precio_total=0.0
for i in products_data:
    precio_total +=i[2]


if(len(sys.argv)>1):
    f=open(sys.argv[1],'w+')
    print(tabulate(products_data, headers=['COMPONENT','PRODUCT NAME', 'PRICE']), file=f)
    print('PRECIO TOTAL: '+str(precio_total), file=f)
    f.close()
else:
    print(tabulate(products_data, headers=['COMPONENT','PRODUCT NAME', 'PRICE']))
    print('PRECIO TOTAL: '+str(precio_total))