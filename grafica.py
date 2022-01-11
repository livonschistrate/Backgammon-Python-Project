import os
import pygame
from pygame import gfxdraw
from constante import *
import helpers

pygame.font.init()

def punct_negru(fereastra, x, y, raza):
    """
        Functie care deseneaza un cerc negru, antialias, pentru zaruri
    :param fereastra: surface-ul pe care se deseneaza
    :param x: x ptr centrul cercului
    :param y: y ptr centrul cercului
    :param raza: razac ercului
    :return: nimic
    """
    pygame.gfxdraw.aacircle(fereastra, x, y, raza, NEGRU)
    pygame.gfxdraw.filled_circle(fereastra, x, y,raza, NEGRU)


class Text:
    """
        Clasa folosita pentru a afisa texte in fereastra grafica
    """

    def __init__(self, text, xy, marime, culoare = NEGRU, bold = False, centrat = False):
        self.text = text
        self.xy = xy
        self.marime = marime
        self.culoare = culoare
        self.bold = bold
        self.centrat = centrat

    def set_text(self, text):
        """
            Seteaza in obiect textul ce va fi afisat
        :param text:
        :return:
        """
        self.text = text

    def afiseaza(self, fereastra):
        """
            Afiseaza (deseneaza) textul in fereastra grafica tinand cont de parametrul centrat
        :param fereastra:
        :return:
        """
        font = FONT
        if self.bold:
            font = font + " Bold"
        self.textul = pygame.font.SysFont(font, self.marime)
        self.eticheta = self.textul.render(self.text, 1, self.culoare)
        latime_text, inaltime_text = self.eticheta.get_size()
        if self.centrat:
            fereastra.blit(self.eticheta, (self.xy[0] - latime_text / 2, self.xy[1] - inaltime_text / 2))
        else:
            fereastra.blit(self.eticheta, self.xy)


class ButonGrafic:
    """
        Implementeaza grafica pentru un buton
    """
    def __init__(self, text, stanga_sus, latime, inaltime):
        """
            Constructor
        :param text:
        :param stanga_sus:
        :param latime:
        :param inaltime:
        """
        self.text = text
        self.stanga_sus = stanga_sus
        self.latime = latime
        self.inaltime = inaltime
        self.eticheta = Text(self.text, ( int(self.stanga_sus[0] + self.latime / 2), int(self.stanga_sus[1] + self.inaltime / 2)), int(10 * ZOOM/2), NEGRU, False, True)

    def afiseaza(self, fereastra):
        """
            Afiseaza/deseneaza butonul
        :param fereastra:
        :return:
        """
        helpers.aa_round_rect(fereastra, (
            int(self.stanga_sus[0]),
            int(self.stanga_sus[1]),
            int(self.latime),
            int(self.inaltime)), NEGRU, 1, 1, GRI_DESCHIS)
        self.eticheta.afiseaza(fereastra)


class Dreptunghi:
    """
        Clasa folosita pentru a afisa un dreptunghi, pentru desenarea partilor din tabla de joc
    """

    def __init__(self, surface, stanga_sus, latime, inaltime, culoare, fundal_imagine=False):
        """
            Constructor
        :param surface:
        :param stanga_sus:
        :param latime:
        :param inaltime:
        :param culoare:
        :param fundal_imagine:
        """
        self.surface = surface
        self.latime = latime
        self.inaltime = inaltime
        self.stanga_sus = stanga_sus
        self.culoare = culoare
        self.fundal_imagine = fundal_imagine

    def afiseaza(self, fereastra):
        """
            Afiseaza dreptunghiul in fereastra grafica
            Exceptie face fundalul de la tabla de joc atunci cand este desenat se incarca o imagine
        :param fereastra:
        :return:
        """
        if self.fundal_imagine:
            imagine_orig = pygame.image.load(os.path.join('imagini', 'lemn.jpg')).convert()
            imagine = imagine_orig.subsurface((1, 1, self.latime, self.inaltime) )
            fereastra.blit(imagine, (self.stanga_sus[0], self.stanga_sus[1]) )
            pygame.draw.rect(fereastra, NEGRU, (self.stanga_sus[0], self.stanga_sus[1], self.latime, self.inaltime+1), 1)
        else:
            pygame.draw.rect(fereastra, self.culoare ,(self.stanga_sus[0], self.stanga_sus[1], self.latime, self.inaltime))
            pygame.draw.rect(fereastra, NEGRU,(self.stanga_sus[0], self.stanga_sus[1], self.latime, self.inaltime), 1)

    def verifica_mouse(self, xy):
        """
            Se verifica daca s-a facut clic in interiorul dreptunghiului
        :param xy:
        :return:
        """
        if xy[0] > self.stanga_sus[0] and xy[0] < self.stanga_sus[0] + self.latime\
           and xy[1] > self.stanga_sus[1] and xy[1] < self.stanga_sus[1] + self.inaltime:
            return True
        return False


