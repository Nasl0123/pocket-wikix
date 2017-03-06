#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'libs')
from bs4 import BeautifulSoup
from urllib import FancyURLopener
from indices import limpiar
from selenium import webdriver

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

def datos_tarjeta(banco,tarjeta=None):
    if not tarjeta:
        return (None,None,None)
    tree = None
    link = {}
    path = {}
    if banco == 'Popular':
        tree = ['div','fullbleed-grid row details','class']
        link = {'clasica':['https://www.popularenlinea.com/clasica'],
                'orbit':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/orbit.aspx'],
                'clasica internacional':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/clasica-facturation-en-dolares.aspx'],
                'prestige':['https://www.popularenlinea.com/visaprestige'],
                'gold':['https://www.popularenlinea.com/gold'],
                'gold internacional':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/gold-facturacion-en-dolares.aspx'],
                'platinum':['https://www.popularenlinea.com/platinum'],
                'platinum internacional':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/platinum-dolares.aspx'],
                'black':['https://www.popularenlinea.com/mastercardblack'],
                'black internacional':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/mastercard-black-dolares.aspx'],
                'fcbescola':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/Tarjeta-Credito-FCBEscola.aspx'],
                'jetblue':['https://www.popularenlinea.com/jetblue'],
                'ccn plus':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/mastercard-ccnpPlus.aspx'],
                'mileage plus':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/mastercard-mileage-plus.aspx'],
                'mb signature':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/mb-visa-signature-card.aspx'],
                'ikea family':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/ikea-family.aspx'],
                'seguros universal':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/mc-seguros.aspx'],
                'caminantes por la vida':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/caminantes-por-la-vida.aspx'],
                'almacenes iberia':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/mastercard-almacenes-iberia.aspx'],
                'sirena':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/visa-pola-sirena.aspx'],
                'avanza':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/avanza.aspx']}

        path = {'clasica':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'orbit':['div','col-md-4 col-sm-4 col-xs-12'],
                'clasica internacional':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'prestige':['div','row grid-line-row'],
                'gold':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'gold internacional':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'platinum':['div','col-md-4 col-sm-4 col-xs-12'],
                'platinum internacional':['div','col-md-4 col-sm-4 col-xs-12'],
                'black':['div','col-md-4 col-sm-4 col-xs-12'],
                'black internacional':['div','col-md-4 col-sm-4 col-xs-12'],
                'fcbescola':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'jetblue':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'ccn plus':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'mileage plus':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'mb signature':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'ikea family':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'seguros universal':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'caminantes por la vida':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'almacenes iberia':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'sirena':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'avanza':['div','col-md-3 col-sm-3 col-xs-12 grid-item']}

    if banco == 'LopezDeHaro':
        tree = ['table','tabla-verticalA','class']
        link = {'clasica':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx'],
                'casa de espana':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx'],
                'club hemingway':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx'],
                'club naco':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx'],
                'gold':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx'],
                'golds gym':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx'],
                'platinum':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx']}

        path = {'clasica':['td','tabla-verticalA_celdaAzul'],
                'casa de espana':['td','tabla-verticalA_celdaAzul'],
                'club hemingway':['td','tabla-verticalA_celdaAzul'],
                'club naco':['td','tabla-verticalA_celdaAzul'],
                'gold':['td','tabla-verticalA_celdaAzul'],
                'golds gym':['td','tabla-verticalA_celdaAzul'],
                'platinum':['td','tabla-verticalA_celdaAzul']}
    if banco == 'Progreso':
        tree = ['div','overview_wrap','id']
        link = {'casa de campo':['http://www.americanexpress.com.do/personal/our-cards/TC_platinum_casadecampo.html'],
                'american express':['http://www.americanexpress.com.do/personal/our-cards/TC_personal.html'],
                'american express gold':['https://www.livegold.do/'],
                'suma ccn':['http://www.americanexpress.com.do/personal/our-cards/TC_suma_ccn.html'],
                'gold':['http://www.progreso.com.do/index.php/tarjetas-de-credito-mastercard-gold-internacional'],
                'internacional':['http://www.progreso.com.do/index.php/tarjetas-de-credito-mastercard-internacional'],
                'local':['http://www.progreso.com.do/index.php/tarjetas-de-credito-mastercard-local'],
                'platinum':['http://www.progreso.com.do/index.php/tarjetas-de-credito-mastercard-platinum-internacional'],
                'platinum card':['http://www.americanexpress.com.do/platinum/priority.html',
                                 'http://www.americanexpress.com.do/platinum/vip.html',
                                 'http://www.americanexpress.com.do/platinum/lifestyle.html',
                                 'http://www.americanexpress.com.do/platinum/rewards.html',
                                 'http://www.americanexpress.com.do/platinum/protection.html',
                                 'http://www.americanexpress.com.do/platinum/cardmember_services.html']}

        path = {'casa de campo':['div','overview_all_data'],
                'american express':['div','overview_all_data'],
                'american express gold':['div','row','class'],
                'suma ccn':['div','overview_all_data'],
                'gold':['table','contentpaneopen','class'],
                'internacional':['table','contentpaneopen','class'],
                'local':['table','contentpaneopen','class'],
                'platinum':['table','contentpaneopen','class'],
                'platinum card':['div','PlatinumContentMain','id']}

        diferentes = ['american express gold','gold','internacional','local','platinum','platinum card']
        if tarjeta in diferentes:
            if tarjeta == 'american express gold':
                tree = ['div','benefits-container','id']
            elif tarjeta == 'platinum card':
                tree = ['div','ContentFeature','id']
            else:
                tree = ['div','mainbody','id']
    if banco == 'ACAP':
        tree = ['div','item-page clearfix','class']
        link = {'gold':['https://www.acap.com.do/site2/index.php/banca-personal/tarjeta-de-credito/tarjeta-de-credito-visa-gold'],
                'clasica':['https://www.acap.com.do/site2/index.php/banca-personal/tarjeta-de-credito/visa-clasica-local'],
                'clasica internacional':['https://www.acap.com.do/site2/index.php/banca-personal/tarjeta-de-credito/visa-clasica-internacional']}

        path = {'gold':['ul','ja-unordered-list'],
                'clasica':['ul','ja-unordered-list'],
                'clasica internacional':['ul','ja-unordered-list']}

    if banco == 'ALNAP':
        tree = ['div','article-content','class']
        link = {'clasica local':['http://www.alnap.com.do/productos/personas/tarjetas/clasica-local'],
                'clasica internacional':['http://www.alnap.com.do/productos/personas/tarjetas/tarjeta-clasica-internacional'],
                'gold':['http://www.alnap.com.do/productos/personas/tarjetas/tarjeta-de-credito-gold'],
                'confiamas':['http://www.alnap.com.do/productos/tarjeta-de-credito-confiamas'],
                'confia en ti local':['http://www.alnap.com.do/productos/confia-en-ti'],
                'confia en ti internacional':['http://www.alnap.com.do/productos/confia-en-ti'],
                'unase local':['http://www.alnap.com.do/productos/personas/tarjetas/tarjeta-visa-unase'],
                'unase internacional':['http://www.alnap.com.do/productos/tarjeta-visa-unase-internacional'],
                'union local':['http://www.alnap.com.do/productos/tarjeta-visa-union'],
                'union internacional':['http://www.alnap.com.do/productos/tarjeta-visa-union'],
                'compramas':['http://www.alnap.com.do/productos/personas/tarjetas/compramas']
                }

        path = {'clasica local':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'clasica internacional':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'gold':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'confiamas':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'confia en ti local':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'confia en ti internacional':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'unase local':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'unase internacional':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'union local':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'union internacional':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'compramas':['div','field field-name-field-content-tab field-type-text-long field-label-hidden']
                }

    if banco == 'BDI':
        tree = ['div','component-content','class']
        link = {'local':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/tarjetas-visa-bdi'],
                'clasica':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/tarjetas-visa-bdi'],
                'gold':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/tarjetas-visa-bdi'],
                'signature':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/tarjeta-signature'],
                'anthonys clasica':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/tarjeta-anthony-s'],
                'anthonys gold':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/tarjeta-anthony-s'],
                'anthonys platinum':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/tarjeta-anthony-s'],
                'signature bm cargo':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/bmcargo'],
                'crediplan':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/credito-diferido']
                }

        path = {'local':['article','item-page'],
                'clasica':['article','item-page'],
                'gold':['article','item-page'],
                'signature':['article','item-page'],
                'anthonys clasica':['article','item-page'],
                'anthonys gold':['article','item-page'],
                'anthonys platinum':['article','item-page'],
                'signature bm cargo':['article','item-page'],
                'crediplan':['article','item-page']
                }

    return (link.get(tarjeta),path.get(tarjeta),tree)

def obtener_beneficios(urls,path,tree,otros=None):
    if not urls or len(urls) == 0:
        return ''
    final = ''
    for url in urls:
        # Realizamos la petición a la web
        #req = urllib.urlopen(url)
        opener = MyOpener()
        req = opener.open(url)
        x = req.read()
        resultado = []
        # Comprobamos que la petición nos devuelve un Status Code = 200
        statusCode = req.getcode()
        if statusCode == 200:

            # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            html = BeautifulSoup(x)
            #b = {}
            # Obtenemos todos los divs donde estan las entradas
            entradas = html.find_all(tree[0],{tree[2] : tree[1]})
            b = ''

            # Recorremos todas las entradas para extraer el título, autor y fecha
            for i,entrada in enumerate(entradas):
                #a = []
                a = ''
                # Con el método "getText()" no nos devuelve el HTML
                if len(path) == 3:
                    titulo = entrada.find_all(path[0], {path[2] : path[1]})
                else:
                    titulo = entrada.find_all(path[0], {tree[2] : path[1]})
                for e in titulo:
                    a = a+"%s"%e.getText()
                if otros:
                    datos = html.find_all(otros[0],{tree[2]: otros[1]})
                    for s in datos:
                        if len(s.getText().split())<6:
                            resultado.append(limpiar(s.getText()))
                    tarjeta = otros[2]
                # Sino llamamos al método "getText()" nos devuelve también el HTML
                #autor = entrada.find('span', {'class' : 'autor'})
                #fecha = entrada.find('span', {'class' : 'fecha'}).getText()
                if i == 0:
                    b = a

                # Imprimo el Título, Autor y Fecha de las entradas
               # print ("%d - %s  |  %s  |  %s" %(i+1,titulo,autor,fecha))
                while '' in resultado:
                    resultado.remove('')
                if otros:
                    b = mas_beneficios(b,a,resultado,i,tarjeta)
                #.encode('utf-8').replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")
                #.replace('\n','').replace('\r','')

        else:
            return "Status Code %d : %s" %(statusCode,req.read())
        final += b
    if final:
        return final.replace('<!--','').replace('-->','')
    else:
        return 'No se encuentran beneficios.'

def mas_beneficios(b,a,resultado,i,tarjeta):
    boolean = False
    if len(resultado)>0:
        for e in resultado[i-1].lower().split():
            if e in tarjeta:
                boolean += 1
            if boolean > len(resultado[i-1].lower().split())-2:
                return a+b
        return b
    else:
        return b+a
