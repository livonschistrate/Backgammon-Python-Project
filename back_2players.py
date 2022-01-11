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
