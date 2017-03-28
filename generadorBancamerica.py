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

def generar_bancamerica(banco):
    try:
        a = formatear_bancamerica(banco)
        return a
    except:
        None

def formatear_bancamerica(result):
    try:
        book = xlrd.open_workbook(file_contents=result)
        sheet = book.sheet_by_index(0)
        var = {}
        for row in range(10,21):
            ind = limpiar_bancamerica(sheet.cell_value(row,0))
            var[ind] = []
            for col in range(1,5):
                var[ind].append(limpiar_bancamerica(sheet.cell_value(row,col)))
        for row in range(21,30):
            ind = limpiar_bancamerica(sheet.cell_value(row,0))
            var[ind] = []
            var[ind].append(limpiar_bancamerica(sheet.cell_value(row,1)))
        #return repr(sheet.cell_value(num_row-5,num_col-2))
        return var
    except:
        None

def limpiar_bancamerica(texto):
    if type(texto) == float:
        if texto < 1:
            return str(texto*100)+'%'
        return 'RD$'+str(texto)
    return texto.encode('utf-8').replace('.','').replace(',','').replace('RDS','RD$').replace('US$','USD$').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")

def obtener_tarjeta_bancamerica(tarjeta,info):
    resultado = {}
    indice = {'clasica':0,'gold':1,'platinum':2,'signature':3}
    if tarjeta in indice:
        for dato in info:
            if 'emision' in dato.lower() and not 'adicional' in dato.lower():
                resultado['emision'] = info[dato][indice[tarjeta]]
            elif 'renovacion' in dato.lower() and not 'adicional' in dato.lower():
                resultado['renovacion'] = info[dato][indice[tarjeta]]
            elif 'proteccion' in dato.lower() and not 'adicional' in dato.lower():
                resultado['seguro_proteccion'] = info[dato][indice[tarjeta]]
            elif 'membresia' in dato.lower():
                resultado['membresia'] = info[dato][indice[tarjeta]]
            elif 'retiro' in dato.lower() and 'efectivo' in dato.lower():
                resultado['avance_efectivo'] = info[dato][0]
            elif 'financiamiento' in dato.lower():
                resultado['tasa_interes'] = info[dato][0]
            elif 'interes' in dato.lower() and 'mora' in dato.lower():
                resultado['comision_mora'] = info[dato][0].split('minimo ')[1]
            elif 'comision' in dato.lower() and 'sobregiro' in dato.lower():
                resultado['sobregiro'] = info[dato][0].split('minimo ')[1]
    return resultado