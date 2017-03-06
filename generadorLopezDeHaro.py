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


def formatear_lopezdeharo(banco):
    try:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        sheet = book.sheet_by_index(0)
        var = ''
        for row in range(2,72):
            var += sheet.cell_value(row,6).replace(',','')
            if sheet.cell_value(row,7) == '':
                if sheet.cell_value(row+1,6) == '':
                    if sheet.cell_value(row+1,7) == '':
                        var += ','
                else:
                    var += ' '
            else:
                var += '|'+str(sheet.cell_value(row,7)).replace(',','')+','
        #for row in range(2,60):
         #   if sheet.cell_value(row,3) == '':
         #       var += sheet.cell_value(row,2)+'|'
         #   else:
         #       var += sheet.cell_value(row,3)+'|'
        #var = limpiar(var[:var.find('Visa Prestige')]+'|'+var[var.find('Visa Prestige'):]+'^')
        #var = var.replace(',','|')
        var = var.replace('.00','').replace('\n',' ').replace('US$','USD$')
        var = var.encode('utf-8').replace('\xc3\xa1','a').replace('\xc3\xb3','o').replace('\xc3\xad','i').replace('\xc3\xa9','e').replace('\xc3\xba','u').replace('\xc3\xb1','n')
        lista_nueva = []
        lista = var.split(',')
        for e in lista:
            if not 'Adicionales' in e:
                lista_nueva.append(e)
        #return repr(sheet.cell_value(num_row-5,num_col-2))
        return (var,lista_nueva)
    except:
        None

def generar_lopezdeharo(banco):
    try:
        a = formatear_lopezdeharo(banco)
        return a[1]
    except:
        None

def obtener_lopezdeharo(inicio,final,lista=None,inde=0,pos=0):
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
                     if final in linea_emision.lower():
                         break
                     else:
                         lista_emision.append(linea_emision)
                 break
             else:
                 inde -= 1
                 repetidos.append(linea)
    return lista_emision

datos_obtener = {'Emision':['renovacion','reemplazo',0],
                 'Renovacion':['renovacion','reemplazo',0],
                 'Otros cargos':['otros cargos','debito',0],
                 'Seguro de proteccion':['perdida','otros cargos',0],
                 }

def generar_info_lopezdeharo(lista):
    info = {}
    for dato in datos_obtener:
        info[dato] = obtener_lopezdeharo(datos_obtener[dato][0],datos_obtener[dato][1],lista,datos_obtener[dato][2])
    return info

def obtener_tarjeta_lopezdeharo(tarjeta,info):
    busqueda = {'Emision':'emision',
                'Seguro de proteccion':'seguro_proteccion',
                'Renovacion':'renovacion'
                }
    resultado = {}
    #info = generar_info(generar(banco))
    for y in info.get('Otros cargos'):
        if 'sobregiro' in y.split('|')[0].lower():
            resultado['sobregiro'] = y.split('|')[1]
        if 'comision' in y.split('|')[0].lower() and 'mora' in y.split('|')[0].lower():
            resultado['comision_mora'] = y.split('|')[1]
        if 'avance' in y.split('|')[0].lower() and 'efectivo' in y.split('|')[0].lower():
            resultado['avance_efectivo'] = str(float(y.split('|')[1])*100)
        if 'financiamiento' in y.split('|')[0].lower() and 'rd' in y.split('|')[0].lower():
            resultado['tasa_interes_rd'] = str(float(y.split('|')[1])*100)
        if 'financiamiento' in y.split('|')[0].lower() and 'us' in y.split('|')[0].lower():
            resultado['tasa_interes_usd'] = str(float(y.split('|')[1])*100)
    if resultado.get('tasa_interes_rd') or resultado.get('tasa_interes_usd'):
        if resultado.get('tasa_interes_rd'):
            if resultado.get('tasa_interes_usd'):
                resultado['tasa_interes'] = 'RD$'+resultado.get('tasa_interes_rd')+'/USD$'+resultado.get('tasa_interes_usd') 
                del resultado['tasa_interes_rd']
                del resultado['tasa_interes_usd']
            else:
                resultado['tasa_interes'] = 'RD$'+resultado.get('tasa_interes_rd')
                del resultado['tasa_interes_rd']
        else:
            resultado['tasa_interes'] = 'USD$'+resultado.get('tasa_interes_usd')
            del resultado['tasa_interes_usd']

    for x in busqueda:
        for dato in info.get(x):
            if comparar_lopezdeharo(tarjeta,dato):
                resultado[busqueda[x]] = dato.split('|')[1]
    return resultado

def comparar_lopezdeharo(tarjeta,dato):
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
