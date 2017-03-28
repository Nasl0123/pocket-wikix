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

def generar_promerica(banco):
    try:
        a = formatear_promerica(banco)
        return a
    except:
        None

def formatear_promerica(banco):
    if True:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        sheet = book.sheet_by_index(0)
        var = {}
        ind = ['','','','','emision','','renovacion','','renovacion_premium','renovacion_crediplus',
               'renovacion_lamaplazos','renovacion_spirit','','seguro_proteccion','','avance_efectivo',
               '','','tasa_interes_rd','tasa_interes_usd','','','','comision_mora']
        for row in range(4,24):
            var[ind[row]] = []
            num = 0
            for col in range(5,8):
                val = limpiar_promerica(sheet.cell_value(row,col))
                if val == '':
                    val = quitar_puntos(limpiar_promerica(sheet.cell_value(row,4)))[num]
                var[ind[row]].append(val)
                num += 1
        var['sobregiro'] = sheet.cell_value(21,4)+'/'+sheet.cell_value(22,4)
        return var
    else:
        None

def limpiar_promerica(texto):
    if type(texto) == float:
        return str(texto*100)+'%'
    return texto.encode('utf-8').replace(',','').replace('USD','USD$').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")

def quitar_puntos(texto):
    res1,res2,res3 = None,None,None
    if texto == '':
        return ''
    texto1 = texto.replace('.','')
    if 'RD' in texto1:
        if 'N/A' in texto1[texto1.find('RD'):]:
            res1 = texto1[:texto1.find('RD')]
            res2 = texto1[texto1.find('RD'):texto1.find('N/A')][:-2]+'.'+texto1[texto1.find('RD'):texto1.find('N/A')][-2:]
            res3 = texto1[texto1.find('N/A'):]
        else:
            res1 = texto1[:texto1.find('RD')]
            res2 = texto1[texto1.find('RD'):][:-2]+'.'+texto1[texto1.find('RD'):][-2:]
            res3 = None
    elif 'N/A' in texto1:
        res1 = texto1[:texto1.find('N/A')]
        res2 = texto1[texto1.find('N/A'):]
        res3 = None
    elif '%' in texto1:
        if texto1[texto1.find('%')-1].isdigit():
            num = otra_funcion(texto1[:texto1.find('%')])
            res1 = texto1[:num]
            res2 = texto1[num:texto1.find('%')+1]
            res3 = None
    return (res2,res3,res1)

def otra_funcion(texto):
    num = -2
    while texto[num].isdigit():
        num -= 1
    return num
        
def obtener_tarjeta_promerica(tarjeta,info):
    resultado = {}
    if 'clasica' in tarjeta:
        ind = 0
    elif 'gold' in tarjeta:
        ind = 1
    elif 'platinum' in tarjeta:
        ind = 2
    else:
        ind = 3

    resultado['emision'] = info['emision'][ind]
    resultado['seguro_proteccion'] = info['seguro_proteccion'][ind]
    resultado['tasa_interes'] = 'RD$'+info['tasa_interes_rd'][ind]+'/USD$'+info['tasa_interes_usd'][ind]
    resultado['avance_efectivo'] = info['avance_efectivo'][ind]
    resultado['comision_mora'] = info['comision_mora'][ind]
    resultado['sobregiro'] = info['sobregiro']
    resultado['renovacion'] = info['renovacion'][ind]
    for e in info:
        if len(e.split('_')) > 1:
            if e.split('_')[1] in tarjeta and e.split('_')[0] == 'renovacion':
                resultado['renovacion'] = info[e][ind]
    return resultado
