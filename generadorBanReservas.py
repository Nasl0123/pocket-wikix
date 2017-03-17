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

def generar_banreservas(banco):
    try:
        a = formatear_banreservas(banco)
        return a
    except:
        None

def formatear_banreservas(banco):
    try:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        resultado = {}
        var = ''
        ind = 'indefinido'
        sheet = book.sheet_by_index(5)
        # if 'mastercard' in sheet.cell_value(row,col[0]).lower() or 'visa' in sheet.cell_value(row,col[0]).lower() or 'tarjeta' in sheet.cell_value(row,col[0]).lower() or 'local' in sheet.cell_value(row,col[0]).lower() or 'card' in sheet.cell_value(row,col[0]).lower():
        #     ind = sheet.cell_value(row,col[0])
        #     resultado[ind] = {}
        # else:
        #     resultado[ind][sheet.cell_value(row,col[0]).replace(',','')] = sheet.cell_value(row,col[1]).replace(',','')

        ind = limpiar_banreservas(sheet.cell_value(14,1))
        resultado[ind] = {}
        for row in range(16,36):
            col = [2,3]
            if 'mastercard' in sheet.cell_value(row,col[0]).lower() or 'visa' in sheet.cell_value(row,col[0]).lower() or 'tarjeta' in sheet.cell_value(row,col[0]).lower() or 'local' in sheet.cell_value(row,col[0]).lower() or 'card' in sheet.cell_value(row,col[0]).lower():
                ind = limpiar_banreservas(sheet.cell_value(row,col[0]))
                resultado[ind] = {}
            else:
                resultado[ind][limpiar_banreservas(sheet.cell_value(row,col[0]).replace(',',''))] = limpiar_banreservas(sheet.cell_value(row,col[1]).replace(',',''))
        sheet = book.sheet_by_index(6)    
        for row in range(1,46):
            col = [0,1]
            if 'mastercard' in sheet.cell_value(row,col[0]).lower() or 'visa' in sheet.cell_value(row,col[0]).lower() or 'tarjeta' in sheet.cell_value(row,col[0]).lower() or 'local' in sheet.cell_value(row,col[0]).lower() or 'card' in sheet.cell_value(row,col[0]).lower():
                ind = limpiar_banreservas(sheet.cell_value(row,col[0]))
                resultado[ind] = {}
            else:
                resultado[ind][limpiar_banreservas(sheet.cell_value(row,col[0]).replace(',',''))] = limpiar_banreservas(sheet.cell_value(row,col[1]).replace(',',''))
        for row in range(1,45):
            col = [2,3]
            if 'mastercard' in sheet.cell_value(row,col[0]).lower() or 'visa' in sheet.cell_value(row,col[0]).lower() or 'tarjeta' in sheet.cell_value(row,col[0]).lower() or 'local' in sheet.cell_value(row,col[0]).lower() or 'card' in sheet.cell_value(row,col[0]).lower():
                ind = limpiar_banreservas(sheet.cell_value(row,col[0]))
                resultado[ind] = {}
            else:
                resultado[ind][limpiar_banreservas(sheet.cell_value(row,col[0]).replace(',',''))] = limpiar_banreservas(sheet.cell_value(row,col[1]).replace(',',''))
        sheet = book.sheet_by_index(7)
        for row in range(1,35):
            col = [0,1]
            if 'mastercard' in sheet.cell_value(row,col[0]).lower() or 'visa' in sheet.cell_value(row,col[0]).lower() or 'tarjeta' in sheet.cell_value(row,col[0]).lower() or 'local' in sheet.cell_value(row,col[0]).lower() or 'card' in sheet.cell_value(row,col[0]).lower():
                ind = limpiar_banreservas(sheet.cell_value(row,col[0]))
                resultado[ind] = {}
            else:
                resultado[ind][limpiar_banreservas(sheet.cell_value(row,col[0]).replace(',',''))] = limpiar_banreservas(sheet.cell_value(row,col[1]).replace(',',''))       
        for row in range(1,36):
            col = [2,3]
            if 'mastercard' in sheet.cell_value(row,col[0]).lower() or 'visa' in sheet.cell_value(row,col[0]).lower() or 'tarjeta' in sheet.cell_value(row,col[0]).lower() or 'local' in sheet.cell_value(row,col[0]).lower() or 'card' in sheet.cell_value(row,col[0]).lower():
                ind = limpiar_banreservas(sheet.cell_value(row,col[0]))
                resultado[ind] = {}
            else:
                resultado[ind][limpiar_banreservas(sheet.cell_value(row,col[0]).replace(',',''))] = limpiar_banreservas(sheet.cell_value(row,col[1]).replace(',',''))
        sheet = book.sheet_by_index(8)
        for row in range(1,38):
            col = [0,1]
            if 'mastercard' in sheet.cell_value(row,col[0]).lower() or 'visa' in sheet.cell_value(row,col[0]).lower() or 'tarjeta' in sheet.cell_value(row,col[0]).lower() or 'local' in sheet.cell_value(row,col[0]).lower() or 'card' in sheet.cell_value(row,col[0]).lower():
                ind = limpiar_banreservas(sheet.cell_value(row,col[0]))
                resultado[ind] = {}
            else:
                resultado[ind][limpiar_banreservas(sheet.cell_value(row,col[0]).replace(',',''))] = limpiar_banreservas(sheet.cell_value(row,col[1]).replace(',',''))
        for row in range(1,38):
            col = [2,3]
            if 'mastercard' in sheet.cell_value(row,col[0]).lower() or 'visa' in sheet.cell_value(row,col[0]).lower() or 'tarjeta' in sheet.cell_value(row,col[0]).lower() or 'local' in sheet.cell_value(row,col[0]).lower() or 'card' in sheet.cell_value(row,col[0]).lower():
                ind = limpiar_banreservas(sheet.cell_value(row,col[0]))
                resultado[ind] = {}
            else:
                resultado[ind][limpiar_banreservas(sheet.cell_value(row,col[0]).replace(',',''))] = limpiar_banreservas(sheet.cell_value(row,col[1]).replace(',',''))
        #return repr(sheet.cell_value(num_row-5,num_col-2))
        return resultado
    except:
        None

