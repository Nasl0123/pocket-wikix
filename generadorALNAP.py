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

def generar_alnap(banco):
    try:
        a = formatear_alnap(banco)
        return a[1]
    except:
        None

def formatear_alnap(banco):
    try:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        var = ''
        select = [0,3]
        selec = [95,102,82,19]
        i = 0
        for inde in range(2,4):
	        sheet = book.sheet_by_index(inde)
	        for sel in select:
		        for row in range(1,selec[i]):
		            var += sheet.cell_value(row,sel)+'|'
		            if type(sheet.cell_value(row,sel+1)) == float:
		            	var += str(sheet.cell_value(row,sel+1)*100)+'|'
		            else:
		            	var += sheet.cell_value(row,sel+1)+'|'
		        i+=1
		        #var = limpiar(var[:var.find('Visa Prestige')]+'|'+var[var.find('Visa Prestige'):]+'^')
		        #var = var.replace(',','|')
		        var = var.encode('utf-8').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")
		        lista = var.split('|')
		        #return repr(sheet.cell_value(num_row-5,num_col-2))
        return (var,lista)
    except:
        None

def ordenar_info(info):
    info = info[1:]
    resultado = {}
    for i,e in enumerate(info):
        if 'tarjeta' in e.lower() or 'credito diferido' in e.lower():
            resultado[e] = []
            for x in info[i+1:]:
                if 'tarjeta' in x.lower() or 'credito diferido' in x.lower():
                    break
                else:
                    resultado[e].append(x)
    return resultado
                    

def obtener_tarjeta_alnap(tarjeta,info):
    resultado = {'comision_mora':''}
    info = ordenar_info(info)
    for x in info:
        if comparar_alnap(tarjeta,x):
            for i,e in enumerate(info[x]):
                if 'emision' in e.lower():
                    resultado['emision'] = info[x][i+1]
                elif 'renovacion' in e.lower():
                    resultado['renovacion'] = info[x][i+1]
                elif 'proteccion' in e.lower():
                    resultado['seguro_proteccion'] = info[x][i+1]
                elif 'avance' in e.lower() and 'efectivo' in e.lower():
                    resultado['avance_efectivo'] = info[x][i+1]
                elif 'tasa' in e.lower() and 'financiamiento' in e.lower():
                    resultado['tasa_interes'] = info[x][i+1]+'%'
                elif 'interes' in e.lower() and 'sobregiro' in e.lower():
                    resultado['sobregiro'] = 'RD$'+info[x][i+1]+'%'
                elif 'mora' in e.lower() and 'cargo' in e.lower():
                    if 'us$' in e.lower():
                        resultado['comision_mora'] = resultado['comision_mora']+info[x][i+1].replace('US','USD')
                    else:
                        resultado['comision_mora'] = resultado['comision_mora']+info[x][i+1]+'/'
            break
    return resultado


def comparar_alnap(tarjeta,dato):
    tarjeta_list = tarjeta.split()
    n = 0
    for e in tarjeta_list:
        if e in dato.lower():
            n+=1
    if n == len(tarjeta_list):
        return True
    return False

