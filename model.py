import json
import random

class Igralec:
    def __init__(self, uporabnisko_ime, geslo, podatki):
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo
        self.podatki = podatki

    def preveri_geslo(self, geslo):
        if self.geslo != geslo:
            raise ValueError('Geslo ni pravilno! Poskusite z drugim geslo.')

    def shrani_stanje(self, ime_datoteke):
        slovar_stanja = {
            'uporabnisko_ime': self.uporabnisko_ime,
            'geslo': self.geslo,
            'podatki': self.podatki.slovar_s_stanjem(),
        }
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(slovar_stanja, datoteka, ensure_ascii=False, indent=4)


    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_stanja = json.load(datoteka)
        uporabnisko_ime = slovar_stanja['uporabnisko_ime']
        geslo = slovar_stanja['geslo']
        podatki = Podatki.nalozi_iz_slovarja(slovar_stanja['podatki'])
        return cls(uporabnisko_ime,geslo, podatki)
        

class Podatki:
    def __init__(self):
        self.igre = []
        self.napacniPrimeri = []

    def nova_igra_nalozi(self, operacija, ime_igre):
        self.operacija = operacija
        self.ime_igre = ime_igre

    def nova_igra(self, operacija, ime_igre):
        self.operacija = operacija
        self.ime_igre = ime_igre
        self.primeri = Podatki._ustvari_primere(self,operacija)

    def nova_igra_rez(self, stopnja, operacija, primeri):
        self.stopnja = stopnja,
        self.operacija = operacija,
        self.primeri = primeri
  

    def slovar_s_stanjem(self):
        return {
            'igre': [{
                'ime_igre': igra.ime_igre,            
                'operacija': igra.operacija,
                'primeri': [{
                    "stevilo1": primer.stevilka1,
                    "stevilo2": primer.stevilka2,
                    "resitev": primer.resitev,
                    "operacija": primer.operacija
                }for primer in igra.primeri]
            }
        }

    @classmethod
    def nalozi_iz_slovarja(cls, slovar_s_stanjem):
        podatki = cls()
        for igra in slovar_s_stanjem['igre']:
            nova_igra = podatki.nova_igra_nalozi(
            igra['operacija'],
            igra['ime_igre']
            )
        return podatki

    def _ustvari_primere(self, operacija):
        primeri = []
        i = 1
        while i <= 5:
            primer = Podatki._nov_primer(self,operacija)                        
            primeri.append(primer)
            i += 1
        return primeri


    def _nov_primer(self, operacija):
        if operacija == 'ses':
            st1 = random.randrange(1,50)
            st2 = random.randrange(1,50)
            rez = st1 + st2
            return Primer(st1, st2, operacija, rez)
        elif operacija == 'ods': 
            st1 = random.randrange(20,100)
            st2 = random.randrange(1,20)
            rez = st1 - st2
            return Primer(st1, st2, operacija, rez)
            
        elif operacija == 'mnoz':
            st1 = random.randrange(1,10)
            st2 = random.randrange(1,10) 
            rez = st1 * st2
            return Primer(st1, st2, operacija, rez)
             
        else:
            st1 = random.randrange(1,100)
            st2 = random.randrange(1,10)
            rez = st1//st2
            return Primer(st1, st2, operacija, rez)
  
    def shrani_stanje(self, ime_datoteke):
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(self.slovar_s_stanjem(), datoteka, ensure_ascii=False, indent=4)
    
    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_s_stanjem = json.load(datoteka)
        return cls.nalozi_iz_slovarja(slovar_s_stanjem)


class Igra:
    def __init__(self, ime_igre, operacija, primeri):
            self.ime_igre = ime_igre
            self.operacija = operacija
            self.primeri = primeri
   
class Primer:
    def __init__(self, stevilka1,stevilka2,operacija, resitev):
        self.stevilka1 = stevilka1,
        self.stevilka2 = stevilka2,
        self.operacija = operacija,
        self.resitev = resitev


