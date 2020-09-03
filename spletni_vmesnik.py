from datetime import date
import bottle
import os
import random
import hashlib
from model import Igralec, Podatki

#pot do imenika, iz katerega beremo igralce
imenik_s_podatki = 'igralci'
igralci={}
skrivnost = 'TO JE ENA HUDA SKRIVNOST'


if not os.path.isdir(imenik_s_podatki):
    os.mkdir(imenik_s_podatki)

for ime_datoteke in os.listdir(imenik_s_podatki):
    igralec = Igralec.nalozi_stanje(os.path.join(imenik_s_podatki, ime_datoteke))
    igralci[igralec.uporabnisko_ime] = igralec

def trenutni_igralec():
    uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime', secret=skrivnost)
    if uporabnisko_ime is None:
        bottle.redirect('/prijava/')
    return igralci[uporabnisko_ime]

def shrani_trenutnega_igralca():
    igralec = trenutni_igralec()
    igralec.shrani_stanje(os.path.join('igralci', f'{igralec.uporabnisko_ime}.json'))

@bottle.get('/')
def zacetna_stran():
    bottle.redirect('/podatki/')

@bottle.get('/podatki/')
def nacrtovanje_podatkov():
    podatki = podatki_igralca()
    return bottle.template('podatki.html', podatki=podatki)

def podatki_igralca():
    return trenutni_igralec().podatki

@bottle.get('/prijava/')
def prijava_get():
    return bottle.template('prijava.html')

@bottle.post('/prijava/')
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    geslo = bottle.request.forms.getunicode('geslo')
    
    if 'nov_racun' in bottle.request.forms and uporabnisko_ime not in igralci:
        igralec = Igralec(
            uporabnisko_ime,
            geslo,
            Podatki()
        )
        igralci[uporabnisko_ime] = igralec
    else:
        igralec = igralci[uporabnisko_ime]
        igralec.preveri_geslo(geslo)
    
    bottle.response.set_cookie('uporabnisko_ime', igralec.uporabnisko_ime, path='/', secret=skrivnost)
    bottle.redirect('/')

@bottle.post('/odjava/')
def odjava():
    bottle.response.delete_cookie('uporabnisko_ime', path='/')
    bottle.redirect('/')

@bottle.post('/ustvari_igro')
def ustvari_igro():
    podatki = podatki_igralca()
    operacija = bottle.request.forms.getunicode('operacija')
    ime_igre = bottle.request.forms.getunicode('ime_igre')
    nova_igra = podatki.nova_igra(operacija, ime_igre)
    shrani_trenutnega_igralca()
    return bottle.template('igra.html', igra=nova_igra)

@bottle.post('/preveri')
def preveri_igro():
    i = 1
    while i <= 5:

        s1 = bottle.request.forms.getunicode('st1-' + str(i))
        s2 = bottle.request.forms.getunicode('st2-' + str(i))
        op = bottle.request.forms.getunicode('op-' + str(i))
        vasVnos = bottle.request.forms.getunicode('vasVnos-' + str(i))
        resitev = bottle.request.forms.getunicode('rezultat-' + str(i))
        if vasVnos != resitev:
            podatki = podatki_igralca()
            podatki.nov_napacenPrimer(s1,s2,op,resitev,vasVnos)
            shrani_trenutnega_igralca()
        i += 1

    bottle.redirect('/')


bottle.run(debug=True, reloader=True)