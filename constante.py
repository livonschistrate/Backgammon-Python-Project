# Tabla dimension constant3.4
ZOOM = 3

LATIME_TRIUNGHI = 22 # latimea unui triunghi de pe table de joc, pentru calcule ulterioare
INALTIME_TRIUNGHI = 90 # inaltimea unui triunghi de pe tabla de joc, pentru calcule ulterioare

LATIME_TABLA = ( 6 + 6 + 1 ) * LATIME_TRIUNGHI  # latimea tablei se calculeaza plecand de la latimea triunghiurilor (6 in stanga, 6 in dreapta + 1 pentru spatiul de la mijloc care este tot de latimea unui triunghi
INALTIME_TABLA =  INALTIME_TRIUNGHI * 2 + INALTIME_TRIUNGHI * 0.5   # inaltimea tablei se calculeaza plecand de la inaltimea triunghiurilor ( 2 ) la care se adauga 0.5 pentru spatiul dintre partea de sus si partea de jos la mijlocul tablei

MARGINE = 7 # marginea tablei de joc
MENIU = 80 # latimea meniului
SPATIU = 2 # spatiu liber intre tabla si elementele din jur

LATIME_FEREASTRA = (SPATIU + MENIU + SPATIU + LATIME_TABLA + MARGINE * 2 + SPATIU + LATIME_TRIUNGHI + SPATIU)
INALTIME_FEREASTRA = (SPATIU + INALTIME_TABLA + 2 * MARGINE + SPATIU)

RAZA_PIESA = 10 # raza unei piese
L_ZAR = LATIME_TRIUNGHI / 2
PUNCT_ZAR = 1
LATIME_MARKER = RAZA_PIESA * 0.4
INALTIME_MARKER = MARGINE * 0.8

# scalarea cu zoom
LATIME_TRIUNGHI = LATIME_TRIUNGHI * ZOOM
INALTIME_TRIUNGHI = INALTIME_TRIUNGHI * ZOOM
LATIME_TABLA = LATIME_TABLA * ZOOM
INALTIME_TABLA = INALTIME_TABLA * ZOOM
LATIME_FEREASTRA = LATIME_FEREASTRA * ZOOM
INALTIME_FEREASTRA = INALTIME_FEREASTRA * ZOOM
RAZA_PIESA = RAZA_PIESA * ZOOM
L_ZAR = L_ZAR * ZOOM
LATIME_MARKER = LATIME_MARKER * ZOOM
INALTIME_MARKER = INALTIME_MARKER * ZOOM
MARGINE = MARGINE * ZOOM
PUNCT_ZAR = PUNCT_ZAR * ZOOM
MENIU = MENIU * ZOOM
MIJLOC = (LATIME_FEREASTRA /2 , INALTIME_FEREASTRA / 2)
SPATIU = SPATIU * ZOOM

FONT = "Arial"

CULOARE_MARGINE = (115, 63, 25 )
GRI = ( 50, 50, 50 )
NEGRU = ( 30, 30, 30 )
PORTOCALIU = ( 255, 60, 0 )
VERDE = ( 0, 135, 32 )
GRI_DESCHIS = ( 200, 200, 200)
GRI_INCHIS = ( 60, 60, 60 )
FUNDAL = (199, 164, 74)
ALB = (255, 255, 255)
BEJ = (245, 245, 220)
