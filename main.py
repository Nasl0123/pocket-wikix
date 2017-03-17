#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
import jinja2
import os
from google.appengine.ext import db
from google.appengine.api import memcache
import re
import hashlib
import urllib2
import time
from generadorPopular import obtener_tarjeta_popular,formatear_popular,generar_popular,generar_info_popular
from generadorProgreso import obtener_tarjeta_progreso,formatear_progreso,generar_progreso
from generadorLopezDeHaro import obtener_tarjeta_lopezdeharo,formatear_lopezdeharo,generar_lopezdeharo,generar_info_lopezdeharo
from generadorACAP import obtener_tarjeta_acap,formatear_acap,generar_acap
from generadorALNAP import obtener_tarjeta_alnap,formatear_alnap,generar_alnap
from generadorBDI import obtener_tarjeta_bdi,formatear_bdi,generar_bdi
from generadorAdemi import obtener_tarjeta_ademi,formatear_ademi,generar_ademi
from generadorScotiabank import obtener_tarjeta_scotiabank, formatear_scotiabank, generar_scotiabank
from generadorBanReservas import obtener_tarjeta_banreservas, formatear_banreservas, generar_banreservas
from generadorBANACI import obtener_tarjeta_banaci, formatear_banaci, generar_banaci, beneficios_banaci
from generadorSantaCruz import obtener_tarjeta_santacruz, formatear_santacruz, generar_santacruz
from scraper import obtener_beneficios,datos_tarjeta
from indices import get_indices,formato_general,limpiar
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(100)

jinja_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(jinja_dir))

class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.write(*a,**kw)
    def render_str(self,template,**params):
        y = jinja_env.get_template(template)
        return y.render(params)
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class Signup(Handler):
    def get(self):
        user = self.request.cookies.get('user_id')
        if not user:
            self.render('signup.html',url='Signup',link='/')
        else:
            self.write("<a href='/'>Already registered</a>")
    def post(self):
        username = valid_username(self.request.get('username'))
        password = valid_pass(self.request.get('password'))
        verify = self.request.get('verify')==self.request.get('password')
        email = valid_email(self.request.get('email'))
        erroruser,errormail,errorpass,errorverify='','','',''
        user_query = get_cache('Users',db.GqlQuery('select * from User'))
        user_list = []
        user_ob = None
        if user_query:
            for e in user_query:
                user_list.append(e.username)
                if e.username == username[1]:
                    user_ob = e
        if not(username[0] and password[0] and verify and email[0] and not user_ob):
            if not username[0]:
                erroruser = 'Invalid username'
            if user_ob:
                erroruser = 'Username already exists'
            if not password[0]:
                errorpass = 'Invalid password'
            if not verify:
                errorverify = "Passwords don't match"
            if not email[0]:
                errormail = 'Invalid e-mail'
            self.render('signup.html',username=username[1],email=email[1],erroruser=erroruser,errormail=errormail,errorpass=errorpass,errorverify=errorverify)
        else:
            user_ob = User(username=username[1],password=hashlib.sha256(username[1]+password[1]).hexdigest(),email=hashlib.sha256(email[1]).hexdigest())
            user_ob.put()
            self.response.headers.add_header('Set-Cookie','user_id='+str(user_ob.username)+'|'+str(user_ob.password)+';Path=/')
            self.redirect('/')

class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty(required=False)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    if USER_RE.match(username):
        return (True,username)
    else:
        return (False,username)

PASS_RE = re.compile(r"^[a-zA-Z0-9]{3,20}$")
def valid_pass(password):
    if PASS_RE.match(password):
        return (True,password)
    return (False,password)
def valid_email(email):
    if not email:
        return (True,'')
    if email[-4:] == '.com' and email.find('@')>-1:
        if len(email) > 4:
            return (True,email)
    return (False,email)

def escape_html(s):
        s = s.replace('&','&amp;')
        s = s.replace('<','&lt;')
        s = s.replace('>','&gt;')
        s = s.replace('"','&quot;')
        return s
def escape_script(s):
    if s.find('<script>') > -1:
        if s.find('</script>') > -1:
            script = s[s.find('<script>'):s.find('</script>')+9]
        else:
            script = s[s.find('<script>'):]
        script = escape_html(script)
        s = s[:s.find('<script>')]+script+s[s.find('</script>')+9:]
    return s 

