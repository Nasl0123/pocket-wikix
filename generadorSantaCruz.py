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

def generar_santacruz(banco):
    try:
        a = formatear_santacruz(banco)
        return a
    except:
        None

def formatear_santacruz(banco):
    try:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        sheet = book.sheet_by_index(7)
        var = {'emision':{},
               'renovacion':{},
               'seguro_proteccion':{},
               'tasa_interes':{},
               'comision_mora':{},
               'sobregiro':{}}
        for row in range(5,15):
            var['emision'][limpiar_santacruz(sheet.cell_value(row,0))] = limpiar_santacruz(sheet.cell_value(row,1))
        for row in range(16,29):
            var['renovacion'][limpiar_santacruz(sheet.cell_value(row,0))] = limpiar_santacruz(sheet.cell_value(row,1))
        for row in range(30,34):
            var['seguro_proteccion'][limpiar_santacruz(sheet.cell_value(row,0))] = limpiar_santacruz(sheet.cell_value(row,1))
        for row in range(4,12):
            var['tasa_interes'][limpiar_santacruz(sheet.cell_value(row,2))] = limpiar_santacruz(sheet.cell_value(row,3))
        for row in range(19,33):
            if len(sheet.cell_value(row,0)) > 0:
                var['comision_mora'][limpiar_santacruz(sheet.cell_value(row,0))] = 'RD$400.00/USD$10.00'
        sheet = book.sheet_by_index(8)
        for row in range(0,4):
            var['seguro_proteccion'][limpiar_santacruz(sheet.cell_value(row,0))] = limpiar_santacruz(sheet.cell_value(row,1))
        for row in range(3,16):
            if len(sheet.cell_value(row,2)) > 0:
                var['sobregiro'][limpiar_santacruz(sheet.cell_value(row,2))] = 'RD$400.00/USD$10.00'
        return var
    except:
        None

def limpiar_santacruz(texto):
    if type(texto) == float:
        return str(texto*100)+'%'
    return texto.encode('utf-8').replace(',','').replace('\n',' ').replace('US$','USD$').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")

def obtener_tarjeta_santacruz(tarjeta,info):
    resultado = {'tasa_interes':''}
    for elem in info:
        for dato in info[elem]:
            if comparar_santacruz(tarjeta,dato):
                if elem == 'tasa_interes':
                    if 'RD$' in dato:
                        resultado[elem] += 'RD$'+info[elem][dato]+'/'
                    else:
                        resultado[elem] += 'USD$'+info[elem][dato]+'/'
                else:
                    resultado[elem] = info[elem][dato]
    return resultado


def comparar_santacruz(tarjeta,dato):
    if tarjeta in dato.lower() and not 'adicional' in dato.lower():
        return True
    return False
