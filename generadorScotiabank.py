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

def generar_scotiabank(banco):
    try:
        a = formatear_scotiabank(banco)
        return a[1]
    except:
        None

def formatear_scotiabank(banco):
    if banco:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        var = ''
        rows = [[5,25,34,41],[26,30,1,8]]
        i = 0
        sheet = book.sheet_by_index(9)
        for row in range(rows[i][0],rows[i][1]):
            for col in range(0,5):
                #var += sheet.cell_value(row,col).replace(',','')+'|'
                if type(sheet.cell_value(row,col)) == float:
                    var += str(sheet.cell_value(row,col)*100).replace(',','')+'|'
                else:
                    var += sheet.cell_value(row,col).replace(',','')+'|'
        for row in range(rows[i][2],rows[i][3]):
            for col in range(0,6):
                #var += sheet.cell_value(row,col).replace(',','')+'|'
                if type(sheet.cell_value(row,col)) == float:
                    var += str(sheet.cell_value(row,col)*100).replace(',','')+'|'
                else:
                    var += sheet.cell_value(row,col).replace(',','')+'|'
        i += 1
        for row in range(rows[i][0],rows[i][1]):
            for col in range(0,5):
                #var += sheet.cell_value(row,col).replace(',','')+'|'
                if type(sheet.cell_value(row,col)) == float:
                    var += str(sheet.cell_value(row,col)*100).replace(',','')+'|'
                else:
                    var += sheet.cell_value(row,col).replace(',','')+'|'
        sheet = book.sheet_by_index(10)
        for row in range(rows[i][2],rows[i][3]):
            for col in range(0,2):
                #var += sheet.cell_value(row,col).replace(',','')+'|'
                if type(sheet.cell_value(row,col)) == float:
                    var += str(sheet.cell_value(row,col)*100).replace(',','')+'|'
                else:
                    var += sheet.cell_value(row,col).replace(',','')+'|'
            #var = limpiar(var[:var.find('Visa Prestige')]+'|'+var[var.find('Visa Prestige'):]+'^')
            #var = var.replace(',','|')
        var = var.encode('utf-8').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")
        lista = var.split('|')
        resultado = []
        while '' in lista:
                lista.remove('')
            #return repr(sheet.cell_value(num_row-5,num_col-2))
        return (var,lista)
    else:
        return None


def ordenar_info(info):
    info = info[1:]
    resultado = {}
    resultado1 = {}
    for i,e in enumerate(info):
        if 'scotiabank' in e.lower():
            if not resultado.get(e):
                resultado[e] = []
                for x in info[i+1:]:
                    if 'scotiabank' in x.lower() or 'comision' in x.lower():
                        break
                    else:
                        resultado[e].append(x)
            else:
                for n,x in enumerate(info[i+1:]):
                    if 'scotiabank' in x.lower() or 'comision' in x.lower():
                        break
                    else:
                        resultado[e][n] += '/'+x
        elif 'comision' in e.lower():
            n = 0
            while n+1 < len(info[i:]):
                resultado1[info[i:][n]] = info[i:][n+1]
                n += 2
    return (resultado,resultado1)

def obtener_tarjeta_scotiabank(tarjeta,info):
    for dato in info:
        if comparar_scotiabank(tarjeta,dato):
            for i,e in enumerate(info[dato]):
                pass





def comparar_scotiabank(tarjeta,dato):
    tarjeta_list = tarjeta.split()
    n = 0
    for e in tarjeta_list:
        if e in dato.lower():
            n+=1
    if n == len(tarjeta_list):
        return True
    return False
