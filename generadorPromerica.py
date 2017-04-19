#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
sys.path.insert(0, 'libs')
import xlrd
import xlwt
import re

p = re.compile("([0-9]+%)|([0-9]+.[0-9]+%)|N/A|Gratis|([U])([S])([D])([$])([0-9]+.[0-9]+)|([U])([S])([D])([0-9]+.[0-9]+)|([R])([D])([$])([0-9]+.[0-9]+)|([R])([D])([$])([0-9]+)|([R])([D])([$])([0-9]+.[0-9]+)[ - ]([U])([S])([D])[ ]([0-9]+.[0-9]+)|([0-9]+)")
j = re.compile(
    '([…]+)([.]+)([…]+)([.]+)([…]+)([.]+)([…]+)([.]+)([…]+)|([…]+)([.]+)([…]+)([.]+)([…]+)([.]+)([…]+)([.]+)|([…]+)([.]+)([…]+)([.]+)([…]+)([.]+)([…]+)|([…]+)([.]+)([…]+)([.]+)([…]+)([.]+)|([…]+)([.]+)([…]+)([.]+)([…]+)|([…]+)([.]+)([…]+)([.]+)|([…]+)([.]+)([…]+)|([…]+)([.]+)|[…]+|Mora')
k = re.compile('([á-úÁ-Úa-zA-Z0-9$-. ),(])+')

def generar_promerica(banco):
    try:
        a = formatear_promerica(banco)
        return a
    except:
        None
        
def limpiar_promerica(texto):
    return texto.replace('  ', '').replace(',', '').replace('\n', ' ').replace('US$', 'USD$').replace('\xe2\x80\x93',
                                                                                                      '').replace(
        "\xc3\xa1", "a").replace("\xc3\xa9", "e").replace("\xc3\xad", "i").replace("\xc3\xb3", "o").replace("\xc3\xba",
                                                                                                            "u").replace(
        "\xc3\x81", "A").replace("\xc3\x89", "E").replace("\xc3\x8d", "I").replace("\xc3\x93", "O").replace("\xc3\x9a",
                                                                                                            "U").replace(
        "\xc3\xb1", "n").replace("\xc3\x91", "N").replace("\xc1", "A").replace("\xe1", "a").replace("\xc9",
                                                                                                    "E").replace("\xe9",
                                                                                                                 "e").replace(
        "\xcd", "I").replace("\xed", "i").replace("\xd3", "O").replace("\xf3", "o").replace("\xda", "U").replace("\xfa",
                                                                                                                 "u").replace(
        "\xd1", "N").replace("\xf1", "n")


def formatear_promerica(banco):
    a = open('txt/'+banco+'.txt','r').read()
    num,b,c,z = 0,0,0,0
    si = []
    final = []
    while a.find('\n', num) != -1:
        si.append(a.find('\n', num))
        num = a.find('\n', num) + 1
    resultado = {}
    i = 0
    l = i
    n = si[i]
    lines = None
    while i < len(si):
        lim = 0
        linea = a[n:si[i] + 1]
        if not resultado.get('linea_' + str(l)):
            resultado['linea_' + str(l)] = {}
            used = resultado['linea_' + str(l)]
        l = i
        for e in j.finditer(linea):
            if b + c == 0:
                b, c = e.span()
            if not lines:
              line = k.search(linea[lim:b])
              if line:
                  line = line.group()
              else:
                  line = ''
              line = limpiar_promerica(line)
            else:
              line = lines
            used[line] = []
            final = used[line]
            for x in p.finditer(linea):
                d, f = x.span()
                if d > b and (linea[c + 1:d].find('…') == -1 and linea[c + 1:d].find('Mora') == -1):
                    final.append(limpiar_promerica(linea[d:f]))
                    lim = f
            if len(final) == 0:
              lines = line
            else:
              lines = None
              b,c = 0,0
        if len(final) == 0:
          linea = a[si[i]:si[i+1] + 1]
          for x in p.finditer(linea):
              d, f = x.span()
              if (linea[c + 1:d].find('…') == -1 and linea[c + 1:d].find('Mora') == -1):
                  final.append(limpiar_promerica(linea[d:f]))
                  lim = f
          lines,b,c = None,0,0
          lim = 0
        n = si[i]
        i += 1
        l = i
    return quitar_vacios(resultado)


def quitar_vacios(resultado):
    borrar = []
    for s in resultado:
      for t in resultado[s]:
        if len(resultado[s][t]) == 0:
          borrar.append(t)
      for r in borrar:
        del resultado[s][r]
      borrar = []
    borrar = []
    for e in resultado:
      if len(resultado[e]) == 0:
        borrar.append(e)
    for x in borrar:
      del resultado[x]
    return resultado
        