class Login(Handler):
    def get(self):
        user = self.request.cookies.get('user_id')
        if not user:
            self.render('login.html',url='Login',link='/')
        else:
            self.write("<a href='/'>Already logged</a>")
    def post(self):
        username = valid_username(self.request.get('username'))
        password = valid_pass(self.request.get('password'))
        erroruser,errorpass='',''
        user_query = get_cache('Users',db.GqlQuery('select * from User'))
        user_list = []
        user_ob = None
        if user_query:
            for e in user_query:
                user_list.append(e.username)
                if e.username == username[1]:
                    user_ob = e
        if not(username[0] and password[0] and user_ob and user_ob.password == hashlib.sha256(username[1]+password[1]).hexdigest()):
            if not username[0]:
                erroruser = 'Invalid username'
            if not user_ob:
                erroruser = "Username don't exists"
            if not password[0]:
                errorpass = 'Invalid password'
            if user_ob and user_ob.password != hashlib.sha256(password[1]).hexdigest():
                errorpass = 'Invalid password'
            self.render('login.html',username=username[1],erroruser=erroruser,errorpass=errorpass)
        else:
            user_ob = User(username=username[1],password=hashlib.sha256(username[1]+password[1]).hexdigest())
            self.response.headers.add_header('Set-Cookie','user_id='+str(user_ob.username)+'|'+str(user_ob.username+user_ob.password)+';Path=/')
            self.redirect('/')

