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

def generar_vimenca(banco):
    try:
        a = formatear_vimenca(banco)
        return a
    except:
        None

def formatear_vimenca(banco):
    if True:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        sheet = book.sheet_by_index(13)
        var = {}
        for col in range(1,7):
            ind = ''
            for row in range(1,7):
                ind += sheet.cell_value(row,col)+'|'
            ind = limpiar_vimenca(ind).replace('|||',' ').replace('||','').replace('|','')
            var[ind] = []
            for row in range(7,22):
                var[ind].append(limpiar_vimenca(sheet.cell_value(row,col)))
        sheet = book.sheet_by_index(14)
        ind = 'comision_mora'
        var[ind] = {}
        for row in range(3,10):
            var[ind][limpiar_vimenca(sheet.cell_value(row,0))] = limpiar_vimenca(sheet.cell_value(row,1))+'/'+limpiar_vimenca(sheet.cell_value(row,2))
        ind = 'sobregiro'
        var[ind] = {}
        for row in range(3,10):
            var[ind][limpiar_vimenca(sheet.cell_value(row,4))] = limpiar_vimenca(sheet.cell_value(row,5))+'/'+limpiar_vimenca(sheet.cell_value(row,6))
        return var
    else:
        None

def limpiar_vimenca(texto):
    if type(texto) == float:
        return str(texto*100)+'%'
    return texto.encode('utf-8').replace(',','').replace('US$','USD$').replace('\n',' ').replace('N/A','-').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")

def obtener_tarjeta_vimenca(tarjeta,info):
    resultado = {}
    for dato in info:
        if comparar_vimenca(tarjeta,dato):
            resultado['emision'] = info[dato][0]
            resultado['renovacion'] = info[dato][8]
            resultado['tasa_interes'] = info[dato][1]
            resultado['seguro_proteccion'] = info[dato][10]
            resultado['avance_efectivo'] = info[dato][14]
    for dato in info['sobregiro']:
        if comparar_vimenca(tarjeta,dato):
            resultado['sobregiro'] = info['sobregiro'][dato]
    for dato in info['comision_mora']:
        if comparar_vimenca(tarjeta,dato):
            resultado['comision_mora'] = info['comision_mora'][dato]
    return resultado

def comparar_vimenca(tarjeta,dato):
    tarjeta_list = tarjeta.split()
    num = 0
    for e in tarjeta_list:
        if e in dato.lower():
            num += 1
    if num == len(tarjeta_list):
        return True
    return False
