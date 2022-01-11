import pygame
import grafica
import random
from constante import *

class Buton:
    """
        Clasa pentru implementarea unui buton
    """

    def __init__(self, text, stanga_sus, latime, inaltime):

        self.text = text
        self.stanga_sus = stanga_sus
        self.latime = latime
        self.inaltime = inaltime
        self.buton_grafic = grafica.ButonGrafic(self.text, self.stanga_sus, self.latime, self.inaltime)

    def afiseaza(self, fereastra):
        self.buton_grafic.afiseaza(fereastra)

    def verifica_mouse(self, xy):
        if xy[0] > self.stanga_sus[0] and xy[0] < self.stanga_sus[0] + self.latime\
           and xy[1] > self.stanga_sus[1] and xy[1] < self.stanga_sus[1] + self.inaltime:
            return True
        return False


class Meniu:
    """
        Clasa care implementeaza meniul
    """
    def __init__(self, fereastra):
        """
            Constructor
        :param fereastra:
        """
        self.fereastra = fereastra
        # un dreptunghi alb pe post de meniu in partea din stanga a ferestrei
        self.dreptunghi = grafica.Dreptunghi(fereastra, ( int(SPATIU), int(SPATIU) ),
                                             int(MENIU), int(INALTIME_FEREASTRA - 2 * SPATIU),ALB )

        # eticheta cu ce jucator este la mutare
        x = int(SPATIU + 2 * ZOOM)
        y = int(SPATIU + 1 * ZOOM)
        self.rand = grafica.Text("", (x, y), int(11 * ZOOM/2), NEGRU, False, False)

        # eticheta cu numarul de mutari
        y = int(y + 12 * ZOOM)
        self.mutari = grafica.Text("", (x, y), int(11 * ZOOM/2), NEGRU, False, False)

        # buton pentru terminarea jocului si iesirea din aplicatie
        latime = int(20 * ZOOM)
        x = int(SPATIU + MENIU / 2 - latime / 2)
        y = int(INALTIME_FEREASTRA - SPATIU - (2 + 10) * ZOOM)
        self.btn_inchide = Buton("Ieșire", (x, y), latime, int(10 * ZOOM) )

        # buton pentru schimbarea jucatorului atunci cand nu mai sunt posibile mutari si nu sunt epuizate toate
        # mutarile date de zaruri
        latime = int(50 * ZOOM)
        x = int(SPATIU + MENIU / 2 - latime / 2)
        y = int(INALTIME_FEREASTRA - SPATIU - (2 + 10 + 10 + 10) * ZOOM)
        self.btn_schimba_randul = Buton("Schimbă jucătorul", (x, y), latime, int(10 * ZOOM))

    def afiseaza(self, fereastra):
        """
            Afiseaza meniul in fereastra
        :param fereastra:
        :return:
        """
        self.dreptunghi.afiseaza(fereastra)
        self.rand.afiseaza(fereastra)
        self.mutari.afiseaza(fereastra)
        self.btn_inchide.afiseaza(fereastra)
        self.btn_schimba_randul.afiseaza(fereastra)

    def setRand(self,text):
        """
            Seteaza textul etichetei pentru cine este la mutare
        :param text:
        :return:
        """
        self.rand.set_text(text)

    def setMutari(self,text):
        """
            Seteaza textul etichetei cu numarul de mutari ramase
        :param text:
        :return:
        """
        self.mutari.set_text(text)


