# -*- coding: cp1252 -*-
import random

hechos = [3,5,7,12,16]

lista = [x for x in range(1,24)]
def seleccionar():
  #return [random.choice(lista) for x in range(3)]
  return [random.choice(hechos) for x in range(3)]
  
def descartar():
  #return [lista.remove(x) for x in hechos]
  return None
  
descartar()
print seleccionar()