def limpiar_banreservas(texto):
    return texto.encode('utf-8').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")

def obtener_tarjeta_banreservas(tarjeta,info):
    resultado = {'avance_efectivo':'6%'}
    for dato in info:
        if comparar_banreservas(tarjeta,dato):
            for e in info[dato]:
                if 'emision' in e.lower() and not 'adicional' in e.lower():
                    resultado['emision'] = info[dato][e].replace('US$','USD$')
                elif 'renovacion' in e.lower() and not 'adicional' in e.lower():
                    resultado['renovacion'] = info[dato][e].replace('US$','USD$')
                elif 'seguro' in e.lower() and 'principal' in e.lower():
                    resultado['seguro_proteccion'] = info[dato][e].replace('US$','USD$')
                elif 'sobregiro' in e.lower():
                    resultado['sobregiro'] = info[dato][e].replace('US$','USD$')
                elif 'comision' in e.lower() and 'mora' in e.lower():
                    mora = info[dato][e].replace('US$','USD$')
                    if 'RD$' in mora:
                        resultado['comision_mora'] = mora[mora.find('RD$'):mora.find(' y')]+'/'+mora[mora.find('USD$'):]
                    else:
                        resultado['comision_mora'] = 'RD$'+mora[:mora.find('%')+1]
                elif 'tasa' in e.lower() and 'interes' in e.lower():
                    resultado['tasa_interes'] = info[dato][e].replace('Pesos:','RD$').replace('Dolares:','USD$')
            break
    return resultado





def comparar_banreservas(tarjeta,dato):
    tarjeta_list = tarjeta.split()
    n = 0
    for e in tarjeta_list:
        if e in dato.lower():
            n+=1
    if n == len(dato.split()) and len(tarjeta.split()) == len(dato.split()):
        return True
    return False
