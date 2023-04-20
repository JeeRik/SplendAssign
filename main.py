from cards import *
from constants import *
from importData import *
import cairo


def cards():
    for lvl in [1, 2, 3]:
        surface = cairo.PDFSurface(f"level{lvl}.pdf", WIDTH, HEIGHT)
        setSurface(surface)
        cardData = importFile(f"t{lvl}cards.csv")

        for data in cardData:
            printCardData(data)
        printBack(f"img/{lvl}.png")


def backs():
    surface = cairo.PDFSurface(f"backs.pdf", WIDTH, HEIGHT)
    setSurface(surface)
    for lvl in range(4):
        printBack(f"img/{lvl}.png")


def nobles():
    surface = cairo.PDFSurface(f"nobles.pdf", WIDTH, HEIGHT)
    setSurface(surface)
    nobleData = importNobles(f"nobles.csv")

    for data in nobleData:
        printNoble(data)
    printBack(f"img/0.png")

cards()
nobles()