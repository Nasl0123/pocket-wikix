#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
sys.path.insert(0, 'libs')
import pdftables_api
import xlrd
import xlwt

c = pdftables_api.Client('q659dgg6odaz')
def crear_xlsx(banco):
    c.xlsx('pdf/'+banco+'.pdf', 'xlsx/'+banco+'_output.xlsx')

def generar_acap(banco):
    try:
        a = formatear_acap(banco)
        return a[1]
    except:
        None

def formatear_acap(banco):
    try:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        sheet = book.sheet_by_index(0)
        var = ''
        for row in range(2,24):
            for col in range(2,5):
                if type(sheet.cell_value(row,col)) == float:
                            var += str(sheet.cell_value(row,col)*100).replace(',','')+'|'
                else:
                            var += sheet.cell_value(row,col).replace(',','')+'|'
            var += ','
            

        #var = limpiar(var[:var.find('Visa Prestige')]+'|'+var[var.find('Visa Prestige'):]+'^')
        #var = var.replace(',','|')
        var = var.encode('utf-8').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")
        lista = var.split(',')
        #return repr(sheet.cell_value(num_row-5,num_col-2))
        return (var,lista)
    except:
        None

def obtener_tarjeta_acap(tarjeta,info):
    resultado = {'tasa_interes':'',
                'comision_mora':'',
                'sobregiro':'',
                'emision':'',
                'renovacion':'',
                }
    if 'clasica' in tarjeta:
        val = 1
    else:
        val = 2
    for x in info:
        for y in x.split('|'):
            if 'tasa' in y.lower() and 'interes' in y.lower():
                if 'rd$' in y.lower():
                    resultado['tasa_interes'] = resultado['tasa_interes']+'RD$'+x.split('|')[val]+'/'
                elif 'us$' in y.lower():
                    resultado['tasa_interes'] = resultado['tasa_interes']+'USD$'+x.split('|')[val]
            elif 'emision' in y.lower() and not 'adicional' in y.lower():
                resultado['emision'] = resultado['emision']+x.split('|')[val]
            elif 'renovacion' in y.lower():
                resultado['renovacion'] = resultado['renovacion']+x.split('|')[val]
            elif 'cargos' in y.lower() and 'mora' in y.lower():
                resultado['comision_mora'] = 'RD$'+resultado['comision_mora']+x.split('|')[val]+'%'
            elif 'cargos' in y.lower() and 'sobregiro' in y.lower():
                resultado['sobregiro'] = 'RD$'+resultado['sobregiro']+x.split('|')[val]+'%'
    return resultado









                    