class Zar:
    """
        Clasa folosita pentru a desena un zar
    """

    def __init__(self, fereastra, latime, stanga_sus, numar):
        """
            Constructor
        :param fereastra:
        :param latime:
        :param stanga_sus:
        :param numar:
        """
        self.fereastra = fereastra
        self.latime = latime
        self.stanga_sus = stanga_sus
        self.numar = numar

    def afiseaza(self, fereastra):
        """
            Afiseaza/deseneaza zarul in fereastra grafica, deseneaza un patrat alb cu colturi rotunjite
            si apoi pune puncte negre in functie de numarul de pe zar
        :param fereastra:
        :return:
        """
        self.rotunjire = int(PUNCT_ZAR)

        # un dreptunghi alb cu colturile rotunjite
        helpers.aa_round_rect(fereastra, (
            int(self.stanga_sus[0]),
            int(self.stanga_sus[1]),
            int(L_ZAR),
            int(L_ZAR)), NEGRU, self.rotunjire, 1, ALB)
        if ( self.numar == 1 ):
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR / 2),
                                    int(self.stanga_sus[1] + L_ZAR / 2), self.rotunjire)
        elif (self.numar == 2):
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR / 4),
                        int(self.stanga_sus[1] + L_ZAR / 4), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR - L_ZAR / 4),
                        int(self.stanga_sus[1] + L_ZAR - L_ZAR / 4), self.rotunjire)
        elif (self.numar == 3):
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR / 4),
                        int(self.stanga_sus[1] + L_ZAR / 4), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR / 2),
                        int(self.stanga_sus[1] + L_ZAR / 2), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR - L_ZAR / 4),
                        int(self.stanga_sus[1] + L_ZAR - L_ZAR / 4), self.rotunjire)
        elif (self.numar == 4):
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR / 4),
                        int(self.stanga_sus[1] + L_ZAR / 4), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR - L_ZAR / 4),
                        int(self.stanga_sus[1] + L_ZAR / 4), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR - L_ZAR / 4),
                        int(self.stanga_sus[1] + L_ZAR - L_ZAR / 4), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR / 4),
                        int(self.stanga_sus[1] + L_ZAR - L_ZAR / 4), self.rotunjire)
        elif ( self.numar == 5 ):
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR / 4),
                                    int(self.stanga_sus[1] + L_ZAR / 4), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR - L_ZAR / 4),
                                    int(self.stanga_sus[1] + L_ZAR / 4), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR - L_ZAR / 4),
                                    int(self.stanga_sus[1] + L_ZAR - L_ZAR / 4), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR / 4),
                                    int(self.stanga_sus[1] + L_ZAR - L_ZAR / 4), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR / 2),
                                    int(self.stanga_sus[1] + L_ZAR / 2), self.rotunjire)
        elif ( self.numar == 6 ):
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR / 4),
                                    int(self.stanga_sus[1] + L_ZAR / 4), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR / 4),
                                    int(self.stanga_sus[1] + L_ZAR / 2), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR / 4),
                                    int(self.stanga_sus[1] + L_ZAR - L_ZAR / 4), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR -  L_ZAR / 4),
                                    int(self.stanga_sus[1] + L_ZAR / 4), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR -  L_ZAR / 4),
                                    int(self.stanga_sus[1] + L_ZAR / 2), self.rotunjire)
            punct_negru(fereastra, int(self.stanga_sus[0] + L_ZAR -  L_ZAR / 4),
                                    int(self.stanga_sus[1] + L_ZAR - L_ZAR / 4), self.rotunjire)

    def set_numar(self, numar):
        """
            Seteaza numarul de pe zar
        :param numar:
        :return:
        """
        self.numar = numar