class Zaruri:
    """
        Clasa care stocheaza zarurile pentru joc, le deseneaza si genereaza noi numere la schimbarea randului
        jucatorilor
    """

    def __init__(self, tabla, fereastra):
        """
            Constructor
        :param tabla:
        :param fereastra:
        """
        self.tabla = tabla

        # Initializarea cu niste valori pentru zaruri, folosite doar la prima instantiere
        self.zar1_numar = 6
        self.zar2_numar = 3

        # se calculeaza coordonatele punctului din stanga sus pentru zaruri in vederea desenarii lor
        xy_zar1 = ( int(SPATIU + MENIU + SPATIU + MARGINE + LATIME_TABLA / 2 - LATIME_TRIUNGHI / 2),
                    int(SPATIU + MARGINE + INALTIME_TABLA / 2 - L_ZAR * 2 / 3 ) )
        xy_zar2 = ( int(SPATIU + MENIU + SPATIU + MARGINE + LATIME_TABLA / 2 - LATIME_TRIUNGHI / 2 + L_ZAR),
                    int(SPATIU + MARGINE + INALTIME_TABLA / 2 - L_ZAR * 1 / 3 ) )

        self.zar1 = grafica.Zar(fereastra, L_ZAR, xy_zar1, self.zar1_numar)
        self.zar2 = grafica.Zar(fereastra, L_ZAR, xy_zar2, self.zar2_numar)

        self.fereastra = fereastra

    def afiseaza(self, fereastra):
        """
            Afiseaza/deseneaza zarurile in fereastra
        :param fereastra:
        :return:
        """
        self.zar1.afiseaza(fereastra)
        self.zar2.afiseaza(fereastra)

    def genereaza(self):
        """
            Genereaza aleator numerele zarurilor
        :return:
        """
        self.zar1_numar = random.randrange(1, 7)
        self.zar1.set_numar(self.zar1_numar)

        self.zar2_numar = random.randrange(1, 7)
        self.zar2.set_numar(self.zar2_numar)

        # actualizeaza valorile zarurilor si in obiectul Tabla
        self.tabla.getZaruri()

        # calculeaza in obiectul Tabla mutarile posibile
        self.tabla.mutariPosibileDinBara()

        # afiseaza din noua fereastra grafica ca sa fie afisate noile numere
        self.afiseaza(self.fereastra)

        pygame.display.flip()

    def getNumere(self):
        """
            Intoarce numerele ordonate de pe zaruri sub forma unei tuple, cu 4 valori daca este o dubla
        :return:
        """
        if self.zar1_numar == self.zar2_numar:
            numList = [self.zar1_numar] * 4
            return sorted(numList)
        return sorted([self.zar1_numar, self.zar2_numar])

class Piesa:
    """
        Clasa pentru o piesa de table
    """

    def __init__(self, culoare):
        """
            Constructor
        :param culoare:
        """
        self.culoare = culoare
        self.mijloc = (0, 0)
        self.piesa = grafica.PiesaTable(self.culoare, self.mijloc, RAZA_PIESA)

    def afiseaza(self, fereastra, peste_5):
        """
            Afiseaza piesa in fereastra grafica
        :param fereastra:
        :param peste_5:
        :return:
        """
        self.piesa.afiseaza(fereastra, peste_5)

    def getCuloare(self):
        """
            Intoarce culoarea piesei
        :return:
        """
        return self.culoare

    def muta(self, mijloc):
        """
            Seteaza centrul piesei in vederea mutarii
        :param center:
        :return:
        """
        self.piesa.muta(mijloc)

