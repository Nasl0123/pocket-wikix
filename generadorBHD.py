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

def generar_bhd(banco):
    try:
        a = formatear_bhd(banco)
        return a
    except:
        None

def formatear_bhd(banco):
    try:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        var = {}
        dataForAll = {}
        sheet = book.sheet_by_index(11)
        for row in range(3,6):
            dataForAll[limpiar_bhd(sheet.cell_value(row,0))] = limpiar_bhd(sheet.cell_value(row,1))
        pos = {7:21,8:11}
        for pos_ind in pos:
            sheet = book.sheet_by_index(pos_ind)
            for row in range(2,pos[pos_ind]):
                ind = limpiar_bhd(sheet.cell_value(row,0))
                var[ind] = {}
                dato = ['unused','emision','renovacion','unused','tasa_interes','unused','tasa_interes','seguro_proteccion','seguro_proteccion']
                for col in range(1,9):
                    data = limpiar_bhd(sheet.cell_value(row,col))
                    if var[ind].get(dato[col]):
                        if data != 'N/A':
                            var[ind][dato[col]] += '/'+data
                    else:
                        if data != 'N/A':
                            var[ind][dato[col]] = data
                var[ind]['comision_mora'] = dataForAll.get('Mora').replace(' y ','/')
                var[ind]['sobregiro'] = dataForAll.get('Sobregiro').replace(' y ','/')
                var[ind]['avance_efectivo'] = dataForAll.get('Retiro de Efectivo')
                if len(var[ind]['tasa_interes'].split('/')) > 1:
                    if len(var[ind]['tasa_interes'].split('/')[1].split('-')) > 1:
                        var[ind]['tasa_interes'] = 'RD$'+var[ind]['tasa_interes'].split('/')[0]+'/'+'USD$'+var[ind]['tasa_interes'].split('/')[1].split('-')[1]
                    else:
                        var[ind]['tasa_interes'] = 'RD$'+var[ind]['tasa_interes'].split('/')[0]+'/'+'USD$'+var[ind]['tasa_interes'].split('/')[1]
                else:
                    var[ind]['tasa_interes'] = 'RD$'+var[ind]['tasa_interes']
        return var
    except:
        None

def limpiar_bhd(texto):
    if type(texto) == float:
        return str(texto*100)+'%'
    return texto.encode('utf-8').replace(',','').replace('\n',' ').replace('US$','USD$').replace('\xe2\x80\x93','').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")


def obtener_tarjeta_bhd(tarjeta,info):
    resultado = {}
    for dato in info:
        if comparar_bhd(tarjeta,dato):
            for e in info[dato]:
                if e != 'unused':
                    resultado[e] = info[dato][e]
            break
    return resultado


def comparar_bhd(tarjeta,dato):
    tarjeta_list = tarjeta.split()
    dato_list = dato.lower().replace('visa ','').replace('mastercard ','').split()
    num = 0
    for e in tarjeta_list:
        if e in dato_list:
            num += 1
    if num == len(tarjeta_list):
        return True
    return False
