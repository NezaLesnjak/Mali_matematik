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
        self.pravilniPrimeri = []

    def nova_igra_nalozi(self, operacija, ime_igre, primeri):
        self.igre.append(Igra(ime_igre, operacija, primeri))

    def append_igra(self, igra):
        self.igre.append(igra)

    def nova_igra(self, operacija, ime_igre):
        nigra = Igra(ime_igre, operacija,Podatki._ustvari_primere(self,operacija))
        self.igre.append(nigra)
        return nigra  

    def nova_igra_rez(self, stopnja, operacija, primeri):
        self.stopnja = stopnja,
        self.operacija = operacija,
        self.primeri = primeri

    def nov_napacenPrimer_nalozi(self, stevilka1, stevilka2, operacija, resitev, vasVnos):
        self.napacniPrimeri.append(NapacniPrimer(stevilka1, stevilka2, operacija, resitev, vasVnos))

    def nov_napacenPrimer(self, stevilka1, stevilka2, operacija, resitev, vasVnos):
        self.napacniPrimeri.append(NapacniPrimer(stevilka1, stevilka2, operacija, resitev, vasVnos))
        return NapacniPrimer(stevilka1, stevilka2, operacija, resitev, vasVnos)

    def nov_pravilenPrimer(self, stevilka1, stevilka2, operacija, resitev):
        self.pravilniPrimeri.append(Primer(stevilka1, stevilka2, operacija, resitev))
        return Primer(stevilka1, stevilka2, operacija, resitev)

    def slovar_s_stanjem(self):
        return {
            'igre': [{
                'ime_igre': igra.ime_igre,            
                'operacija': igra.operacija,
                'primeri': [{
                    "stevilka1": primer.stevilka1,
                    "stevilka2": primer.stevilka2,
                    "resitev": primer.resitev,
                    "operacija": primer.operacija
                }for primer in igra.primeri]
            }for igra in self.igre],
            'napacniPrimeri': [{
                "stevilka1": napacniPrimer.stevilka1,
                "stevilka2": napacniPrimer.stevilka2,
                "operacija": napacniPrimer.operacija,
                "resitev": napacniPrimer.resitev,
                "vasVnos": napacniPrimer.vasVnos
            } for napacniPrimer in self.napacniPrimeri]            
        }

    @classmethod
    def nalozi_iz_slovarja(cls, slovar_s_stanjem):
        podatki = cls()
        for igra in slovar_s_stanjem['igre']:
            primeri = []
            for primer in igra['primeri']:
                nov_primer = Primer(primer['stevilka1'], 
                primer['stevilka2'], 
                primer['operacija'], 
                primer['resitev'])
                primeri.append(nov_primer)
            podatki.nova_igra_nalozi(
            igra['operacija'],
            igra['ime_igre'],
            primeri)
        for napacniPrimer in slovar_s_stanjem['napacniPrimeri']:
            podatki.nov_napacenPrimer_nalozi(napacniPrimer['stevilka1'],
            napacniPrimer['stevilka2'],
            napacniPrimer['operacija'],
            napacniPrimer['resitev'],
            napacniPrimer['vasVnos'])            
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
    def __init__(self, stevilka1, stevilka2, operacija, resitev):
        self.stevilka1 = stevilka1
        self.stevilka2 = stevilka2
        self.operacija = operacija
        self.resitev = resitev

class NapacniPrimer:
    def __init__(self, stevilka1, stevilka2, operacija, resitev, vasVnos):
        self.stevilka1 = stevilka1
        self.stevilka2 = stevilka2
        self.operacija = operacija
        self.resitev = resitev
        self.vasVnos = vasVnos  