class Linie:
    """
        Clasa pentru liniile de pe tabla (triunghiuri), cu aceasta clasa vor interactiona jucatorii
    """

    def __init__(self, x, y, susjos, tabla, zaruri, culoare, fereastra):

        self.numar = None
        self.culoare = culoare

        # True daca linia reprezinta o linie de destinatie valida in cadrul unei mutari
        self.mutare_valida = False
        self.tabla = tabla
        self.zaruri = zaruri
        self.susjos = susjos
        self.fereastra = fereastra

        # Coltul din dreapta al triunghiului corespunzator liniei
        self.x = x
        self.y = y

        # Setarea triunghiului grafic daca este o linie in partea de jos
        if susjos == 'jos':
            self.triangle = grafica.Triunghi(self.culoare, ((x, y), (x - LATIME_TRIUNGHI, y),
                                                                   (x - LATIME_TRIUNGHI / 2, y - INALTIME_TRIUNGHI)), susjos)

        # Setarea triunghiului grafic daca este o linie in partea de sus
        else:
            self.triangle = grafica.Triunghi(self.culoare, ((x, y), (x + LATIME_TRIUNGHI, y),
                                                                   (x + LATIME_TRIUNGHI / 2, y + INALTIME_TRIUNGHI)), susjos)

        self.piese = []
        self.vida = True  # True daca linia nu contine nicio piesa
        self.singura = False  # True daca linia contine o singura piesa, utilizat atunci cand se scot piese
        self.jucator = None  # Culoarea jucatorului a carui piese sunt pe linie
        self.activa = False  # True daca linia este a jucatorului curent
        self.selectata = False  # True daca jucatorul a ales linia ca destinatie pentru o mutare

    def verifica_mouse(self, pos):
        """
            Verifica daca s-a facut clic in spatiul liniei (un dreptunghi mai mare decat triunghiul cu RAZA_PIESA)
        :param pos:
        :return:
        """
        if self.triangle.verifica_mouse(pos):
            self.clicLinie()

    def afiseaza(self, fereastra):
        """
            Afiseaza triunghiul corespunzator liniei in fereastra grafica
        :param fereastra:
        :return:
        """
        self.triangle.afiseaza(fereastra)

    def afiseazaPiese(self, fereastra):
        """
            Afiseaza/deseneaza piesele de pe linie
            In cazul in care sunt mai mult de 5 piese pe linie este memorata piesa cu nr. 5
            pentru a se inscrie pe ea numarul total de piese de pe linia respectiva
        :param fereastra:
        :return:
        """
        j=0
        ultima = None
        for piesa in self.piese:
            piesa.afiseaza(fereastra, 0)
            j = j + 1
            if j == 5:
                ultima = piesa

        if ultima != None:
            ultima.afiseaza(fereastra, j)

    def clicLinie(self):
        """
            Functie care realizeaza operatiile de selectare, deselectare a liniilor si mutare a pieselor
            atunci cand jucatorul face clic pe linie
        :return:
        """
        bara_mijloc_vida = self.tabla.baraMijlocVida()  # True daca nu este nicio piesa a jucatorului curent
                                                        # pe bara din mijloc

        # Se incearca scoaterea piesei din linie 
        # daca piesa este scoasa se iese din functie
        if self.tabla.toatePieseleInCasa():
            if self.activa and not self.tabla.lineSelectata():
                if self.tabla.incearcaScoatereAfara(self):
                    return

        # Se verifica daca se poate realiza mutarea unei piese intre linii
        if bara_mijloc_vida:
            if self.selectata:
                self.scoateSelectia() # se face deselectarea liniei sursa
            elif self.activa and not (self.selectata or self.tabla.lineSelectata()):
                self.clic() # se face selectia destinatiei 
            elif self.mutare_valida:
                self.tabla.mutaPiesa(self)

        # Daca exista vreo piesa in bara de mijloc a jucatorului curent se scoate de acolo o piesa        
        else:
            if self.mutare_valida:
                self.tabla.scoatePiesaDinBaraMijloc(self)

    def scoateSelectia(self):
        """
            Se deselecteaza linia sursa si sunt sterse mutarile care au fost considerate posibile
        :return:
        """
        self.selectata = False
        # pentru stergerea chenarului portocaliu
        self.setActiv(NEGRU, False)
        
        self.tabla.stergeMutariPosibile(self.numar)

    def clic(self):
        """
            Seteaza linia pe care s-a facut clic ca fiind selectata si se calculeaza mutarile posibile
            pentru jucatorul curent plecand de la linia selectata
        :return:
        """
        self.selectata = True
        # pentru marcarea liniei, desenarea chenarului portocaliu
        self.setActiv(PORTOCALIU, True)
        self.tabla.mutariPosibile(self.numar)

    def adaugaPiesa(self, piesa):
        """
            Adauga o piesa la linie
        :param piesa:
        :return:
        """
        self.piese.append(piesa)

    def scoatePiesa(self):
        """
            Scoate prima piesa din linie
        :return:
        """
        self.piese.pop(0)

    def getPiesa(self):
        """
            Intoarce prima piesa din linie
        :return: 
        """
        return self.piese[0]

    def esteVida(self):
        """
            Intoarce daca linia este sau nu vida 
        :return: 
        """
        return self.vida

    def este1Piesa(self):
        """
            Intoarce True daca pe linie se afla o singura piesa
        :return: 
        """
        return self.singura

    def esteSelectata(self):
        """
            Intoarce True daca linia este selectata
        :return:
        """
        return self.selectata

    def get_jucator(self):
        """
            Intoarce culoarea jucatorului a carui piese sunt pe linie sau None daca nu este nicio piesa pe linie
        :return:
        """
        return self.jucator

    def setActiv(self, culoare, activ):
        """
            Seteaza daca linia este activa si cu ce culoare trebuie desenata evidentierea
        :param culoare:
        :param activ:
        :return:
        """
        self.triangle.setActiv(culoare, activ)
        self.tabla.afiseaza_tabla()

    def aranjarePiese(self):
        """
            Aranjeaza (grafic) piesele pe fiecare linie astfel incat sa fie corect afisate
        :return: 
        """
        if self.susjos == 'jos':
            for i in range(len(self.piese)):
                self.piese[i].muta((int(self.x - LATIME_TRIUNGHI / 2),
                                         int(self.y - RAZA_PIESA
                                             - (i % 5) * 2 * RAZA_PIESA)))
        else:
            for i in range(len(self.piese)):
                self.piese[i].muta((int(self.x + LATIME_TRIUNGHI / 2),
                                         int(self.y + RAZA_PIESA
                                             + (i % 5) * 2 * RAZA_PIESA)))

    def update(self):
        """
            Actualizeaza atributele unei linii dupa efectuarea mutarii
        :return:
        """
        self.vida = not len(self.piese)
        if len(self.piese) == 1:
            self.singura = True
        else:
            self.singura = False
        if len(self.piese) != 0:
            self.jucator = self.piese[0].getCuloare()
        else:
            self.jucator = None

    def marcheazaActiva(self):
        """
            Marcheaza linia ca fiind activa daca este a jucatorului curent
        :return: 
        """
        if self.tabla.getCuloareJucator() == self.jucator:
            self.activa = True
        else:
            self.activa = False

    def adaugaNumar(self, numar):
        """
            Seteaza numarul unei linii
        :param numar: 
        :return: 
        """
        self.numar = numar

    def getNumar(self):
        """
            Intoarce numarul liniei
        :return:
        """
        return self.numar

    def mutareValida(self, value):
        """
            Seteaza mutarea ca fiind valida
        :param value: 
        :return: 
        """
        self.mutare_valida = value


