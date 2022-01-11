# Proiect python Liviu Istrate
import pygame
import obiecte
import grafica
from constante import *


class Jucator:
    """
        Clasa care reprezinta un jucator
    """

    def __init__(self, culoare, tabla):
        self.culoare = culoare
        self.tabla = tabla
        self.linii = []

    def adauga_linii(self, linii):
        """
            Adauga liniile cu piese unui jucator
        :param linii:
        :return:
        """
        self.linii = linii

    def getCuloare(self):
        """
            Intoarce culoarea jucatorului
        :return:
        """
        return self.culoare


class Tabla:
    """
        Clasa principala care contine tabla de joc si elementele din ea
    """

    def __init__(self, fereastra):

        self.castigat = False
        self.fereastra = fereastra

        x_tabla = int(SPATIU + MENIU + SPATIU + MARGINE)
        y_tabla = int(SPATIU + MARGINE)

        self.fundal = grafica.Dreptunghi( fereastra,
                                          (x_tabla, y_tabla),
                                          int(LATIME_TABLA), int(INALTIME_TABLA), FUNDAL, True)
        self.margine = grafica.Dreptunghi( fereastra,
                   (int( x_tabla - MARGINE), int(y_tabla - MARGINE)),
                   int(LATIME_TABLA + MARGINE * 2), int(INALTIME_TABLA + MARGINE * 2),
                    CULOARE_MARGINE)

        # Creaza barele din mijloc, cate una pentru fiecare jucator, bare unde vor fi puse piesele care sunt scoase de
        # oponent pentru a fi trimise in casa
        self.bare_mijloc = []
        self.bare_mijloc.append(obiecte.Bara(NEGRU, self))
        self.bare_mijloc.append(obiecte.Bara(ALB, self))

        # Creaza bara de iesire pentru piesele care sunt scoase din joc la final
        self.bara_iesire = obiecte.BaraIesire(self.fereastra)

        # Creare jucatori
        self.jucatori = []
        for culoare in [NEGRU, ALB]:
            self.jucatori.append(Jucator(culoare, self))
        
        # Setare primul jucator cu piesele albe
        self.jucator = 1

        # initializare clasa pentru zaruri
        self.zaruri = obiecte.Zaruri(self, self.fereastra)

        # Creare lista cu toate liniile (triunghiurile de pe tabla)

        self.linii = []

        # Creare linii pentru partea de jos a tablei de joc
        for i in range(13):
            if i != 6:
                if i % 2 == 0:
                    # Creates white linii
                    self.linii.append(obiecte.Linie(
                        (x_tabla + LATIME_TABLA) - (i * (LATIME_TRIUNGHI)),
                        y_tabla + INALTIME_TABLA,
                        'jos', self,
                        self.zaruri, BEJ, self.fereastra))
                else:
                    # Creates red linii
                    self.linii.append(obiecte.Linie(
                        x_tabla + LATIME_TABLA - (i * (LATIME_TRIUNGHI)),
                        y_tabla + INALTIME_TABLA, 'jos', self,
                        self.zaruri, NEGRU, self.fereastra))

        # Creare linii pentru partea de sus a tablei de joc
        for i in range(13):
            if i != 6:
                if i % 2:
                    self.linii.append(obiecte.Linie(
                        x_tabla +(i * (LATIME_TRIUNGHI)),
                        y_tabla, 'top', self,
                        self.zaruri, BEJ, self.fereastra))
                else:
                    self.linii.append(obiecte.Linie(
                        x_tabla +(i * (LATIME_TRIUNGHI)),
                        y_tabla, 'top', self,
                        self.zaruri, NEGRU, self.fereastra))

        # Se pun piesele de joc pentru configuratia de inceput a jocului
        for _ in range(2):
            self.linii[0].adaugaPiesa(obiecte.Piesa(NEGRU))
            self.linii[23].adaugaPiesa(obiecte.Piesa(ALB))
        for _ in range(3):
            self.linii[7].adaugaPiesa(obiecte.Piesa(ALB))
            self.linii[16].adaugaPiesa(obiecte.Piesa(NEGRU))
        for _ in range(5):
            self.linii[5].adaugaPiesa(obiecte.Piesa(ALB))
            self.linii[11].adaugaPiesa(obiecte.Piesa(NEGRU))
            self.linii[12].adaugaPiesa(obiecte.Piesa(ALB))
            self.linii[18].adaugaPiesa(obiecte.Piesa(NEGRU))

        # Configurarea / initializarea liniior pentru jucatori
        self.set_linii()

        # La inceput nicio piesa/linie nu este selectata
        self.linia_selectata = None

        # O lista de numere ale zarurilor care va fi folosita pentru mutarile posibile
        self.numere_zaruri = []

        # Adaugarea lista de linii/triunghiuri la fiecare jucator
        for jucator in self.jucatori:
            jucator.adauga_linii(self.linii)

        # Prima aruncare de zaruri la inceput
        self.zaruri.genereaza()

        self.meniu = obiecte.Meniu(fereastra)
        self.meniu.setRand("Jucătorul cu piesele " + self.get_culoare_jucator() + " mută")

        self.afiseaza_tabla()

    def joc_castigat(self):
        """
            Intoarce True/False daca jocul este castigat (terminat)
        :return:
        """
        return self.castigat

    def afiseaza_tabla(self):
        """
            Afiseaza toate elementele grafice
        :return:
        """
        # mai intai se deseneaza marginea tabelei
        self.margine.afiseaza(self.fereastra)

        # peste margine se deseneaza tabela de joc
        self.fundal.afiseaza(self.fereastra)
        for linie in self.linii:
            linie.afiseaza(self.fereastra)
            linie.afiseazaPiese(self.fereastra)

        # se deseneaza bara de iesire
        self.bara_iesire.afiseaza(self.fereastra)

        # se deseneaza piesele de pe bara de iesire
        self.bara_iesire.afiseazaPiese(self.fereastra)

        # se deseneaza barele din mijloc si eventualele piese de pe ele
        for bare_mijloc in self.bare_mijloc:
            bare_mijloc.afiseaza(self.fereastra)
            bare_mijloc.afiseazaPiese(self.fereastra)

        # se deseneaza zarurile
        self.zaruri.afiseaza(self.fereastra)

        # inainte de afisare se construiesc string-urile pentru afisarea informatiilor suplimentare
        if len(self.numere_zaruri) == 1:
            de_afisat = "O mutare rămasă: "
        else:
            de_afisat = str(len(self.numere_zaruri)) + " mutări rămase: "
        for numar in self.numere_zaruri:
            de_afisat = de_afisat + "  " + str(numar)
        self.meniu.setMutari(de_afisat)

        # se afiseaza meniul
        self.meniu.afiseaza(self.fereastra)

        pygame.display.flip()

    def get_culoare_jucator(self):
        """
            Intoarce culoarea jucatorului curent (la mutare) pentru afisare, pentru cuvantul piese
        :return:
        """
        if self.getCuloareJucator() == NEGRU:
            return 'NEGRE'
        return 'ALBE'

    def verifica_mouse(self, xy):
        """
            Verifica daca s-a facut vreun clic pe elementele din ecranul grafic
        :param xy:
        :return:
        """
        if self.meniu.btn_schimba_randul.verifica_mouse(xy):
            self.schimbaJucatorul()
            self.afiseaza_tabla()
        for linie in self.linii:
            linie.verifica_mouse(xy)

    def verificaJocTerminat(self, fereastra):
        """
            Verifica daca jocul este castigat/terminat prin verificare pieselor pe liniile jucatorilor
        :param fereastra:
        :return:
        """
        joc_castigat = True

        # se verifica daca mai exista vreo piesa pe vreo linie
        for linie in self.linii:
            if linie.get_jucator() == self.getCuloareJucator():
                joc_castigat = False

        # Afiseaza ecranul pentru terminarea jocului
        if joc_castigat:
            # se face tot ecranul negru
            self.fereastra.fill(NEGRU)

            # se afiseaza mesajul cu jucatorul castigator
            mesaj_final_1 = grafica.Text("Jucătorul cu piesele " + self.get_culoare_jucator() + ' a câștigat!', (int(LATIME_FEREASTRA/2),int(INALTIME_FEREASTRA/2)), 30, ALB, True, True)
            mesaj_final_1.afiseaza(self.fereastra)

            # se afiseaza intrebarea pentru a juca din nou
            mesaj_final_2 = grafica.Text("Jucați din nou?", (int(LATIME_FEREASTRA/2),int(INALTIME_FEREASTRA/2 + 20 * ZOOM)), 30, ALB, True, True)
            mesaj_final_2.afiseaza(self.fereastra)

            # se afiseaza un buton pentru Da, rejucare
            self.btn_rejoaca_1 = obiecte.Buton("Da", (int(LATIME_FEREASTRA/2 - 36 * ZOOM),int(INALTIME_FEREASTRA/2 + 25 * ZOOM)), int(12 * ZOOM), int(12 * ZOOM))
            self.btn_rejoaca_1.afiseaza(self.fereastra)

            # se afiseaza un buton pentru iesire
            self.btn_rejoaca_2 = obiecte.Buton("Nu, ieșire", (int(LATIME_FEREASTRA/2 + 10 * ZOOM),int(INALTIME_FEREASTRA/2 + 25 * ZOOM)), int(30 * ZOOM), int(12 * ZOOM))
            self.btn_rejoaca_2.afiseaza(self.fereastra)

            # actualizeaza ecranul grafic
            pygame.display.flip()
            
            self.castigat = True

    def toatePieseleInCasa(self):
        """
            Verifica daca toate piesele jucatorului curent sunt in casa
            (se cauta de fapt piese ale jucatorului care nu sunt in casa)
        """

        # creare linii de inceput si sfarsit pentru fiecare jucator, liniile in afara casei care sunt verificate
        # daca mai contin vreo piesa de-a jucatorului
        if self.getCuloareJucator() == NEGRU:
            start = 0
            stop = 18
        else:
            start = 6
            stop = 24

        # se verifica daca jucatorul curent mai are vreo piesa pe liniile din afara casei
        for i in range(start, stop):
            if self.linii[i].get_jucator() == self.getCuloareJucator():
                return False

        return True

    def getZaruri(self):
        """
            Actualizeaza lista numere_zaruri cu noile valori ale zarurilor
        """
        self.numere_zaruri = []
        for num in self.zaruri.getNumere():
            self.numere_zaruri.append(num)

    def set_linii(self):
        """
            Configurarea obiectelor linii
        :return:
        """
        self.fundal.afiseaza(self.fereastra)
        for i in range(len(self.linii)):
            self.linii[i].aranjarePiese()
            self.linii[i].update()
            self.linii[i].adaugaNumar(i)
            self.linii[i].marcheazaActiva()

    def getCuloareJucator(self):
        """
            Intoarce culoarea jucatorului curent, cel care trebuie sa mute
        :return:
        """
        return self.jucatori[self.getJucator()].getCuloare()

    def getJucator(self):
        """
            Intoarce indexul pentru jucatorul curent
        :return:
        """
        return self.jucator

    def baraMijlocVida(self):
        """
            Intoarce True daca bara de mijloc a jucatorului curent este vida
        :return:
        """
        return self.bare_mijloc[self.getJucator()].esteVida()

    def schimbaJucatorul(self):
        """
            Schimba jucatorul si actualizeaza informatiile de pe linii si din bare
        :return:
        """
        # Se sterge selectia si se sterg si mutarile posibile
        for linie in self.linii:
            if linie.esteSelectata():
                linie.scoateSelectia()
        if not self.bare_mijloc[self.jucator].esteVida():
            self.stergeMutariPosbileDinBara()

        # Schimba jucatorul la mutare si actualizeaza obiectele corespunzator
        self.jucator = (self.jucator + 1) % 2

        # genereaza noi valori pentru zaruri
        self.zaruri.genereaza()

        for linie in self.linii:
            linie.marcheazaActiva()

        for bare_mijloc in self.bare_mijloc:
            bare_mijloc.update()
            bare_mijloc.marcheazaActiva()

        self.meniu.setRand("Jucătorul cu piesele " + self.get_culoare_jucator() + " mută")

        pygame.display.flip()

    def mutaPiesa(self, linie):
        """
            Muta o piesa din linia selectata in cea aleasa ca destinatie
        :param linie:
        :return:
        """

        linia_selectata = self.linia_selectata

        # Verifica daca este o singura piesa pe linia destinatie si se scoate acea piesa
        if linie.este1Piesa() and \
                linie.get_jucator() != self.linii[linia_selectata].get_jucator():
            self.scoate1Piesa(linie)

        # Adauga piesa la linie si actualizeaza informatiile din linie
        linie.adaugaPiesa(self.linii[self.linia_selectata].getPiesa())
        linie.aranjarePiese()
        linie.update()
        linie.marcheazaActiva()

        # Scoate piesa din linia selectat (sursa) si actualizeaza informatiile din linie
        self.linii[linia_selectata].scoatePiesa()
        self.linii[linia_selectata].aranjarePiese()
        self.linii[linia_selectata].update()
        self.linii[linia_selectata].marcheazaActiva()
        self.linii[linia_selectata].scoateSelectia()

        # Actualizeaza lista cu numere de la zaruri prin scoaterea mutarii efectuate
        self.numere_zaruri.remove((linie.getNumar() - linia_selectata)
                                * (-1) ** self.jucator)

        # Schimba jucatorul
        if not len(self.numere_zaruri):
            self.schimbaJucatorul()

        # reafiseaza tabla de joc pentru a ilustra modificarile
        self.afiseaza_tabla()

    def scoatePiesaDinBaraMijloc(self, linie):
        """
            Scoate o piesa din bara de mijloc si o pune pe linia destinatie aleasa
        :param linie:
        :return:
        """

        # Daca pe linia destinatie este o singura piesa se scoate acea piesa
        if linie.este1Piesa() and \
                linie.get_jucator() != self.getCuloareJucator():
            self.scoate1Piesa(linie)

        # Adauga piesa la linie si actualizeaza informatiile din linie
        linie.adaugaPiesa(self.bare_mijloc[self.jucator].getPiesa())
        linie.aranjarePiese()
        linie.update()
        linie.setActiv(NEGRU, False)
        linie.mutareValida(False)
        linie.marcheazaActiva()

        # Scoate piesa din bara de mijloc si actualizeaza informatiile din bara de mijloc
        self.bare_mijloc[self.jucator].scoatePiesa()
        self.bare_mijloc[self.jucator].aranjarePiese()
        self.bare_mijloc[self.jucator].update()
        self.bare_mijloc[self.jucator].marcheazaActiva()

        # Se scoate din lista de mutari/numere ale zarurilor mutarea efectuata
        if self.jucator == 0:
            self.numere_zaruri.remove(linie.getNumar() + 1)
        else:
            self.numere_zaruri.remove(24 - linie.getNumar())

        # Schimba jucatorul la mutare (schimba randul) daca este cazul
        if not len(self.numere_zaruri):
            self.schimbaJucatorul()
            return

        self.bare_mijloc[self.getJucator()].afiseaza(self.fereastra)
        self.bare_mijloc[self.getJucator()].afiseazaPiese(self.fereastra)
        pygame.display.update()

        # Se sterg mutarile posibile daca nu mai sunt piese in bara de mijloc
        if self.bare_mijloc[self.jucator].esteVida():
            self.stergeMutariPosbileDinBara()

    def incearcaScoatereAfara(self, linie):
        """
            Incearca scoaterea unei piese in bara de iesire la finalul jocului. Intoarce
            False daca scoaterea nu a avut loc
        :param linie:
        :return:
        """

        # Creaza numerele necesare pentru comparatie la scoaterea pieselor
        for num in self.numere_zaruri:
            if self.getCuloareJucator() == NEGRU:
                compara = 24 - linie.getNumar()
            else:
                compara = linie.getNumar() + 1

            # Daca numarul de pe zar este suficient de mare piesa pleaca de pe linia selectat
            # si se duce in bara de iesire, se actualizeaza informatiile din linie si se reafiseaza tabla de joc
            if num >= compara:
                self.bara_iesire.adaugaPiesa(linie.getPiesa())
                linie.scoatePiesa()
                linie.aranjarePiese()
                linie.update()
                linie.marcheazaActiva()
                self.numere_zaruri.remove(num)
                self.afiseaza_tabla()

                # Se verifica daca jucatorul curent a castigat jocul
                self.verificaJocTerminat(self.fereastra)

                # Schimba jucatorul si reafiseaza tabla de joc
                if not len(self.numere_zaruri) and not self.joc_castigat():
                    self.schimbaJucatorul()
                    self.afiseaza_tabla()

                return True  # Scoaterea definitva a piesei a reusit

        return False # Scoaterea piesei nu a reusit, se intoarce False

    def mutariPosibile(self, linieStart):
        """
            Determina numarul de mutari posibile plecand de la linia selectata si tinand cont de numerele de pe zaruri
        :param linieStart: 
        :return: 
        """
        
        self.linia_selectata = linieStart
        for num in self.numere_zaruri:
            liniaUrmatoare = linieStart + num * ((-1) ** self.jucator)
            # seteaza liniile ca fiind valide daca se poate realiza o mutare pe ele
            if liniaUrmatoare < len(self.linii) and liniaUrmatoare >= 0:
                if self.linii[liniaUrmatoare].esteVida() \
                        or self.linii[liniaUrmatoare].este1Piesa() \
                        or self.linii[liniaUrmatoare].get_jucator() == self.getCuloareJucator():
                    self.linii[liniaUrmatoare].mutareValida(True)
                    self.linii[liniaUrmatoare].setActiv(VERDE, True)

    def mutariPosibileDinBara(self):
        """
            Determina care sunt mutarile posibile din bara de mijloc a jucatorului plecand de la numerele de pe
            zaruri si daca sunt piese in bara de mijloc
        :return:
        """

        if not self.bare_mijloc[self.jucator].esteVida():
            # creaza un index de linie pentru a scoate o piesa din bara de mijloc
            for num in self.numere_zaruri:
                if self.jucator == 0:
                    indexLinie = num - 1
                else:
                    indexLinie = num * (-1)

                # Seteaza liniile destinatie posibile ca fiind valide
                if self.linii[indexLinie].esteVida() \
                        or self.linii[indexLinie].este1Piesa() \
                        or self.linii[indexLinie].get_jucator() == self.getCuloareJucator():
                    self.linii[indexLinie].mutareValida(True)
                    self.linii[indexLinie].setActiv(VERDE, True)

    def stergeMutariPosibile(self, linieStart):
        """
            Sterge toate mutarile posibile care au fost determinate
        """
        self.linia_selectata = None  # Se sterge linia selectata
        for num in self.numere_zaruri:
            liniaUrmatoare = linieStart + num * ((-1) ** self.jucator)
            if liniaUrmatoare < len(self.linii) and liniaUrmatoare >= 0:
                self.linii[liniaUrmatoare].mutareValida(False)
                self.linii[liniaUrmatoare].setActiv(NEGRU, False)

    def stergeMutariPosbileDinBara(self):
        """
            Sterge liniile selectate ca mutari posibile din bara de mijloc
        :return:
        """
        for num in self.numere_zaruri:
            if self.jucator == 0:
                indexLinie = num - 1
            else:
                indexLinie = num * (-1)
            self.linii[indexLinie].mutareValida(False)
            self.linii[indexLinie].setActiv(NEGRU, False)

    def scoate1Piesa(self, linie):
        """
            Scoate o piesa de pe linie, o adauga in bara de mijloc a jucatorului si actualizeaza
            informatiile din linie
        :param linie:
        :return:
        """
        self.bare_mijloc[(self.jucator + 1) % 2].adaugaPiesa(linie.getPiesa())
        self.bare_mijloc[(self.jucator + 1) % 2].aranjarePiese()
        self.bare_mijloc[(self.jucator + 1) % 2].update()
        linie.scoatePiesa()

    def lineSelectata(self):
        """
            Intoarce True daca este selectata vreo linie
        :return:
        """
        if self.linia_selectata is None:
            return False
        return True



