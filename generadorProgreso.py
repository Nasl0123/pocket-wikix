import sys
sys.path.insert(0, 'libs')
import pdftables_api
import xlrd
import xlwt

c = pdftables_api.Client('fc9wow7u2a9c')
def crear_xlsx(banco):
    c.xlsx(banco+'.pdf', 'xlsx/'+banco+'_output.xlsx')

def generar_progreso(banco):
    try:
        a = formatear_progreso(banco)
        return a[1]
    except:
        None


def formatear_progreso(banco):
    try:
        book = xlrd.open_workbook('xlsx/'+banco+'_output.xlsx')
        sheet = book.sheet_by_index(2)
        var = ''
        for row in range(27,54):
            for col in range(0,10):
                if type(sheet.cell_value(row,col)) == float:
                    var += str(sheet.cell_value(row,col)).replace(',','')+'|'
                else:
                    var += sheet.cell_value(row,col).replace(',','')+'|'


        # for row in range(2,60):
        #     if sheet.cell_value(row,3) == '':
        #         var += sheet.cell_value(row,2)+'|'
        #     else:
        #         var += sheet.cell_value(row,3)+'|'
        #var = limpiar(var[:var.find('Visa Prestige')]+'|'+var[var.find('Visa Prestige'):]+'^')
        #var = var.replace(',','|')
        var = var.encode('utf-8').replace('\xc2\xae','').replace("\xc3\xa1","a").replace("\xc3\xa9","e").replace("\xc3\xad","i").replace("\xc3\xb3","o").replace("\xc3\xba","u").replace("\xc3\x81","A").replace("\xc3\x89","E").replace("\xc3\x8d","I").replace("\xc3\x93","O").replace("\xc3\x9a","U").replace("\xc3\xb1","n").replace("\xc3\x91","N").replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")
        lista = var.split('|')
        #return repr(sheet.cell_value(num_row-5,num_col-2))
        return (var,lista)
    except:
        None

def obtener_tarjeta_progreso(tarjeta,info):
    busqueda = ['emision',
                'renovacion',
                'renovacion_adicional',
                'reemplazo',
                'comision_mora_rd',
                'comision_mora_usd',
                'sobregiro_rd',
                'sobregiro_usd',
                'seguro_proteccion']
    resultado = {'tasa_interes':'60%',
                 'avance_efectivo':'6%'}
    i = 0
    while i < len(info):
        if comparar_progreso(tarjeta,info[i]):
            for n,e in enumerate(info[i+1:i+10]):
                resultado[busqueda[n]] = e
            break
        i+=1
    return limpiar(resultado)

def limpiar(info):
    eliminar = []
    resultado = {}
    for e in info:
        if e == 'renovacion_adicional' or e == 'reemplazo':
            eliminar.append(e)
        elif info[e] == 'N/A':
            eliminar.append(e)
    for s in eliminar:
        del info[s]
    eliminar = []
    if info.get('emision') == '':
        info['emision'] = 'GRATIS'
    if info.get('comision_mora_rd') and info.get('comision_mora_usd'):
        info['comision_mora'] = info.get('comision_mora_rd')+'/'+info.get('comision_mora_usd')
        eliminar += ['comision_mora_rd'] + ['comision_mora_usd']
    elif info.get('comision_mora_rd'):
        info['comision_mora'] = info.get('comision_mora_rd')
        eliminar += ['comision_mora_rd']
    if info.get('sobregiro_rd') and info.get('sobregiro_usd'):
        info['sobregiro'] = info.get('sobregiro_rd')+'/'+info.get('sobregiro_usd')
        eliminar += ['sobregiro_rd'] + ['sobregiro_usd']
    elif info.get('sobregiro_rd'):
        info['sobregiro'] = info.get('sobregiro_rd')
        eliminar += ['sobregiro_rd']
    for s in eliminar:
        del info[s]
    return info
    

def comparar_progreso(tarjeta,dato):
    tarjeta_list = tarjeta.split()
    n = 0
    for e in tarjeta_list:
        if e in dato.lower():
            n+=1
    if n == len(tarjeta_list):
        return True
    return False
