#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'libs')
from bs4 import BeautifulSoup
from urllib import FancyURLopener
from indices import limpiar

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

def datos_tarjeta(banco,tarjeta=None):
    if not tarjeta:
        return (None,None,None)
    tree = None
    link = {}
    path = {}
    if banco == 'Popular':
        tree = ['div','fullbleed-grid row details','class']
        link = {'clasica':['https://www.popularenlinea.com/clasica'],
                'orbit':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/orbit.aspx'],
                'clasica internacional':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/clasica-facturation-en-dolares.aspx'],
                'prestige':['https://www.popularenlinea.com/visaprestige'],
                'gold':['https://www.popularenlinea.com/gold'],
                'gold internacional':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/gold-facturacion-en-dolares.aspx'],
                'platinum':['https://www.popularenlinea.com/platinum'],
                'platinum internacional':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/platinum-dolares.aspx'],
                'black':['https://www.popularenlinea.com/mastercardblack'],
                'black internacional':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/mastercard-black-dolares.aspx'],
                'fcbescola':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/Tarjeta-Credito-FCBEscola.aspx'],
                'jetblue':['https://www.popularenlinea.com/jetblue'],
                'ccn plus':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/mastercard-ccnpPlus.aspx'],
                'mileage plus':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/mastercard-mileage-plus.aspx'],
                'mb signature':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/mb-visa-signature-card.aspx'],
                'ikea family':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/ikea-family.aspx'],
                'seguros universal':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/mc-seguros.aspx'],
                'caminantes por la vida':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/caminantes-por-la-vida.aspx'],
                'almacenes iberia':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/mastercard-almacenes-iberia.aspx'],
                'sirena':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/visa-pola-sirena.aspx'],
                'avanza':['https://www.popularenlinea.com/Personas/Paginas/tarjetas/avanza.aspx']}

        path = {'clasica':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'orbit':['div','col-md-4 col-sm-4 col-xs-12'],
                'clasica internacional':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'prestige':['div','row grid-line-row'],
                'gold':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'gold internacional':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'platinum':['div','col-md-4 col-sm-4 col-xs-12'],
                'platinum internacional':['div','col-md-4 col-sm-4 col-xs-12'],
                'black':['div','col-md-4 col-sm-4 col-xs-12'],
                'black internacional':['div','col-md-4 col-sm-4 col-xs-12'],
                'fcbescola':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'jetblue':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'ccn plus':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'mileage plus':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'mb signature':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'ikea family':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'seguros universal':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'caminantes por la vida':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'almacenes iberia':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'sirena':['div','col-md-3 col-sm-3 col-xs-12 grid-item'],
                'avanza':['div','col-md-3 col-sm-3 col-xs-12 grid-item']}

    if banco == 'LopezDeHaro':
        tree = ['table','tabla-verticalA','class']
        link = {'clasica':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx'],
                'casa de espana':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx'],
                'club hemingway':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx'],
                'club naco':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx'],
                'gold':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx'],
                'golds gym':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx'],
                'platinum':['http://www.blh.com.do/Inicio/Productos/Tarjetas-de-cr%C3%A9dito.aspx']}

        path = {'clasica':['td','tabla-verticalA_celdaAzul'],
                'casa de espana':['td','tabla-verticalA_celdaAzul'],
                'club hemingway':['td','tabla-verticalA_celdaAzul'],
                'club naco':['td','tabla-verticalA_celdaAzul'],
                'gold':['td','tabla-verticalA_celdaAzul'],
                'golds gym':['td','tabla-verticalA_celdaAzul'],
                'platinum':['td','tabla-verticalA_celdaAzul']}
    if banco == 'Progreso':
        tree = ['div','overview_wrap','id']
        link = {'casa de campo':['http://www.americanexpress.com.do/personal/our-cards/TC_platinum_casadecampo.html'],
                'american express':['http://www.americanexpress.com.do/personal/our-cards/TC_personal.html'],
                'american express gold':['https://www.livegold.do/'],
                'suma ccn':['http://www.americanexpress.com.do/personal/our-cards/TC_suma_ccn.html'],
                'gold':['http://www.progreso.com.do/index.php/tarjetas-de-credito-mastercard-gold-internacional'],
                'internacional':['http://www.progreso.com.do/index.php/tarjetas-de-credito-mastercard-internacional'],
                'local':['http://www.progreso.com.do/index.php/tarjetas-de-credito-mastercard-local'],
                'platinum':['http://www.progreso.com.do/index.php/tarjetas-de-credito-mastercard-platinum-internacional'],
                'platinum card':['http://www.americanexpress.com.do/platinum/priority.html',
                                 'http://www.americanexpress.com.do/platinum/vip.html',
                                 'http://www.americanexpress.com.do/platinum/lifestyle.html',
                                 'http://www.americanexpress.com.do/platinum/rewards.html',
                                 'http://www.americanexpress.com.do/platinum/protection.html',
                                 'http://www.americanexpress.com.do/platinum/cardmember_services.html']}

        path = {'casa de campo':['div','overview_all_data'],
                'american express':['div','overview_all_data'],
                'american express gold':['div','row','class'],
                'suma ccn':['div','overview_all_data'],
                'gold':['table','contentpaneopen','class'],
                'internacional':['table','contentpaneopen','class'],
                'local':['table','contentpaneopen','class'],
                'platinum':['table','contentpaneopen','class'],
                'platinum card':['div','PlatinumContentMain','id']}

        diferentes = ['american express gold','gold','internacional','local','platinum','platinum card']
        if tarjeta in diferentes:
            if tarjeta == 'american express gold':
                tree = ['div','benefits-container','id']
            elif tarjeta == 'platinum card':
                tree = ['div','ContentFeature','id']
            else:
                tree = ['div','mainbody','id']
    if banco == 'ACAP':
        tree = ['div','item-page clearfix','class']
        link = {'gold':['https://www.acap.com.do/site2/index.php/banca-personal/tarjeta-de-credito/tarjeta-de-credito-visa-gold'],
                'clasica':['https://www.acap.com.do/site2/index.php/banca-personal/tarjeta-de-credito/visa-clasica-local'],
                'clasica internacional':['https://www.acap.com.do/site2/index.php/banca-personal/tarjeta-de-credito/visa-clasica-internacional']}

        path = {'gold':['ul','ja-unordered-list'],
                'clasica':['ul','ja-unordered-list'],
                'clasica internacional':['ul','ja-unordered-list']}

    if banco == 'ALNAP':
        tree = ['div','article-content','class']
        link = {'clasica local':['http://www.alnap.com.do/productos/personas/tarjetas/clasica-local'],
                'clasica internacional':['http://www.alnap.com.do/productos/personas/tarjetas/tarjeta-clasica-internacional'],
                'gold':['http://www.alnap.com.do/productos/personas/tarjetas/tarjeta-de-credito-gold'],
                'confiamas':['http://www.alnap.com.do/productos/tarjeta-de-credito-confiamas'],
                'confia en ti local':['http://www.alnap.com.do/productos/confia-en-ti'],
                'confia en ti internacional':['http://www.alnap.com.do/productos/confia-en-ti'],
                'unase local':['http://www.alnap.com.do/productos/personas/tarjetas/tarjeta-visa-unase'],
                'unase internacional':['http://www.alnap.com.do/productos/tarjeta-visa-unase-internacional'],
                'union local':['http://www.alnap.com.do/productos/tarjeta-visa-union'],
                'union internacional':['http://www.alnap.com.do/productos/tarjeta-visa-union'],
                'compramas':['http://www.alnap.com.do/productos/personas/tarjetas/compramas']
                }

        path = {'clasica local':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'clasica internacional':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'gold':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'confiamas':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'confia en ti local':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'confia en ti internacional':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'unase local':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'unase internacional':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'union local':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'union internacional':['div','field field-name-field-content-tab field-type-text-long field-label-hidden'],
                'compramas':['div','field field-name-field-content-tab field-type-text-long field-label-hidden']
                }

    if banco == 'BDI':
        tree = ['div','component-content','class']
        link = {'local':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/tarjetas-visa-bdi'],
                'clasica':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/tarjetas-visa-bdi'],
                'gold':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/tarjetas-visa-bdi'],
                'signature':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/tarjeta-signature'],
                'anthonys clasica':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/tarjeta-anthony-s'],
                'anthonys gold':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/tarjeta-anthony-s'],
                'anthonys platinum':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/tarjeta-anthony-s'],
                'signature bm cargo':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/bmcargo'],
                'crediplan':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/credito-diferido'],
                'bm cargo local':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/bmcargo'],
                'bm cargo clasica':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/bmcargo'],
                'bm cargo gold':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/bmcargo'],
                'fundapec clasica':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/tarjeta-fundapec'],
                'plaza central clasica':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/plaza-central'],
                'plaza central local':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/plaza-central'],
                'plaza central gold':['https://www.bdi.com.do/index.php/productos-y-servicios/tarjetas-de-credito/visa-marca-compartida/plaza-central']
                }

        path = {'local':['article','item-page'],
                'clasica':['article','item-page'],
                'gold':['article','item-page'],
                'signature':['article','item-page'],
                'anthonys clasica':['article','item-page'],
                'anthonys gold':['article','item-page'],
                'anthonys platinum':['article','item-page'],
                'signature bm cargo':['article','item-page'],
                'crediplan':['article','item-page'],
                'bm cargo local':['article','item-page'],
                'bm cargo clasica':['article','item-page'],
                'bm cargo gold':['article','item-page'],
                'fundapec clasica':['article','item-page'],
                'plaza central clasica':['article','item-page'],
                'plaza central local':['article','item-page'],
                'plaza central gold':['article','item-page']
                }
                
    if banco == 'Scotiabank':
        tree = ['div','a overview content','class']
        link = {'scotiabank gold visa':['http://www.scotiabank.com/do/es/0,,6986,00.html','http://www.scotiabank.com/do/es/0,,6988,00.html'],
                'scotiabank mastercard':['http://www.scotiabank.com/do/es/0,,6985,00.html'],
                'scotiabank visa':['http://www.scotiabank.com/do/es/0,,6987,00.html'],
                'scotiabank platinum visa':['http://www.scotiabank.com/do/es/0,,6991,00.html','http://www.scotiabank.com/do/es/0,,6997,00.html'],
                'scotiabank aadvantage visa':['http://www.scotiabank.com/do/es/0,,6992,00.html'],
                'scotiabank aadvantage gold mastercard':['http://www.scotiabank.com/do/es/0,,6993,00.html','http://www.scotiabank.com/do/es/0,,6994,00.html'],
                'scotiabank aadvantage platinum visa':['http://www.scotiabank.com/do/es/0,,6995,00.html'],
                'scotiabank pricesmart diamond mastercard':['http://www.scotiabank.com/do/es/0,,6996,00.html'],
                'scotiabank bravo visa':['http://www.scotiabank.com/do/es/0,,7154,00.html'],
                'scotiabank orange mastercard':['http://www.scotiabank.com/do/es/0,,7155,00.html'],
                'scotiabank visa infinite':['http://www.scotiabank.com/do/es/0,,9492,00.html']}

        path = {'scotiabank gold visa':['div','bullets'],
                'scotiabank mastercard':['div','bullets'],
                'scotiabank visa':['div','bullets'],
                'scotiabank platinum visa':['div','bullets'],
                'scotiabank aadvantage visa':['div','bullets'],
                'scotiabank aadvantage gold mastercard':['div','bullets'],
                'scotiabank aadvantage platinum visa':['div','bullets'],
                'scotiabank pricesmart diamond mastercard':['div','bullets'],
                'scotiabank bravo visa':['div','bullets'],
                'scotiabank orange mastercard':['div','bullets'],
                'scotiabank visa infinite':['div','bullets']}

    if banco == 'BanReservas':
        tree = ['div','beneficios-previews cms-content','class']
        link = {'visa / mastercard / mastercard multimoneda gold':['https://www.banreservas.com/products/visa-y-mastercard-gold'],
                'mastercard platinum':['https://www.banreservas.com/products/mastercard-platinum'],
                'visa clasica y mastercard standard':['https://www.banreservas.com/products/visa-clasica-y-mastercard-standard'],
                'visa y mastercard multimoneda':['https://www.banreservas.com/products/visa-y-mastercard-multimoneda'],
                'visa platinum universe':['https://www.banreservas.com/products/visa-platinum-universe'],
                'visa infinite':['https://www.banreservas.com/products/visa-infinite']}
        
        path = {'visa / mastercard / mastercard multimoneda gold':['div','beneficios-preview'],
                'mastercard platinum':['div','beneficios-preview'],
                'visa clasica y mastercard standard':['div','beneficios-preview'],
                'visa y mastercard multimoneda':['div','beneficios-preview'],
                'visa platinum universe':['div','beneficios-preview'],
                'visa infinite':['div','beneficios-preview']}

    if banco == 'SantaCruz':
        tree = ['div','article-content','class']
        link = {'clasica':['https://www.bsc.com.do/~bsccom/soluciones-personales/tarjetas/tarjetas-de-credito/tarjeta-de-credito-clasica/'],
                'oro':['https://www.bsc.com.do/~bsccom/soluciones-personales/tarjetas/tarjetas-de-credito/tarjeta-de-credito-gold/'],
                'platinum':['https://www.bsc.com.do/~bsccom/soluciones-personales/tarjetas/tarjetas-de-credito/tarjeta-de-credito-platinum/'],
                'infinite':['https://www.bsc.com.do/~bsccom/soluciones-personales/tarjetas/tarjeta-de-credito-infinite/'],
                'multicredito':['https://www.bsc.com.do/~bsccom/soluciones-personales/tarjetas/multicredito/'],
                'full car':['https://www.bsc.com.do/~bsccom/soluciones-personales/tarjetas/full-car/'],
                'cecomsa':['https://www.bsc.com.do/~bsccom/soluciones-personales/tarjetas/tarjeta-cecomsa/']}

        path = {'clasica':['div','entry-body'],
                'oro':['div','entry-body'],
                'platinum':['div','entry-body'],
                'infinite':['div','entry-body'],
                'multicredito':['div','entry-body'],
                'full car':['div','entry-body'],
                'cecomsa':['div','entry-body']}

    if banco == 'BHD':
        tree = ['div','tab_container','class']
        link = {'clasica local':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tVNdb4IwFP0r-uAjacUi9ZHsy80tJLBN6YsphWodtAgdbv_eu2XLnpQshr60zT33nJObexBDK8Q0b9WGW2U0L-CfsOmazK7xPSHjxd38FuPAffRmcRRGV3OCXhFDTGhb2S1K0m02wkorocwIp1wLPqjyugGmEba83uWWN38vUeeZsoCsapO9C2ugxp1Bqxo-EAVvFLQXRoALkKiEylBCpz7x6TRzJjijDqEydaiU0uEUS-lKV4zdMVp2eWZQxidOgKGffUNOMCxirwMQ_gLOiCRg0j9t0kfLVuUH9KJNXcIE4n_OYN6lMHMvVOig9_qkd0O_V3pCLqR_OLcfXysIuVK7_Z4FEB6jbf5h0aqv9FRlSSefzltED89yuynXTzcT7-cqNsPhEX567X4!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'standard local':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tVPLbsIwEPwVOHCMbBInJMeoL1paIUFbiC_I3hhiSuzguND-fU3VqqcQVSi-eK0dz4xWO4iiJaKKHeSGWakV27l3RqMVSa7xPSHDyd34FuPUfwyT-Ww6uxoT9IoooqBsZQuU8SIfYKkkSD3AnClgvUqY2jENsGVmKyyr_yowIpfWISuj83ew2vW41ytZbYUBZvJebZnKT8VOgzPjlCqQOcoA-xh8HnsBF7FHOAQeB8BePOQR40G0DhOBFm3WqWvjhpNi959-QxoYJvOwBTD9BZwRyZzJUbPJEVocpDiiF6VN6SYw_-cMxm0KiX-hQgt92CW9Px11Sk_IhfQP5_bjtIIuXnK739PUZUgrKz4sWnYcoqos4-DTe5vFx-d1sSlXTzdB-HPtNv3-F1d2JtI!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'clasica premia':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tVNdb4IwFP0r-OAjaYFi5ZHsy80tJLBN6Yu5lKJ1UrB0uv371WXLnpQsxr60zT33nJP2HsTQHDEFO7kEIxsFG3vP2WhBomt8T4g3vZvcYhz7j2GUpUl6NSHoFTHEuDKtWaG8WJVDLJXkshniAhQHpxW6s0xDbECvhYHu78S1KKWxyFY35Ts3ja1x19nJDhy-gU4e2rWoJRw0Wi5LlHs4qGhVFi6MKLjEp4Vb0CpygxCL0IcKe7RAsz7TzJbxkRVj28--IUcYplnYA0h-ASdEcmuSHjdJ0WwnxR69qEbX9iOyf77BpE8h8s9U6KEPL0nvJ_Si9IScSf9waj4OI2iDJdfbLYttehplxIdB84vFp63rcfDpvqXj_XO1WtaLp5sg_Nk2y8HgCz2JFF0!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'clasica internacional':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tVPLbsIwEPwVOORo2TUOSY6or7S0QoK2EF-QH0kwJU5IXGj_nu1LPUFUofhiWzs7M1rNYo4XmFuxM7lwprRiA_-ED5csuiJ3jF2Mb-MbQkb0wY9m08n0Mmb4BXPMlXWVW-FErrRHjDXKlB6RwirRq9K6ASaPOFGvUyeav5eqU20cIKu61G_KlVDTqLczjeipjWgMtBvr0toK9e0GpCplNE40i6gMpUYi0xliQkkUDiOKMhYwGko_iIjG8zbvHMrkyBkR6OdfkCMM45nfApj8Ak6IJGAyOG4ywPOdSff42ZZ1AROY_XMGcZtCRM9UaKH3u6Snk6BTesbOpL8_lY_PCMJ-mfV2y0ewRCVk_d3hRddbVBVFOPhAr9Nw_5St8mL5eD3wf65N3u8fAIh6K2o!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'standard internacional':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/vVPLbsIwEPwVOHCMbBIHkyPqi5ZWSNAW4gtabAOmxAmOC-3fd-lDPYWoQtQXr73jmfVqlggyJcLCzizBm9zCBs-p6MxYcklvGWsPbvrXlPbC-zgZj4ajiz4jz0QQIa0v_Iqk85VqUWONNHmLzsFKaBTalcjUoh7cWnsofyPptDIekYXL1av0OeZ00Mig9NpJcKpRerDqEBiLVxbkV1GoWEijSBpG7XaXdniwYKEKGHSSAGIJwUJFHPg84TpWZFL3BYFpWrF6FN-LT0gFw2Ac1wCGP4AjIikWyauL5GSyM3pPnmzuMuzA-I896NcpJOGJCjX08TnpwyE_Kz1jJ9LfHfPHwYI4Zma93YoezlKOXn_zZPpPw1RkWTd6D15G3f3jYrXMZg9XUfy9bZbN5gdcBKLW/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'mi pais':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tZNdb8IgFIb_Sr3wsgFbOuSy2Vc3tzTRbVpuDAXa4izUlun274fLll1pszi5gZPz8rwncA6gYAGoZltVMquMZmsXZ_RiicgVvENoNLlNbiCMg4eIzKbp9DJB4AVQQLm2ja1AlldiCJVWXJkhzJnmzGtk2znSEFrWrqRl3e-Jt1Io65RNa8Qbt8blCt_bqo55tfIapro9vOFKgAwiIfE4Zz4PRpGPMMQ-gYT5IoQ5KaQg4agA875qqUvDAyuG7j79khwgTGZRjyD9ERwxyVyR-HCRGMy3Su7AszZt7X5g9sc3SPocSHCiQw8-Oic-SPFZ8QidiL8_1h_7FnQTpVabDY3d2Bht5bsFi_-fm6aux-GH_zod756KqqyXj9dh9L2ty8HgEwp3v34!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'gold internacional':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tZNdT4MwFIb_CrvgkrR2ZcAl8Ws6zZKhbvRmKW2FTmgZVKb_fp3ReMWImetNe3LePufNyTmAgBUginYyp0ZqRUsbp2SyxtEVvMP4YnY7vYEwRg9-lCzmi8spBi-AAMKUqU0B0qzgLpRKMqldmFHFqFOLprUkFxrabISh7e-LNYJLY5V1o_k7M9rmCs_pZEudXJf8QK6Z5CBFEcIiRJGHeUY9a4R7kc-QFwrGJihj_iTLwHLIKrFp2HNiaP-TL0kPYZb4A4L5j-BIkdSaDPpNBmDZSbEDz0o3lW1_8sceTIcqROjECgN4_5x4NA_Oisf4RPz9sfk4jKBdJ7nZbklsd0YrIz4MWP3z0tRVFY4_vbdFuHt6LfJq_Xg99r-vMh-N9pNYYm4!/dz/d5/L2dBISEvZ0FBIS9nQSEh/','https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tZPLbsIwEEV_BRYsLbvEeS1RX2lphQRtId4gv0hMEzsYF9q_x1StuoKoQvHGHs31uSN7BhK4gETTnSqoU0bTysc5iZY4vUEPGF-N77M7hEbDpzCdTSfT6wzDN0gg4do1roQ5K8UAKa24MgPEqOa010i79aQBctSupaPbvxO3UijnlY014oM743MK9Gq6ddJyakWvMJU48huuBMyTgDMWRTGgIUMAYy4BQ3EKIiHCBEUJ4sEKztsKJj6NTqwR8vfJt-QEYTwLWwSTX8EZk9wXGZ8uMobznZJ7-KqNrf0nzP75BlmbQzq80KEFH3aJH07iTvEYX4h_PNcfxxb0Q6XWmw0Z-ckx2slPBxedjE5T10nwBd6nyf5lVRb18vk2CH-2quj3Dwq5ONc!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'gold mujer':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tVNdb8IgFP0r9cHHBtbSlj6afbm5pUndh-XFUMBK10JF1O3fi8uWPWmzGHngI_fccy5wDyBgBoiiW1lRK7WijTsXJJ6j9AY-IHQ1uR_fQTgKnqJ0mmf59RiBN0AAYcp2dgmKcsmHUCrJpB7CkipGvU6YtWMaQktNLSxd_-2YEVxah-yM5htmtYvVvtfStRWGUcO9Sjfcaze1MAeVjkkOijRKwzKOY7_EZeCjgKc-5m4KMcbxgpUMRgl47yubuDA8MkbQ5ZNvyBGGyTTqAWS_gBMihSsyOV6ku8VWih14Vdq07ium_3yDcZ9CGpyp0EMfXZI-yJKL0iN0Jv3jqf44tKCzlqxXKzJy_tHKik8LZhc0UNe2OPzyP3K8e1ksq3b-fBtGP0tTDQZ76p2o8g!!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'gold premia':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tZNdb4IwFIb_Cl54SVqhfF2afbG5hQS2qb0xpS1QhRah0-3fW5ctu1KyGHvTnpy3z3vSngMwWAAsyU6URAslSW3iJfZXKLqFjwhNZg_xPYRT59mLsjRJb2IE3gEGmErd6gos84qNoZCCCjWGOZGUWC3vekMaQ026Ndek_zvRjjOhjbLtFPugWpncxrZ2oidWqWpmtR1vBDkatFQwgy-gDylnNstDZiM3D2wCaWQXnBRBOGEu8RmYD1WMTRqeWFNo7uNvyQnCLPMGBMmv4IzJ0hQZnC4yAPOd4HvwJlXXmF_I_vkG8ZBD5FzoMID3rol3kuCqeIQuxD-d649jC5qpEuvtFk_N6Cip-acGi-vMTts0oftlb9Jw_1pUZbN6uXO9n60uR6MDGp_Hpw!!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'mlb':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tVPLbsIwEPyVcOAY2QSnSY5RX7S0QoK2EF_Q-kEwTexgXGj_HlO16gmiCuGLvdrxzMjeQRTNENWwVSU4ZTRUvi7o1ZxkN_iBkN7wfnCHcR49xdlkPBpfDwh6QxRRrl3jlqhgS9HFSiuuTBcz0ByCRtqNZ-piB3YlHWz-TtxKoZxHNtaID-6M71VhUMPGScvBiqA0lQjqih00Gq4EKhKcAunzRdhLGQ4JEBICExBGLMO9LJYZi2I0bTNNfRsfWTn29-k35AjDcBK3AEa_gBMihTeZHDeZoOlWyR161cbW_iMm_3yDQZtCFp2p0EIfX5I-GiUXpSfkTPrHU_NxGEEfLLVar2nu02O0k58OzS4Wn6au0_5X-D5Ody-LZVnPn2_78c9WlZ3OHrsfpoM!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'beisbol invernal':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/vVNbT8IwGP0r44FEH5Z2o2Pb4-INRUMCKqwvpDehuLajq6D_3mI0PsFiCPalbb7Tc07b7wAMZgBrspEL4qTRpPL7EvfnKL-EtwhFw5vBNYRFfJ_kk_FofDFA4BlggJl2tVuCki55F0otmTRdSIlmJKiFbTxTFzpiV8KR5nfFrODSeWRtDX9jzviaCgNFGicsI5YHVMiGmiqQeiOstxOcVZIbdb7TrJnkoOyjGKZRLw4zSlGIBExDmjAYpjDLeIRYLPIITNsugX0Z7hkF9OfxF2QPw3CStABGP4ADIqU3me43mYLpRooteNLGKv8xkz--waBNIY-PVGihT05JH4_Sk9IjdCT93aH-2LWgD5pcrde48Gky2ol3B2b_Fqdaqaz3Eb6Os-3jy3Kh5g9XveR7qhadzieykykF/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'platinum':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tZNdb4IwFIb_il5wSVqgKFySfbG5xQS3Kb0xtRSog4JQdfv3Hpctu0KyGHrTnpy3z3nTnoMoWiGq2EFmTMtKsQLimE7WxL_Fj4RYs4fwHuPAfnb9RTSPbkKC3hFFlCtd6xzFmzwxsFSSy8rAG6Y4G9WiaYFkYM2ardCs_TvxRiRSg7JuqmTPdQW52hwdZAvXCnCg9uWZXnOZoNifJI5lW64pEj81icMtk6UCQ8i81MeejW0XLfvsUkjjjhVguE-_JR2E2cLtEcx_BReKxGBy2m1yipYHKY7oTVVNCV-w-OcbhH0VfPvKCj14d0i8PZ8OiifkSvzTpf44tyCMlNzudjSAuamUFp8arQYYnLosPefL_Ii842uaZ-X65c5xf7YiG49PbZqOlg!!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'black mujer':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tVNdb4IwFP0r-OAjacEy4JHsi80tJrpN6Yu5tEWqUrBU3f69ddmyJyWLsS_tzT0956S9B1E0Q1TBTi7AyFrB2tYZvZmT-A4_EeINH9MHjBP_JYgn49H4NiXoA1FEmTKNKVGWl7yPpZJM1n2cg2LgNEK3lqmPDeilMND-nZgWXBqLbHTNt8zUtte6TgWtEZqB5k6-BrZyqu1S6KNMwyRHmQARe14IbhRD4RIfQjcqAnB9zrzIw0U-iDmadvmmto1PrATb-_QbcoJhOAk6AKNfwBmRzJoMT5sM0XQnxR69q1pX9i8m_3yDtEsh9i9U6KAPrknvj8Kr0hNyIf3zufk4jqDNllxuNjSxAaqVEZ8Gza6ZoKaqosGXuxpH-7eiXFTz1_tB8LOtF73eAeIg9ag!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'siremas oro':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tVNbb4IwGP0r-OAjacEi8Eh2Y3MLCW5T-mJKqVAnLZaK27-3Llv2hGQx9qGXfKfnnLTfARgsARak4yXRXAqyNecMT1covIWPCDmzh_gewsh99sJ5mqQ3MQLvAANMhW50BbK8KsaQC065HMOcCEqshqnWMI2hJmrDNGn_dlSxgmuDbJQs9lRLU9vbVsdbYrVcsZq0llTyJNBQXoDMcdnUgfnaJqcJEeLZgZO7NoQBoiHLc8ehYDHkGJsy7BkRNPfxN6SHYTb3BgDJL-CMSGZM-v0mfbDoODuANyFVbX5h_s83iIcUQvdChQF675r0buJflR6hC-mfzvXHqQVNqvhmt8ORiY4Umn1qsLxOdpq6DiZf9kcaHF7XVVmvXu4m3s-yLUejI-t56Fk!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'la cadena':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tZNdb4IwFIb_Cl54SVqhFbgk-3JzC4luU3pjjm3ROiiIHW7_fnXZsiski6E37cl5-7wn7TmIoSViGhq1AaNKDbmNUzZekega3xMymt5NbjGOvUcazWfJ7GpC0CtiiHFtKrNF6XorhlhpxVU5xGvQHJxK1gdLGmID9U4aOPydeC2FMlZZ1aV456Y85VynUQdwcnA4CKnhhK-4EiglYhSCBHDDMPBdkvmeG0V07GKfg59RKnjmoUVXvcymccuKsb3PviUthOmcdgiSX8EZk9QWGbQXGaBFo-QRveiyLuwfzP_5BpMuh8i70KEDT_vEe0nQK56QC_EP5_rj1IJ2ptRuv2exHZxSG_lh0LKPyamKIvQ_3bdZeHzOtpti9XTj058t3wwGX0IaDcs!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'platinum mujer':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tVNdb8IgFP0r9cHHBqS0lcdmX93cYqLbtLwYStHihFaKuv17cdmyJ20WU17g5h7OOYF7AAVzQDXbyxWzstJs4-qMRgtMbuEjxoPRQ3oPYYKeQzKdjCc3KQbvgALKta1tCbK8LPpQasll1Yc505x5tTCNY-pDy8xaWNb8nbgRhbQOWZuq2HFbud7W9xRrrDCcmcKrN86H3ilP7dbCnJRqLguQBWQpch5HPonjwMcCcT8vlsIfBBFCIiQkGiAwa7NOXRueWQl09-k35AzDaBq2AMa_gAsimTMZnzcZg9leigN405VR7jum_3yDtE2BoCsVWujDLunROO6UHuMr6Z8uzcdpBF285Hq7pYnLUKWt-LRg3nGIaqWGwZf_MRkeXpflSi1e7oLwZ9user0j9HdKRQ!!/dz/d5/L2dBISEvZ0FBIS9nQSEh/'],
                'infinite':['https://www.bhdleon.com.do/wps/portal/BHD/Inicio/bancapersona/Productos/!ut/p/z1/tZNdT4MwFIb_CrvgkrRCkfaS-IVOQwLqRm-WjnbQOQqDyvTf2xmNV4yYhd60J-ft85605wAKloAq1suCaVkrtjNxRi9XiFzDe4Qu5nfRLYSh--iTNImTqwiBV0ABzZVudAmydcltKJXMZW3DNVM5sxrRdoZkQ83ardCs-zvlreBSG2XT1vw917XJtY7Vy45ZUm0MR4sjvcklBxn3XA4ZYo6HA99BGHoOI4Q43IUIC1cIQTBYjJVLTRoOrBCa-_RbMkCYp_6IIP4VnDDJTJHBcJEBWPRSHMCLqtvKfEH6zzeIxhyIe6bDCN6fEu_GwaR4hM7EP5zqj2MLmpGS2_2ehmZuaqXFhwbLCQanqSrsfTpvCT48b8qiWj3deP7Ptitmsy-IVfzf/dz/d5/L2dBISEvZ0FBIS9nQSEh/']
                }

        path = {'clasica local':['div','tab2','id'],
                'standard local':['div','tab2','id'],
                'clasica premia':['div','tab2','id'],
                'clasica internacional':['div','tab2','id'],
                'standard internacional':['div','tab2','id'],
                'mi pais':['div','tab2','id'],
                'gold internacional':['div','tab2','id'],
                'gold mujer':['div','tab2','id'],
                'gold premia':['div','tab2','id'],
                'mlb':['div','tab2','id'],
                'beisbol invernal':['div','tab2','id'],
                'platinum':['div','tab2','id'],
                'black mujer':['div','tab2','id'],
                'siremas oro':['div','tab2','id'],
                'la cadena':['div','tab2','id'],
                'platinum mujer':['div','tab2','id'],
                'infinite':['div','tab2','id']
                }

    if banco == 'Bancamerica':
        tree = ['section','beneficio','class']
        link = {'clasica':['http://bancamerica.com.do/banca_personal/visa_clsica_bancamrica'],
                'gold':['http://bancamerica.com.do/banca_personal/visa_gold_bancamrica'],
                'platinum':['http://bancamerica.com.do/banca_personal/visa_platinum_bancamrica'],
                'signature':['http://bancamerica.com.do/banca_personal/visa_signature_bancamrica']}

        path = {'clasica':['div','container'],
                'platinum':['div','container'],
                'gold':['div','container'],
                'signature':['div','container']
                }

    if banco == 'Vimenca':
        c = {'clasica local':'clasica-local',
             'clasica int':'clasica-internacional',
             'gold':'gold-internacional',
             'black gold':'black-gold-internacional',
             'platinum':'platinum-internacional',
             'gold pagatodo':'gold-pagatodo'}
        tree = ['div','yoo-zoo blog-uikit blog-uikit-tarjeta-de-credito-visa-'+c[tarjeta],'class']
        link = {'clasica int':['http://www.bancovimenca.com/portal/tarjetas/tarjeta-de-credito-visa-clasica-internacional'],
                'clasica local':['http://www.bancovimenca.com/portal/tarjetas/tarjeta-de-credito-visa-clasica-local'],
                'gold':['http://www.bancovimenca.com/portal/tarjetas/tarjeta-de-credito-visa-gold-internacional'],
                'black gold':['http://www.bancovimenca.com/portal/tarjetas/tarjeta-de-credito-visa-black-gold-internacional'],
                'platinum':['http://www.bancovimenca.com/portal/tarjetas/tarjeta-de-credito-visa-platinum-internacional']}

        path = {'clasica int':['article','uk-article'],
                'clasica local':['article','uk-article'],
                'gold':['article','uk-article'],
                'black gold':['article','uk-article'],
                'platinum':['article','uk-article']}

    return (link.get(tarjeta),path.get(tarjeta),tree)

