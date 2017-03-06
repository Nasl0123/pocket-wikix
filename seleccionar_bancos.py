# -*- coding: cp1252 -*-
import random

hechos = [1,4,8,9,11,15,16,18,20,21,22,23]

lista = [x for x in range(1,24)]
def seleccionar():
  return [random.choice(lista) for x in range(3)]
  
def descartar():
  return [lista.remove(x) for x in hechos]
  
descartar()
print seleccionar()