def obtener_tarjeta_promerica(tarjeta,info):
    deter = 0
    resultado = {'tasa_interes':[],
                 'sobregiro':'RD$500.00/USD$12.50'}
    seccionGeneral,seccionBusiness,seccionBlack = {},{},{}
    for menos46 in info:
        if int(menos46.split('_')[1]) < 46 and int(menos46.split('_')[1]) > 30:
            seccionBusiness[menos46] = info[menos46]
    for menos31 in info:
        if int(menos31.split('_')[1]) < 31:
            seccionGeneral[menos31] = info[menos31]
    for menos76 in info:
        if int(menos76.split('_')[1]) < 76 and int(menos76.split('_')[1]) > 45:
            seccionBlack[menos76] = info[menos76]
    if 'clasica' in tarjeta:
        deter = 0
    elif 'gold' in tarjeta:
        deter = 1
    elif 'platinum' in tarjeta:
        deter = 2
    elif 'business' in tarjeta:
        deter = 3
    elif 'infinite' in tarjeta or 'black' in tarjeta:
        deter = 4

    if deter < 3:
        for linea in seccionGeneral:
            for dato in seccionGeneral[linea]:
                if 'emision' in dato.lower() and not 'adicional' in dato.lower():
                    
                    resultado['emision'] = seccionGeneral[linea][dato][deter]
                if 'renovacion' in dato.lower() and not 'tarjeta' in dato.lower():
                    resultado['renovacion'] = seccionGeneral[linea][dato][deter]
                if 'renovacion' in dato.lower() and comparar_promerica(tarjeta,dato):
                    resultado['renovacion1'] = seccionGeneral[linea][dato][deter]
                if 'seguro' in dato.lower() and 'perdida' in dato.lower():
                    resultado['seguro_proteccion'] = seccionGeneral[linea][dato][deter]
                if 'avance' in dato.lower() and 'efectivo' in dato.lower():
                    resultado['avance_efectivo'] = seccionGeneral[linea][dato][deter]
                if 'pesos' in dato.lower():
                    resultado['tasa_interes'].append('RD$'+seccionGeneral[linea][dato][deter])
                if 'dolares' in dato.lower():
                    resultado['tasa_interes'].append('USD$'+seccionGeneral[linea][dato][deter])
                if ' cargo' in dato.lower() and 'por' in dato.lower():
                    resultado['comision_mora'] = seccionGeneral[linea][dato][deter]
    elif deter == 3:
        for linea in seccionBusiness:
            for dato in seccionBusiness[linea]:
                if 'emision' in dato.lower():
                    resultado['emision'] = seccionBusiness[linea][dato][0]
                if 'renovacion' in dato.lower():
                    resultado['renovacion'] = seccionBusiness[linea][dato][0]
                if 'seguro' in dato.lower() and 'perdida' in dato.lower():
                    resultado['seguro_proteccion'] = seccionBusiness[linea][dato][0]
                if 'cargo' in dato.lower() and 'por' in dato.lower():
                    resultado['comision_mora'] = seccionBusiness[linea][dato][0]
        resultado['tasa_interes'] = '36%'
    elif deter == 4:
        for linea in seccionBlack:
            for dato in seccionBlack[linea]:
                if 'emision' in dato.lower():
                    resultado['emision'] = seccionBlack[linea][dato][0]
                if 'renovacion' in dato.lower():
                    resultado['renovacion'] = seccionBlack[linea][dato][0]
                if 'seguro' in dato.lower():
                    resultado['seguro_proteccion'] = seccionBlack[linea][dato][0]
                if 'interes' in dato.lower() and 'financiamiento' in dato.lower():
                    resultado['tasa_interes'].append('RD$'+seccionBlack[linea][dato][0])
                    resultado['tasa_interes'].append('RD$'+seccionBlack[linea][dato][1])
                if 'retiro' in dato.lower():
                    resultado['avance_efectivo'] = '6.25%'
                
    if resultado.get('renovacion1'):
        resultado['renovacion'] = resultado['renovacion1']
        del resultado['renovacion1']
    if type(resultado['tasa_interes']) == list:
        resultado['tasa_interes'] = resultado['tasa_interes'][0]+'/'+resultado['tasa_interes'][1]
    return resultado

def comparar_promerica(tarjeta,dato):
    tarjeta_list = tarjeta.split()
    for e in tarjeta_list:
        if e in dato.lower():
            return True
    return False