class Triunghi:
    """
        Clasa care rolul de desena un triunghi corespunzator unei linii pe tabla de joc si de a gestiona evenimentele
        atunci cand se face clic pe spatiul triunghiului
    """

    def __init__(self, culoare, varfuri, susjos):
        """
            Constructor
        :param culoare:
        :param varfuri:
        :param susjos:
        """
        self.culoare = culoare
        self.varf1 = varfuri[0]
        self.varf2 = varfuri[1]
        self.varf3 = varfuri[2]
        self.susjos = susjos
        self.culoare_contur = NEGRU
        self.activ = False

    def setActiv(self, culoare, activ=False):
        """
            Seteaza daca triunghiul corespunzator unei linii este activ, sau nu, si culoarea cu care trebuie
            desenata evidentierea liniei
        :param culoare:
        :param activ:
        :return:
        """
        self.culoare_contur = culoare
        self.activ = activ

    def afiseaza(self, fereastra):
        """
            Afiseaza/deseneaza triunghiul in fereastra grafica
        :param fereastra:
        :return:
        """
        # sunt folosite functiile din gfxdraw pentru a desena antialias
        pygame.gfxdraw.filled_trigon(fereastra, int(self.varf1[0]), int(self.varf1[1]), int(self.varf2[0]),
                                int(self.varf2[1]), int(self.varf3[0]), int(self.varf3[1]), (self.culoare[0],self.culoare[1],self.culoare[2], 160))
        pygame.gfxdraw.aapolygon(fereastra, (self.varf1, self.varf2, self.varf3), GRI)
        if self.activ:
            factor = 0
            if self.susjos == 'jos':
                factor = 1
            pygame.draw.rect(fereastra, self.culoare_contur,
                             (self.varf1[0] - factor * LATIME_TRIUNGHI,
                              self.varf1[1] - factor * (INALTIME_TRIUNGHI + RAZA_PIESA + 4),
                              LATIME_TRIUNGHI,
                              INALTIME_TRIUNGHI + RAZA_PIESA + 4),
                             3)
            factor = -1
            if self.susjos == 'jos':
                factor = 1
            mijloc = (self.varf1[0] + self.varf2[0]) / 2
            pygame.gfxdraw.filled_polygon(fereastra,(
                                ( int( mijloc ), int(self.varf1[1]) ),
                                ( int( mijloc - LATIME_MARKER / 2 ), int(self.varf1[1] + factor * INALTIME_MARKER)),
                                ( int( mijloc + LATIME_MARKER / 2 ), int(self.varf1[1] + factor * INALTIME_MARKER)) ),
                                self.culoare_contur)

    def verifica_mouse(self, xy):
        """
            Verifica daca s-a facut clic in zona unui triunghi.
            Se ia in considerare cu 2 * RAZA_PIESA mai mult in sus/jos
        :param xy: pozitia cursorului
        :return:
        """
        if self.susjos == 'jos':
            if xy[0] > self.varf2[0] and xy[0] < self.varf1[0] and\
               xy[1] < self.varf1[1] + int(2 * RAZA_PIESA) and xy[1] > self.varf3[1]:
                return True
        else:
            if xy[0] < self.varf2[0] and xy[0] > self.varf1[0] and\
               xy[1] > self.varf1[1] and xy[1] < self.varf3[1] + int( 2 * RAZA_PIESA):
                return True
        return False


class PiesaTable:
    """
        Clasa pentru a desena o piesa, folosita pentru desenarea pieselor din joc
    """

    def __init__(self, culoare, mijloc, raza):
        """
            Constructor
        :param culoare:
        :param mijloc:
        :param raza:
        """
        self.culoare = culoare
        self.mijloc = mijloc
        self.raza = raza

    def afiseaza(self, fereastra, peste_5 = 0 ):
        """
            Deseneaza piesa in feresatra grafica la coordonatele setate cu culoarea setata
            Daca peste_5 este mai mare decat 5 se afiseaza si o cifra in a 5-a piesa pentru a
            indica faptul ca sunt mai mult de 5 piese pe linia respectiva
        :param fereastra: 
        :param peste_5: 
        :return: 
        """
        if self.culoare == NEGRU:
            pygame.gfxdraw.filled_circle(fereastra, int(self.mijloc[0]), int(self.mijloc[1]), int(self.raza),
                                         self.culoare)
            pygame.gfxdraw.filled_circle(fereastra, int(self.mijloc[0]), int(self.mijloc[1]), int(self.raza * 0.8),
                                         (128,128,128,40))

        else:
            pygame.gfxdraw.filled_circle(fereastra, int(self.mijloc[0]), int(self.mijloc[1]), int(self.raza),
                                         self.culoare)
            pygame.gfxdraw.filled_circle(fereastra, int(self.mijloc[0]), int(self.mijloc[1]), int(self.raza),
                                         (128,128,128,40))
            pygame.gfxdraw.filled_circle(fereastra, int(self.mijloc[0]), int(self.mijloc[1]), int(self.raza * 0.8),
                                         self.culoare)

        pygame.gfxdraw.aacircle(fereastra, int(self.mijloc[0]), int(self.mijloc[1]), int(self.raza * 0.8),
                                (0,0,0,80) )
        pygame.gfxdraw.aacircle(fereastra, int(self.mijloc[0]), int(self.mijloc[1]), int(self.raza), NEGRU)

        # artificiu pentru a desena si o cifra in mijlocul cercului daca sunt mai mult de 5 piese intr-o linie
        if (peste_5 > 5):
            self.fontul = pygame.font.SysFont(FONT + ' Bold',int ( 14 * ZOOM) )

            # se alege culoarea textului de pe piesa in functie de culoarea piesei
            culoare_numar = GRI_INCHIS
            if self.culoare == NEGRU:
                culoare_numar = GRI_DESCHIS
            self.eticheta = self.fontul.render(str(peste_5), 1, culoare_numar)
            latime_text, inaltime_text = self.eticheta.get_size()

            # afiseaza eticheta cu textul care contine numarul de piese pe linia respectiva, cu mici corectii pentru
            # centrarea textului, 1 pe orizontala si 2 pe verticala
            fereastra.blit(self.eticheta,
                           (self.mijloc[0] - latime_text / 2 + 1, self.mijloc[1] - inaltime_text / 2 + 2) )

    def muta(self, mijloc):
        """
            Seteaza centrul piesei in vederea mutarii ei
        :param mijloc:
        :return:
        """
        self.mijloc = mijloc

