from constants import *
from cards import *

colorMap = {
    "Red": TokenColors.RED,
    "Green": TokenColors.GREEN,
    "Blue": TokenColors.BLUE,
    "White": TokenColors.WHITE,
    "Black": TokenColors.BLACK
}


def parseLine(line):
    chunks = line.split(',')
    if len(chunks) != 9:
        return None
    color = colorMap[chunks[2]]
    return CardData(int(chunks[0]), color, int(chunks[3]), [int(chunks[a]) for a in [8, 6, 5, 4, 7]])


def importFile(filename):
    with open(filename, 'r') as file:
        return [parseLine(line) for line in file]


def parseNoble(line, i):
    chunks = line.split(",")
    if len(chunks) != 7:
        return None
    return NobleData(i+1, int(chunks[1]), [int(chunks[a]) for a in [6, 4, 3, 2, 5]])


def importNobles(filename):
    with open(filename, 'r') as file:
        return [parseNoble(line, i) for line, i in zip(file, range(11))]


if __name__ == "__main__":
    importFile('t2cards.csv')

__all__ = ["importFile", "importNobles", "CardData"]