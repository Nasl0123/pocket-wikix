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

def generar_ademi(banco):
    try:
        a = formatear_ademi(banco)
        return a[1]
    except:
        None


def formatear_ademi(banco):
    try:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        sheet = book.sheet_by_index(1)
        var = ''
        for col in range(0,3):
            var += sheet.cell_value(0,col).replace(',','')+'|'
        var = var.encode('utf-8').replace('\n','|').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")
        lista = var.split('|')
        resultado = []
        for e in lista:
            if 'RD' in e or '%' in e:
                e = e[::-1].replace(' ','|',1)[::-1]
            resultado.append(e)
        var = ''
        sheet = book.sheet_by_index(2)
        cols = [0,2,4]
        for col in cols:
            for row in range(0,25):
                var += sheet.cell_value(row,col)+'|'
                if type(sheet.cell_value(row,col+1)) == float:
                    var += str(sheet.cell_value(row,col+1)*100)+','
                else:
                    var += sheet.cell_value(row,col+1).replace(',','')+','
        var = var.encode('utf-8').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")
        lista = var.split(',')
        while '' in lista:
            lista.remove('')
        return (var,resultado+lista)
    
    except:
        None

def ordenar_info(info):
    info = info[0:]
    resultado = {}
    for i,e in enumerate(info):
        if 'tarjeta' in e.lower():
            resultado[e] = []
            for x in info[i+1:]:
                if 'tarjeta' in x.lower():
                    break
                else:
                    resultado[e].append(x)
    return resultado

def obtener_tarjeta_ademi(tarjeta,info):
    resultado = {'comision_mora':''}
    info = ordenar_info(info)
    for x in info:
        if comparar_ademi(tarjeta,x):
            for e in info[x]:
                if 'emision' in e.lower() and 'principal' in e.lower():
                    resultado['emision'] = e.split('|')[1]
                elif 'renovacion' in e.lower() and not 'adicional' in e.lower():
                    resultado['renovacion'] = e.split('|')[1]
                elif 'perdida' in e.lower() and 'robo' in e.lower():
                    resultado['seguro_proteccion'] = e.split('|')[1]
                elif 'avance' in e.lower() and 'efectivo' in e.lower():
                    resultado['avance_efectivo'] = e.split('|')[1]+'%'
                elif 'interes' in e.lower() and 'financiamiento' in e.lower():
                    resultado['tasa_interes'] = e.split('|')[1]+'%'
                elif 'comision' in e.lower() and 'sobregiro' in e.lower():
                    resultado['sobregiro'] = e.split('|')[1]
                elif 'comision' in e.lower() and 'mora' in e.lower():
                    resultado['comision_mora'] = e.split('|')[1]
            break
    return resultado

def comparar_ademi(tarjeta,dato):
    tarjeta_list = tarjeta.split()
    n = 0
    for e in tarjeta_list:
        if e in dato.lower():
            n+=1
    if n == len(tarjeta_list):
        return True
    return False

# def obtener_id_ademi(tarjeta):
#     resultado = {'clasica':'ctl00_ctl00_body_load_ajax_body_producto_LnkClasica',
#                  'empresarial':'ctl00_ctl00_body_load_ajax_body_producto_LnkEmpresarial',
#                  'gold':'ctl00_ctl00_body_load_ajax_body_producto_LnkGold',
#                  'flexible':'ctl00_ctl00_body_load_ajax_body_producto_LnkFlexible',
#                  'hiperole':'ctl00_ctl00_body_load_ajax_body_producto_LnkOle',
#                  'blue':'ctl00_ctl00_body_load_ajax_body_producto_LnkBlue',
#                  'plus':'ctl00_ctl00_body_load_ajax_body_producto_LnkPlus'}
#     return ('http://www.bancoademi.com.do/Pages/prod_tarjeta.aspx',resultado.get(tarjeta),'div')