class Bara:
    """
        Clasa pentru barele din mijloca ale jucatorilor unde se stocheaza piesele care sunt scoase in timpul jocului
    """

    def __init__(self, jucator, tabla):

        self.tabla = tabla
        self.jucator = jucator

        x_bara = SPATIU + MENIU + SPATIU + MARGINE + LATIME_TABLA / 2 - LATIME_TRIUNGHI / 2
        y_bara = SPATIU + MARGINE

        # Bara jucatorului cu piese negre
        if self.jucator == NEGRU:
            self.bare_mijloc = grafica.Dreptunghi( tabla.fereastra, ( int(x_bara), int(y_bara + INALTIME_TABLA / 2) ),
                                           int(LATIME_TRIUNGHI), int((INALTIME_TABLA+2) / 2) , CULOARE_MARGINE)

        # bara jucatorului cu piese albe
        else:
            self.bare_mijloc = grafica.Dreptunghi( tabla.fereastra, (int(x_bara), int(y_bara)),
                                           int(LATIME_TRIUNGHI), int((INALTIME_TABLA) / 2), CULOARE_MARGINE)

        self.piese = []
        self.vida = True  # True daca bara din mijloc nu are nicio piesa
        self.activa = False  # True daca bara din mijloc este a jucatorului curent

    def afiseaza(self, fereastra):
        """
            Afiseaza/deseneaza bara de mjloc in fereastra grafica
        :param fereastra:
        :return:
        """
        self.bare_mijloc.afiseaza(fereastra)

    def afiseazaPiese(self, fereastra):
        """
            Afiseaza/deseneaza piesele pe bara din mijloc
        :param fereastra:
        :return:
        """
        for piesa in self.piese:
            piesa.afiseaza(fereastra, 0)

    def adaugaPiesa(self, piesa):
        """
            Adauga o piesa la bara de mijloc
        :param piesa:
        :return:
        """
        self.piese.append(piesa)

    def getPiesa(self):
        """
            Intoarce prima piesa din bara de mijloc
        :return:
        """
        return self.piese[0]

    def scoatePiesa(self):
        """
            Scoate prima piesa din bara de mijloc
        :return:
        """
        self.piese.pop(0)

    def esteVida(self):
        """
            Intoarce True daca bara din mijloc este vida, nu este nicio piesa in ea
        :return:
        """
        return self.vida

    def aranjarePiese(self):
        """
            Aranjeaza piesele astfel incat sa fie afisate corespunzator pe bara din mijloc, dupa ce au fost mutate
        :return:
        """
        for i in range(len(self.piese)):
            x_bara_mijloc = int(SPATIU + MENIU + SPATIU + MARGINE + LATIME_TABLA / 2)

            # aranjeaza piesele negre pe bara din mijloc
            if self.jucator == NEGRU:
                self.piese[i].muta((x_bara_mijloc,
                                    int( SPATIU + MARGINE + INALTIME_TABLA - RAZA_PIESA - (i % 5) * 2 * RAZA_PIESA)))

            # aranjeaza piesele albe pe bara din mijloc
            else:
                self.piese[i].muta((x_bara_mijloc, int(SPATIU + MARGINE + RAZA_PIESA + (i % 5) * 2 * RAZA_PIESA)))

    def update(self):
        """
            Actualizeaza atributele barei din mijloc
        :return:
        """
        self.vida = not len(self.piese)

    def marcheazaActiva(self):
        """
            Marhceaza bara de mijloc ca fiind a jucatorului curent
        :return:
        """
        if self.tabla.getCuloareJucator() == self.jucator and not self.esteVida():
            self.activa = True
        else:
            self.activa = False


