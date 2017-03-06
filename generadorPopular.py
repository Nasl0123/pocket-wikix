#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
sys.path.insert(0, 'libs')
import pdftables_api
import xlrd
import xlwt

c = pdftables_api.Client('fc9wow7u2a9c')
def crear_xlsx(banco):
    c.xlsx(banco+'.pdf', 'xlsx/'+banco+'_output.xlsx')

def formatear_popular(banco):
    try:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        sheet = book.sheet_by_index(0)
        var = ''
        for row in range(100,121):
            var += sheet.cell_value(row,1)+'|'
        for row in range(2,60):
            if sheet.cell_value(row,3) == '':
                var += sheet.cell_value(row,2)+'|'
            else:
                var += sheet.cell_value(row,3)+'|'
        var = limpiar(var[:var.find('Visa Prestige')]+'|'+var[var.find('Visa Prestige'):]+'^')
        #var = var.replace(',','|')
        var = var.encode('utf-8').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")
        lista = var.split(',')
        #return repr(sheet.cell_value(num_row-5,num_col-2))
        return (var,lista)
    except:
        None

def limpiar(string):
    clave,clave1 = 0,0
    pos,pos1 = 0,0
    string = string.replace('US$','USD$')
    string = string.replace(',','')
    string = string.replace('.00','')
    while pos < len(string):
        while string[pos] == '|':
            string = string[:pos]+string[pos+1:]
            clave = 1
        if clave == 1:
            string = string[:pos]+','+string[pos:]
            clave = 0
            if string[pos+1] == '.':
                string = string[:pos+1] +'#'+ string[pos+1:]
        pos += 1
    while pos1 < len(string):
        while string[pos1] == '.':
            string = string[:pos1]+string[pos1+1:]
            clave1 = 1
        if clave1 == 1:
            string = string[:pos1]+'|'+string[pos1:]
            clave1 = 0
        pos1 += 1
    return string


def generar_popular(banco):
    try:
        a = formatear_popular(banco)
        return a[1]
    except:
        None

def obtener_popular(inicio,final,lista=None,inde=0,pos=0):
    if not lista:
        return 'Asigna una lista'
    lista_emision = []
    repetidos = []
    for linea in lista:
         if inicio in linea.lower():
             if inde == 0:
                 if linea in repetidos:
                     pos += 1
                 for linea_emision in lista[lista.index(linea,lista.index(linea)+pos)+1:]: #continuar aqui
                     if final in linea_emision:
                         break
                     else:
                         lista_emision.append(linea_emision)
                 break
             else:
                 inde -= 1
                 repetidos.append(linea)
    return lista_emision

#agregar aqui un nombre para la propiedad, seguido de una lista con:inicio de la recoleccion de datos, final de la recoleccion e indice de aparicion en el documento
datos_obtener = {'Emision':['emision','adicional',0],
                 'Renovacion':['membresia','adicional',0],
                 'Emision internacional':['emision','Cargos por servicios',1],
                 'Renovacion internacional':['membresia','Cargos por servicios',1],
                 'Otros cargos':['cargos por servicios','Seguro proteccion',0],
                 'Seguro de proteccion':['seguro proteccion','de TC al exterior',0],
                 'Tasa de interes':['tasas de interes','^',0]
                 }

def generar_info_popular(lista):
    info = {}
    for dato in datos_obtener:
        info[dato] = obtener_popular(datos_obtener[dato][0],datos_obtener[dato][1],lista,datos_obtener[dato][2])
    return info

#continuar en esta funcion
def obtener_tarjeta_popular(tarjeta,info):
    busqueda = {'Emision':'emision',
                'Emision internacional':'emision_internacional',
                'Renovacion internacional':'renovacion_internacional',
                'Tasa de interes':'tasa_interes',
                'Seguro de proteccion':'seguro_proteccion',
                'Renovacion':'renovacion'
                }
    resultado = {}
    #info = generar_info(generar(banco))
    for y in info.get('Otros cargos'):
        if len(y.split('|')) > 1 and not '' in y.split('|'):
            if 'sobregiro' in y.split('|')[0].lower():
                resultado['sobregiro'] = y.split('|')[1]
            if 'avance' in y.split('|')[0].lower() and 'efectivo' in y.split('|')[0].lower():
                if len(y.split('|')) > 2:
                    resultado['avance_efectivo'] = y.split('|')[1]+'.'+y.split('|')[2]
                else:
                    resultado['avance_efectivo'] = y.split('|')[1]
            if 'comision' in y.split('|')[0].lower() and 'mora' in y.split('|')[0].lower():
                resultado['comision_mora'] = y.split('|')[1]
            #resultado[] = y.split('|')[1]
    for x in busqueda:
        for dato in info.get(x):
            if comparar_popular(tarjeta,dato):
                if len(dato.split('|')) > 1 and not '' in dato.split('|'):
                    resultado[busqueda[x]] = dato.split('|')[1]
                else:
                    for dato_exp in info.get(x)[info.get(x).index(dato):]:
                        if len(dato_exp.split('|')) > 1 and not '' in dato_exp.split('|'):
                            resultado[busqueda[x]] = dato_exp.split('|')[1]
                            break

    return resultado

def comparar_popular(tarjeta,dato):
    tarjeta_list = tarjeta.split()
    n = 0
    if 'internacional' in tarjeta_list:
        tarjeta_list.remove('internacional')
    for e in tarjeta_list:
        if e in dato.lower():
            n+=1
    if n == len(tarjeta_list):
        return True
    return False
#print (obtener_tarjeta('test','clásica'))
#print (obtener_tarjeta('test','black'))
#print (obtener_tarjeta('test','platinum'))
#print (obtener_tarjeta('test','gold'))
#print (generar_info(generar('test')).get('Otros cargos'))
