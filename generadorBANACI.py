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

def generar_banaci(banco):
    try:
        a = formatear_banaci(banco)
        return a
    except:
        None

def formatear_banaci(banco):
    try:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        sheet = book.sheet_by_index(2)
        var = {}
        for col in range(1,10):
            ind = limpiar_banaci(sheet.cell_value(1,col)).lower()
            var[ind] = []
            for row in range(2,11):
                var[ind].append(limpiar_banaci(sheet.cell_value(row,col)))
        return var
    except:
        None

def limpiar_banaci(texto):
    if type(texto) == float:
        return str(texto*100)+'%'
    return texto.replace(',','').replace('US$','USD$').encode('utf-8').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")

def obtener_tarjeta_banaci(tarjeta,info):
    resultado = {}
    for dato in info:
        if comparar_banaci(tarjeta,dato):
            resultado['emision'] = info[dato][0]
            resultado['renovacion'] = info[dato][0]
            resultado['seguro_proteccion'] = info[dato][2]
            resultado['avance_efectivo'] = info[dato][4]
            resultado['tasa_interes'] = info[dato][5]
            resultado['sobregiro'] = info[dato][7]
            resultado['comision_mora'] = info[dato][8]
            break
    return resultado

def comparar_banaci(tarjeta,dato):
    tarjeta_list = tarjeta.split()
    if dato in tarjeta_list:
        return True
    return False


def beneficios_banaci():
    var = '''Programa de fidelidad.
    Tasa de financiamiento competitiva.
    Posibilidad de realizar pagos a traves de su cuenta de ahorro.
    Asignacion de limite para tarjetas adicionales.'''
    return var