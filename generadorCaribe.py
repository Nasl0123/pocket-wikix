#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

p = re.compile("[0-9]+.[0-9]+%|([0-9]+%)|N/A|Gratis|([0-9]+,[0-9]+.[0-9]+)|([0-9]+.[0-9]+)|([0-9]+,[0-9]+)|([0-9]+)|-")
j = re.compile('[..]+[…]+[..]+[…]+|[..]+[…]+[..]+|[…]+[..]+|[..]+[…]+|[…]+|[.]+[..]+|[..]+[.]+')
k = re.compile('([á-úÁ-Úa-zA-Z0-9$-. ),(])+')


def generar_caribe(banco):
    try:
        a = formatear_caribe(banco)
        return a
    except:
        None


def limpiar_caribe(texto):
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


def formatear_caribe(banco):
    a = open('txt/'+banco+'.txt','r').read()
    num, b, c, z = 0, 0, 0, 0
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
    element_list = {0:'',1:''}
    while i < len(si):
        lim = 0
        linea = a[n:si[i] + 1]
        if buscar_tarjeta(limpiar_caribe(linea)):
          element = k.search(linea[:60])
          element_list[lim] = element.group()
          lim += 1
          element = k.search(linea[60:])
          element_list[lim] = limpiar_caribe(element.group())
          lim += 1
        if not resultado.get(element_list[0]):
            resultado[element_list[0]] = {}
            resultado[element_list[1]] = {}
        l = i
        lim = 0
        for e in j.finditer(linea):
            if b + c == 0:
                b, c = e.span()
            if b < 60:
              used = resultado[element_list[0]]
            else:
              used = resultado[element_list[1]]
            if not lines:
                line = k.search(linea[lim:b])
                if line:
                    line = line.group()
                else:
                    line = ''
                line = limpiar_caribe(line) + str(lim)
            else:
                line = lines
            used[line] = []
            final = used[line]
            for x in p.finditer(linea):
                d, f = x.span()
                if d > b and (linea[c + 1:d].find('…') == -1 and linea[c + 1:d].find('...') == -1):
                    final.append(limpiar_caribe(linea[d:f]))
                    lim = f
            if len(final) == 0:
                lines = line
            else:
                lines = None
                b, c = 0, 0
        if len(final) == 0:
            linea = a[si[i]:si[i + 1] + 1]
            for x in p.finditer(linea):
                d, f = x.span()
                if (linea[c + 1:d].find('…') == -1 and linea[c + 1:d].find('...') == -1):
                    final.append(limpiar_caribe(linea[d:f]))
                    lim = f
            lines, b, c = None, 0, 0
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

def buscar_tarjeta(info):
  busqueda = ['otros tarjetas','clasica','oro local','extralimite','unica casoline','e-card','platinum','elite']
  for e in busqueda:
    if e in info.lower():
      return True
  return False

def obtener_tarjeta_caribe(tarjeta, info):
    resultado = {'avance_efectivo':'6.5%'}
    det = 'RD$'
    if 'card' in tarjeta:
        det = 'USD$'
    for dato in info:
        if comparar_caribe(dato,tarjeta):
            for x in info[dato]:
                if 'emision' in x.lower():
                    resultado['emision'] = det + info[dato][x][0]
                elif 'mantenimiento' in x.lower() and 'anual' in x.lower():
                    resultado['renovacion'] = det + info[dato][x][0]
                elif 'seguro' in x.lower() and 'proteccion' in x.lower():
                    resultado['seguro_proteccion'] = det + info[dato][x][0]
                elif 'tasa' in x.lower() and 'interes' in x.lower():
                    resultado['tasa_interes'] = det + info[dato][x][0]
                elif 'membresia' in x.lower():
                    resultado['membresia'] = det + info[dato][x][0]
                elif 'mora' in x.lower():
                    resultado['comision_mora'] = det + info[dato][x][0]
                elif 'sobregiro' in x.lower():
                    resultado['sobregiro'] = det + info[dato][x][0]
                
    return resultado
                

def comparar_caribe(dato,tarjeta):
    tarjeta_list = tarjeta.split()
    dato = limpiar_caribe(dato)
    if 'otros tarjeta' in dato.lower():
        return True
    for e in tarjeta_list:
        if e in dato.lower():
            return True
    return False
