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

def generar_bdi(banco):
    try:
        a = formatear_bdi(banco)
        return a[1]
    except:
        None

def formatear_bdi(banco):
    try:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        sheet = book.sheet_by_index(0)
        var = ''
        for col in range(1,7):
            for row in range(2,19):
                if type(sheet.cell_value(row,col)) == float:
                            var += str(sheet.cell_value(row,col)*100)+'|'
                else:
                    var += sheet.cell_value(row,col).replace(',','')+'|'
        #var = limpiar(var[:var.find('Visa Prestige')]+'|'+var[var.find('Visa Prestige'):]+'^')
        #var = var.replace(',','|')
        var = var.encode('utf-8').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")
        lista = var.split('|')
        #return repr(sheet.cell_value(num_row-5,num_col-2))
        return (var,lista)
    except:
        None

def obtener_tarjeta_bdi(tarjeta,info):
    resultado = {}
    for i,e in enumerate(info):
        if e.lower() in tarjeta:
            lista = info[i:i+16]
            resultado['emision'] = lista[1]
            resultado['renovacion'] = lista[3]
            resultado['seguro_proteccion'] = lista[7]
            if 'local' in tarjeta:
                resultado['tasa_interes'] = 'RD$'+lista[9].split('-')[1]
                resultado['comision_mora'] = 'RD$'+lista[11].split('-')[0]
                resultado['sobregiro'] = 'RD$'+lista[13].split('-')[0]
            else:
                resultado['tasa_interes'] = 'RD$'+lista[9].split('-')[1]+'/USD$'+lista[10].split('-')[1]
                resultado['comision_mora'] = 'RD$'+lista[11].split('-')[0]+'/USD$'+lista[12].split('-')[0]
                resultado['sobregiro'] = 'RD$'+lista[13].split('-')[0]+'/USD$'+lista[14].split('-')[0]
            resultado['avance_efectivo'] = lista[15]+'%'
            break
    return resultado