class BaraIesire:
    """
        Clasa pentru bara de iesire unde sunt puse piesele care sunt scoase din joc la final
    """

    def __init__(self, fereastra):
        """
            Constuctor
        :param fereastra:
        """
        self.bara = grafica.Dreptunghi( fereastra, ( int(LATIME_FEREASTRA - SPATIU - LATIME_TRIUNGHI),
                                               int(SPATIU) ),
                                       LATIME_TRIUNGHI, INALTIME_TABLA + 2 * MARGINE, CULOARE_MARGINE)
        self.negre = []
        self.albe = []
        self.fereastra = fereastra

    def afiseaza(self, fereastra):
        """
            Afiseaza bara de iesire in fereastra grafica
        :param fereastra: 
        :return: 
        """
        self.bara.afiseaza(fereastra)

    def afiseazaPiese(self, fereastra):
        """
            Afiseaza piesele care sunt scoase in bara de iesire
        :param fereastra:
        :return:
        """
        for piesa in self.albe:
            piesa.afiseaza(self.fereastra, 0)
        for piesa in self.negre:
            piesa.afiseaza(self.fereastra, 0)

    def adaugaPiesa(self, piesa):
        """
            Adauga piesa la bara de iesire si o pozitioneaza corect pentru afisare
        :param piesa:
        :return:
        """
        # se calculeaza mijlocul barei de iesire
        y_bara_mijloc = int(SPATIU + MARGINE + INALTIME_TABLA / 2)

        # Adauga piesele negre
        if piesa.getCuloare() == NEGRU:
            self.negre.append(piesa)
            piesa.muta((int((LATIME_FEREASTRA - SPATIU - LATIME_TRIUNGHI / 2)), \
                            int(y_bara_mijloc - RAZA_PIESA - (len(self.negre) - 1) * RAZA_PIESA / 3)))
            self.negre.append(piesa)

        # Adauga piesele albe
        else:
            self.albe.append(piesa)
            piesa.muta((int((LATIME_FEREASTRA - SPATIU - LATIME_TRIUNGHI / 2)), \
                            int(y_bara_mijloc - RAZA_PIESA + INALTIME_TABLA / 2 - (len(self.albe) - 1) * RAZA_PIESA / 3)))
            self.albe.append(piesa)