class Logout(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie','user_id=;Path=/')
        self.redirect('/')

class WikiPage(Handler):
    def get(self,link):
        page_list = get_cache(link,db.GqlQuery("select * from Page where url='"+link+"'"))
        page_list = list(page_list)
        url_ob = None
        version = self.request.get('v')
        if version:
            version = int(version)
        if len(page_list) > 0:
            url_ob = page_list[0]
        if url_ob:
            if not version:
                version = -1
            if type(version) == int and version < len(url_ob.version):
                if link == '/':
                    url = 'Main'
                else:
                    url = link[1:]
                user_base = self.request.cookies.get('user_id')
                if user_base:
                    user_base = user_base.split('|')[0]
                else:
                    user_base = ''
                banco = get_indices(link)[0]
                tarjeta = get_indices(link)[1]
                self.render('children.html',page=url_ob.page[version],url=url,page_url=all_url()[0],user_base=user_base,link=link,credito=tarjeta,banco=banco,url_full=self.request.url)
            else:
                self.redirect('/_edit'+link+'?v='+str(len(url_ob.version)-1))               
        else:
            self.redirect('/_edit'+link)

class EditPage(Handler):
    def get(self,link):
        user = self.request.cookies.get('user_id')
        if (user and (user.split('|')[0] == 'Nasl' or user.split('|')[0] == 'Jorge')) or self.request.get('token') == '1597532468':
            page_list = get_cache(link,db.GqlQuery("select * from Page where url='"+link+"'"))
            page_list = list(page_list)
            page_ob = ''
            version = self.request.get('v')
            if version:
                version = int(version)
            if len(page_list) > 0:
                page_ob = page_list[0]
                if type(version) != int:
                    version = len(page_ob.version)-1
                if version > len(page_ob.version)-1:
                    version = page_ob.version[-1]
                    self.redirect('/_edit'+link+'?v='+str(version))
            if link == '/':
                url = 'Main'
            else:
                url = link[1:]
            user_base = self.request.cookies.get('user_id')
            if user_base:
                user_base = user_base.split('|')[0]
            else:
                user_base = ''
            self.render('page.html',page=page_ob,version=version,name='Edit',url=url,page_url=all_url()[0],user_base=user_base,link=link)

    def post(self,link):
        user = self.request.cookies.get('user_id')
        if (user and (user.split('|')[0] == 'Nasl' or user.split('|')[0] == 'Jorge')) or self.request.get('token') == '1597532468':
            page = self.request.get('content')
            page = escape_script(page)
            page_ob = None
            page_list = get_cache(link,db.GqlQuery("select * from Page where url='"+link+"'"))
            page_list = list(page_list)
            if len(page_list) > 0:
                page_ob = page_list[0]
            if page_ob:
                new_ob = Page(url='new',page=[db.Text('new')],version=[0],created_list=['new'])
                page_ob.created = new_ob.created
                page_ob.version = page_ob.version + [page_ob.version[-1]+1]
                page_ob.page = page_ob.page + [db.Text(page)]
                page_ob.created_list = page_ob.created_list + [str(page_ob.created)]
            else:
                page_ob = Page(url=link,page=[db.Text(page)],version=[0])
                page_ob.created_list = [str(page_ob.created)]
            page_ob.put()
            get_cache(link,db.GqlQuery("select * from Page where url='"+link+"'"),actualizar=True)
            memcache.delete('Pages')
            self.redirect('http://rexi-verification.appspot.com'+link+'?update=1')
           # time.sleep(2)

class HistoryPage(Handler):
    def get(self,link):
        page_ob = None
        page_list = get_cache(link,db.GqlQuery("select * from Page where url='"+link+"'"))
        page_list = list(page_list)
        if len(page_list) > 0:
            page_ob = page_list[0]
        if page_ob:
            if link == '/':
                url = 'Main'
            else:
                url = link[1:]
            escaped_list = []
            for e in page_ob.page:
                escaped_list.append(escape_html(e))
            user_base = self.request.cookies.get('user_id')
            if user_base:
                user_base = user_base.split('|')[0]
            else:
                user_base = ''
            self.render('history.html',page_list=escaped_list,link=link,url=url,version=list(reversed(page_ob.version)),created=list(reversed(page_ob.created_list)),name='History',page_url=all_url()[0],user_base=user_base)
        else:
            self.redirect('/_edit'+link)

class Redirect(Handler):
    def get(self):
        link = self.request.get('text')
        if link:
            self.redirect('/'+link)
        else:
            self.redirect('/')

class Page(db.Model):
    url = db.StringProperty(required=True)
    page = db.ListProperty(db.Text,required=True)
    version = db.ListProperty(int,required=True)
    created = db.DateProperty(auto_now_add=True)
    created_list = db.ListProperty(str,required=True)

def get_cache(name,query,actualizar=False):
    cache = query
    #cache = memcache.get(str(name))
    if actualizar == True:
        memcache.add(str(name),query)
        cache = query
    if not cache:
        memcache.add(str(name),query)
        cache = query
    return cache

def all_url(actualizar=False):
    page_list = get_cache('Pages',list(db.GqlQuery("select * from Page order by url asc")),actualizar=actualizar)
    page_dict = {}
    for e in page_list:
        page_dict[str(e.url)] = ''
    return (page_list,None)

class GeneradorPopular(Handler):
    def get(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        self.render('generador.html',user_base=user_base,url='Generador Popular')
    def post(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        banco = self.request.get('banco')
        tarjeta = self.request.get('tarjeta')
        datos = get_cache(banco+tarjeta+'_datos',datos_tarjeta('Popular',self.request.get('tarjeta')))
        contenido=get_cache(banco+tarjeta+'_contenido',obtener_tarjeta_popular(self.request.get('tarjeta'),generar_info_popular(generar_popular('Popular'))))
        beneficios=get_cache(banco+tarjeta+'_beneficios',obtener_beneficios(datos[0],datos[1],datos[2]))
        content = formato_general(self.request.get('title'),contenido,beneficios)
        self.render('generador.html',beneficios=beneficios,cont=contenido,contenido=content,user_base=user_base,url='Generador Popular',link=self.request.get('link'))

class GeneradorLopezDeHaro(Handler):
    def get(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        self.render('generador.html',user_base=user_base,url='Generador LopezDeHaro')
    def post(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        banco = self.request.get('banco')
        tarjeta = self.request.get('tarjeta')
        datos = get_cache(banco+tarjeta+'_datos',datos_tarjeta('LopezDeHaro',self.request.get('tarjeta')))#CONTINUAR AQUI
        contenido=get_cache(banco+tarjeta+'_contenido',obtener_tarjeta_lopezdeharo(self.request.get('tarjeta'),generar_info_lopezdeharo(generar_lopezdeharo('LopezDeHaro'))))
        beneficios=get_cache(banco+tarjeta+'_beneficios',obtener_beneficios(datos[0],datos[1],datos[2],['div','subtitulo',get_indices(self.request.get('link'))[1]]))
        content = formato_general(self.request.get('title'),contenido,beneficios)
        self.render('generador.html',beneficios=beneficios,cont=contenido,contenido=content,user_base=user_base,url='Generador LopezDeHaro',link=self.request.get('link'))

class GeneradorProgreso(Handler):
    def get(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        self.render('generador.html',user_base=user_base,url='Generador Progreso')
    def post(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        banco = self.request.get('banco')
        tarjeta = self.request.get('tarjeta')
        datos = get_cache(banco+tarjeta+'_datos',datos_tarjeta('Progreso',self.request.get('tarjeta')))
        contenido=get_cache(banco+tarjeta+'_contenido',obtener_tarjeta_progreso(self.request.get('tarjeta'),generar_progreso('Progreso')))
        beneficios=get_cache(banco+tarjeta+'_beneficios',obtener_beneficios(datos[0],datos[1],datos[2]))
        content = formato_general(self.request.get('title'),contenido,beneficios)
        self.render('generador.html',beneficios=beneficios,cont=contenido,contenido=content,user_base=user_base,url='Generador Progreso',link=self.request.get('link'))

class GeneradorACAP(Handler):
    def get(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        self.render('generador.html',user_base=user_base,url='Generador ACAP')
    def post(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        banco = self.request.get('banco')
        tarjeta = self.request.get('tarjeta')
        datos = get_cache(banco+tarjeta+'_datos',datos_tarjeta('ACAP',self.request.get('tarjeta')))
        contenido=get_cache(banco+tarjeta+'_contenido',obtener_tarjeta_acap(self.request.get('tarjeta'),generar_acap('ACAP')))
        beneficios=get_cache(banco+tarjeta+'_beneficios',obtener_beneficios(datos[0],datos[1],datos[2]))
        content = formato_general(self.request.get('title'),contenido,beneficios)
        self.render('generador.html',beneficios=beneficios,cont=contenido,contenido=content,user_base=user_base,url='Generador ACAP',link=self.request.get('link'))

class GeneradorALNAP(Handler):
    def get(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        self.render('generador.html',user_base=user_base,url='Generador ALNAP')
    def post(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        banco = self.request.get('banco')
        tarjeta = self.request.get('tarjeta')
        datos = get_cache(banco+tarjeta+'_datos',datos_tarjeta('ALNAP',self.request.get('tarjeta')))
        contenido=get_cache(banco+tarjeta+'_contenido',obtener_tarjeta_alnap(self.request.get('tarjeta'),generar_alnap('ALNAP')))
        beneficios=get_cache(banco+tarjeta+'_beneficios',obtener_beneficios(datos[0],datos[1],datos[2]))
        content = formato_general(self.request.get('title'),contenido,beneficios)
        self.render('generador.html',beneficios=beneficios,cont=contenido,contenido=content,user_base=user_base,url='Generador ALNAP',link=self.request.get('link'))

class GeneradorBDI(Handler):
    def get(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        self.render('generador.html',user_base=user_base,url='Generador BDI')
    def post(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        banco = self.request.get('banco')
        tarjeta = self.request.get('tarjeta')
        datos = get_cache(banco+tarjeta+'_datos',datos_tarjeta('BDI',self.request.get('tarjeta')))
        contenido=get_cache(banco+tarjeta+'_contenido',obtener_tarjeta_bdi(self.request.get('tarjeta'),generar_bdi('BDI')))
        beneficios=get_cache(banco+tarjeta+'_beneficios',obtener_beneficios(datos[0],datos[1],datos[2]))
        content = formato_general(self.request.get('title'),contenido,beneficios)
        self.render('generador.html',beneficios=beneficios,cont=contenido,contenido=content,user_base=user_base,url='Generador BDI',link=self.request.get('link'))


class GeneradorAdemi(Handler):
    def get(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        self.render('generador.html',user_base=user_base,url='Generador Ademi')
    def post(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        banco = self.request.get('banco')
        tarjeta = self.request.get('tarjeta')
        datos = get_cache(banco+tarjeta+'_datos',datos_tarjeta('Ademi',self.request.get('tarjeta')))
        contenido=get_cache(banco+tarjeta+'_contenido',obtener_tarjeta_ademi(self.request.get('tarjeta'),generar_ademi('Ademi')))
        beneficios=get_cache(banco+tarjeta+'_beneficios',obtener_beneficios(datos[0],datos[1],datos[2]))
        content = formato_general(self.request.get('title'),contenido,beneficios)
        self.render('generador.html',beneficios=beneficios,cont=contenido,contenido=content,user_base=user_base,url='Generador Ademi',link=self.request.get('link'))

class GeneradorScotiabank(Handler):
    def get(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        self.render('generador.html',user_base=user_base,url='Generador Scotiabank')
    def post(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        banco = self.request.get('banco')
        tarjeta = self.request.get('tarjeta')
        datos = get_cache(banco+tarjeta+'_datos',datos_tarjeta('Scotiabank',self.request.get('tarjeta')))
        contenido=get_cache(banco+tarjeta+'_contenido',obtener_tarjeta_scotiabank(self.request.get('tarjeta'),generar_scotiabank('Scotiabank')))
        beneficios=get_cache(banco+tarjeta+'_beneficios',obtener_beneficios(datos[0],datos[1],datos[2]))
        content = formato_general(self.request.get('title'),contenido,beneficios)
        self.render('generador.html',beneficios=beneficios,cont=contenido,contenido=content,user_base=user_base,url='Generador Scotiabank',link=self.request.get('link'))

class GeneradorBanReservas(Handler):
    def get(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        self.render('generador.html',user_base=user_base,url='Generador BanReservas')
    def post(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        banco = self.request.get('banco')
        tarjeta = self.request.get('tarjeta')
        datos = get_cache(banco+tarjeta+'_datos',datos_tarjeta('BanReservas',self.request.get('tarjeta')))
        contenido=get_cache(banco+tarjeta+'_contenido',obtener_tarjeta_banreservas(self.request.get('tarjeta'),generar_banreservas('BanReservas')))
        beneficios=get_cache(banco+tarjeta+'_beneficios',obtener_beneficios(datos[0],datos[1],datos[2]))
        content = formato_general(self.request.get('title'),contenido,beneficios)
        self.render('generador.html',beneficios=beneficios,cont=contenido,contenido=content,user_base=user_base,url='Generador BanReservas',link=self.request.get('link'))

class GeneradorBANACI(Handler):
    def get(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        self.render('generador.html',user_base=user_base,url='Generador BANACI')
    def post(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        banco = self.request.get('banco')
        tarjeta = self.request.get('tarjeta')
        datos = get_cache(banco+tarjeta+'_datos',datos_tarjeta('BANACI',self.request.get('tarjeta')))
        contenido=get_cache(banco+tarjeta+'_contenido',obtener_tarjeta_banaci(self.request.get('tarjeta'),generar_banaci('BANACI')))
        beneficios=get_cache(banco+tarjeta+'_beneficios',beneficios_banaci())
        content = formato_general(self.request.get('title'),contenido,beneficios)
        self.render('generador.html',beneficios=beneficios,cont=contenido,contenido=content,user_base=user_base,url='Generador BANACI',link=self.request.get('link'))

class GeneradorSantaCruz(Handler):
    def get(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        self.render('generador.html',user_base=user_base,url='Generador SantaCruz')
    def post(self):
        user_base = self.request.cookies.get('user_id')
        if user_base:
            user_base = user_base.split('|')[0]
        else:
            user_base = ''
        banco = self.request.get('banco')
        tarjeta = self.request.get('tarjeta')
        datos = get_cache(banco+tarjeta+'_datos',datos_tarjeta('SantaCruz',self.request.get('tarjeta')))
        contenido=get_cache(banco+tarjeta+'_contenido',obtener_tarjeta_santacruz(self.request.get('tarjeta'),generar_santacruz('SantaCruz')))
        beneficios=get_cache(banco+tarjeta+'_beneficios',obtener_beneficios(datos[0],datos[1],datos[2]))
        content = formato_general(self.request.get('title'),contenido,beneficios)
        self.render('generador.html',beneficios=beneficios,cont=contenido,contenido=content,user_base=user_base,url='Generador SantaCruz',link=self.request.get('link'))


class FlushCache(Handler):
    def get(self):
        tarjeta = self.request.get('tarjeta')
        banco = self.request.get('banco')
        memcache.delete(banco+tarjeta+'_datos')
        memcache.delete(banco+tarjeta+'_contenido')
        memcache.delete(banco+tarjeta+'_beneficios')
        self.redirect(str(self.request.get('link')))
    def post(self):
        tarjeta = self.request.get('tarjeta')
        banco = self.request.get('banco')
        memcache.delete(banco+tarjeta+'_datos')
        memcache.delete(banco+tarjeta+'_contenido')
        memcache.delete(banco+tarjeta+'_beneficios')
        self.redirect(self.request.get('link'))

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/login', Login),
                               ('/logout', Logout),
                               ('/redirect', Redirect),
                               ('/_edit' + PAGE_RE, EditPage),
                               ('/_history' + PAGE_RE, HistoryPage),
                               #('/signup', Signup),
                               ('/generadorpopular', GeneradorPopular),
                               ('/generadorlopezdeharo', GeneradorLopezDeHaro),
                               ('/flush-cache', FlushCache),
                               ('/generadorprogreso', GeneradorProgreso),
                               ('/generadoracap', GeneradorACAP),
                               ('/generadoralnap', GeneradorALNAP),
                               ('/generadorbdi', GeneradorBDI),
                               ('/generadorademi',GeneradorAdemi),
                               ('/generadorscotiabank',GeneradorScotiabank),
                               ('/generadorbanreservas',GeneradorBanReservas),
                               ('/generadorbanaci',GeneradorBANACI),
                               ('/generadorsantacruz',GeneradorSantaCruz),
                               (PAGE_RE, WikiPage),
                               ],
                              debug=True)
