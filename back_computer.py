# Proiect python Liviu Istrate
import pygame
import joc
from constante import *

fereastra = pygame.display.set_mode((LATIME_FEREASTRA, INALTIME_FEREASTRA))

tabla = joc.Tabla(fereastra)
app_activa = True

# Bucla principala a jocului
while app_activa:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            tabla.verifica_mouse(event.pos)
            if tabla.meniu.btn_inchide.verifica_mouse(event.pos):
                app_activa = False
        if tabla.jucator == 0: # jucatorul este negru
            while len(tabla.numere_zaruri)>0 and tabla.jucator==0 and not tabla.joc_castigat():
                #  mai intai se scot piese afara daca este posibil
                scoasa_una = False
                if tabla.toatePieseleInCasa():
                    for linie in tabla.linii:
                        if linie.activa:
                            if tabla.incearcaScoatereAfara(linie):
                                scoasa_una = True
                                pygame.time.wait(2000)
                                break
                if tabla.joc_castigat():
                    break
                if not scoasa_una:
                    # mai intai se incearca scoaterea din bara de mijloc daca exista
                    if not tabla.baraMijlocVida():
                        for linie in tabla.linii:
                            if (linie.mutare_valida):
                                pygame.time.wait(2000)
                                tabla.scoatePiesaDinBaraMijloc(linie)
                    else:
                        # se selecteaza prima linie care are o piesa a jucatorului
                        for linie in tabla.linii:
                            if (linie.activa):
                                linie.clic()
                                break
                        mutata = False
                        for linie_destinatie in tabla.linii:
                            if linie_destinatie.mutare_valida:
                                pygame.time.wait(2000)
                                linie_destinatie.clicLinie()
                                mutata = True
                                break
                        if mutata:
                            linie.scoateSelectia()
                        else: # nu s-a efectuat mutarea, se scoate linia ca fiind activa
                            linie.activa = False
                            linie.jucator = 2 # se marcheaza linia ca nefiind a jucatorului
                            linie.scoateSelectia()
                            linie.setActiv(NEGRU, False)
                # reafiseaza tabela
                tabla.afiseaza_tabla()
            # refacere informatii linii
            for i in range(len(tabla.linii)):
                tabla.linii[i].update()
    if tabla.joc_castigat():
        intrebare = True
        din_nou = False
        while intrebare:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if tabla.btn_rejoaca_1.verifica_mouse(event.pos):
                       din_nou = True
                       intrebare = False
                    if tabla.btn_rejoaca_2.verifica_mouse(event.pos):
                       din_nou = False
                       intrebare = False
        if din_nou:
            tabla = joc.Tabla(fereastra)
            app_activa = True
        else:
            app_activa = False