def obtener_beneficios(urls,path,tree,otros=None):
    if not urls or len(urls) == 0:
        return ''
    final = ''
    for url in urls:
        # Realizamos la petición a la web
        #req = urllib.urlopen(url)
        opener = MyOpener()
        req = opener.open(url)
        x = req.read()
        resultado = []
        # Comprobamos que la petición nos devuelve un Status Code = 200
        statusCode = req.getcode()
        if statusCode == 200:

            # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            html = BeautifulSoup(x)
            #b = {}
            # Obtenemos todos los divs donde estan las entradas
            entradas = html.find_all(tree[0],{tree[2] : tree[1]})
            b = ''

            # Recorremos todas las entradas para extraer el título, autor y fecha
            for i,entrada in enumerate(entradas):
                #a = []
                a = ''
                # Con el método "getText()" no nos devuelve el HTML
                if len(path) == 3:
                    titulo = entrada.find_all(path[0], {path[2] : path[1]})
                else:
                    titulo = entrada.find_all(path[0], {tree[2] : path[1]})
                for e in titulo:
                    a = a+"%s"%e.getText()
                if otros:
                    datos = html.find_all(otros[0],{tree[2]: otros[1]})
                    for s in datos:
                        if len(s.getText().split())<6:
                            resultado.append(limpiar(s.getText()))
                    tarjeta = otros[2]
                # Sino llamamos al método "getText()" nos devuelve también el HTML
                #autor = entrada.find('span', {'class' : 'autor'})
                #fecha = entrada.find('span', {'class' : 'fecha'}).getText()
                if i == 0:
                    b = a

                # Imprimo el Título, Autor y Fecha de las entradas
               # print ("%d - %s  |  %s  |  %s" %(i+1,titulo,autor,fecha))
                while '' in resultado:
                    resultado.remove('')
                if otros:
                    b = mas_beneficios(b,a,resultado,i,tarjeta)
                #.encode('utf-8').replace("\xc1","A").replace("\xe1","a").replace("\xc9","E").replace("\xe9","e").replace("\xcd","I").replace("\xed","i").replace("\xd3","O").replace("\xf3","o").replace("\xda","U").replace("\xfa","u").replace("\xd1","N").replace("\xf1","n")
                #.replace('\n','').replace('\r','')

        else:
            return "Status Code %d : %s" %(statusCode,req.read())
        final += b
    if final:
        return final.replace('<!--','').replace('-->','').replace('<strong>','').replace('</strong','')
    else:
        return 'No se encuentran beneficios.'

def mas_beneficios(b,a,resultado,i,tarjeta):
    boolean = False
    if len(resultado)>0:
        for e in resultado[i-1].lower().split():
            if e in tarjeta:
                boolean += 1
            if boolean > len(resultado[i-1].lower().split())-2:
                return a+b
        return b
    else:
        return b+a
