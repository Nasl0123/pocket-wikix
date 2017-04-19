#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


p = re.compile("[0-9]+.[0-9]+%|([0-9]+%)|N/A|Gratis|([0-9]+,[0-9]+.[0-9]+)|([0-9]+.[0-9]+)|([0-9]+,[0-9]+)|([0-9]+)")
k = re.compile('([á-úÁ-Úa-zA-Z*-. &),(])+')
l = re.compile('([á-úÁ-Úa-zA-Z*-.),(])+')



def generar_apap(banco):
    try:
        a = formatear_apap(banco)
        return a
    except:
        None


def limpiar_apap(texto):
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


def formatear_apap(banco):
  a = open('txt/'+banco+'.txt','r').read()
  n=0
  lista = []
  while a.find('\n') != -1: 
     lista.append(a[270:a.find('\n')]) 
     n = a.find('\n')+1 
     a = a[n:]

  lista1 = []
  n = 0
  while n+2 < len(lista):
    new = k.search(lista[n])
    if new:
      new = lista[n][k.search(lista[n]).span()[1]+1:]
      if p.search(new) or l.search(new):
        lista1.append(lista[n].replace('/',' '))
        n += 1
      else:
        lista1.append(lista[n]+lista[n+2]+lista[n+1].replace('/',' '))
        n += 3
    else:
      n += 1
     
  dic = {}
  resultado = {}
  for n,e in enumerate(lista1):
    if 'Débito' in e:
      break
    val = []
    ind = e.replace('No aplica','N/A').replace('Anual','').replace('Mensual','')
    for x in p.finditer(ind):
      ind = ind.replace(x.group(),'').replace('  ','')
      val.append(limpiar_apap(x.group()))
    resultado[n] = {}
    resultado[n][limpiar_apap(ind)] = val
    
  final = {'emision_renovacion':{},
           'seguro_proteccion':{},
           'avance_efectivo':{},
           'comision_mora':{},
           'sobregiro':{},
           'tasa_interes':{}
  }
  for dat in resultado:
    if dat > 2 and dat < 7:
      for e in resultado[dat]:
        final['emision_renovacion'][e] = resultado[dat][e]
    elif dat == 8:
      for e in resultado[dat]:
        final['seguro_proteccion'][e] = resultado[dat][e]
    elif dat == 9:
      for e in resultado[dat]:
        final['avance_efectivo'][e] = resultado[dat][e]
    elif dat > 10 and dat < 15:
      for e in resultado[dat]:
        final['comision_mora'][e] = resultado[dat][e]
    elif dat == 15:
      for e in resultado[dat]:
        final['sobregiro'][e] = resultado[dat][e]
    elif dat > 16 and dat < 21:
      for e in resultado[dat]:
        final['tasa_interes'][e] = resultado[dat][e]
  return final

def obtener_tarjeta_apap(tarjeta, info):
    resultado = {'tasa_interes':''}
    for e in info:
        if e == 'seguro_proteccion':
            for dato in info[e]:
                if 'platinum' in tarjeta:
                    resultado[e] = 'RD$'+info[e][dato][1]
                else:
                    resultado[e] = 'RD$'+info[e][dato][0]
        elif e == 'sobregiro':
            for dato in info[e]:
                resultado[e] = 'RD$'+info[e][dato][0]
        elif e == 'avance_efectivo':
            for dato in info[e]:
                resultado[e] = info[e][dato][0]
        elif e == 'emision_renovacion':
            for dato in info[e]:
                if comparar_apap(dato,tarjeta):
                    resultado['emision'] = 'RD$'+info[e][dato][0]
                    resultado['renovacion'] = 'RD$'+info[e][dato][0]
        elif e == 'comision_mora':
            for dato in info[e]:
                if comparar_apap(dato,tarjeta):
                    resultado[e] = 'RD$'+info[e][dato][0]+'/USD$'+info[e][dato][1]
        elif e == 'tasa_interes':
            for dato in info[e]:
                if 'platinum' in tarjeta:
                    if 'rd hasta' in dato.lower():
                        resultado[e] += 'RD$'+info[e][dato][1]
                    elif 'us hasta' in dato.lower():
                        resultado[e] += '/USD$'+info[e][dato][1]
                elif comparar_apap2(dato,tarjeta):
                    resultado[e] = 'RD$'+info[e][dato][1]
    return resultado


def comparar_apap(dato,tarjeta):
    tarjeta_list = tarjeta.split()
    n = 0
    for e in tarjeta_list:
        if e in dato.lower():
            n+=1
    if n == len(tarjeta_list):
        return True
    return False

def comparar_apap2(dato,tarjeta):
    tarjeta_list = tarjeta.split()
    for e in tarjeta_list:
        if e in dato.lower():
            return True
    return False
                    
