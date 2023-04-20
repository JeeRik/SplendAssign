import math

import cairo
from constants import *
from enum import Enum

# COST_FONT_NAME = "DynaPuff"


class TokenColors(Enum):
    WHITE = ("w", (1.0, 1.0, 1.0), (0.4, 0.3, 0.2))
    BLUE = ("b", (0.2, 0.3, 0.9), (0.0, 0.0, 0.2), (0.8, 0.9, 1.0))
    GREEN = ("g", (0.3, 0.9, 0.2), (0.1, 0.3, 0.1), (0.05, 0.1, 0.0), )
    RED = ("r", (0.8, 0.3, 0.2), (0.3, 0.15, 0.1), (0.1, 0.05, 0.0))
    BLACK = ("u", (0.2, 0.15, 0.1), (0, 0, 0), (0.8, 0.8, 0.8))

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, letter, primary, shadow, text=(0, 0, 0)):
        self._primary = primary
        self._letter = letter
        self._shadow = shadow
        self._text = text

    @property
    def value(self):
        return self._value_

    @property
    def primary(self):
        return self._primary

    @property
    def shadow(self):
        return self._shadow

    @property
    def text(self):
        return self._text

    @property
    def letter(self):
        return self._letter


class CardData:
    color: TokenColors
    value: int
    level: int
    cost = (0, 0, 0, 0, 0)

    def __init__(self, level, color, value, cost):
        self.color = color
        self.value = value
        self.cost = cost
        self.level = level

    def __str__(self):
        return f"L{self.level} P{self.value} letter={self.color.letter} color={self.color} cost={self.cost}"


class NobleData:
    id: int
    value: int
    cost = (0, 0, 0, 0, 0)

    def __init__(self, index, value, cost):
        self.index = index
        self.value = value
        self.cost = cost

    def __str__(self):
        return f"{self.index}: V{self.value} C{self.cost}"


def addImage(path, width=WIDTH, height=HEIGHT):
    with cairo.ImageSurface.create_from_png(path) as photo:
        context.save()
        xScale = (1.0*width) / photo.get_width()
        yScale = height / photo.get_height()
        context.scale(xScale, yScale)
        context.set_source_surface(photo, 0, 0)
        context.paint()
        context.restore()


def costCircle(x, y, text, colorScheme, r=45):
    color = colorScheme.primary
    stop = colorScheme.shadow
    fontColor = colorScheme.text
    highlightColor=(0.1 ,0.1 ,0)

    gradient = cairo.RadialGradient(x, y, r+5, x, y, r)
    gradient.add_color_stop_rgba(0, *highlightColor, 0.0)
    gradient.add_color_stop_rgba(1, *highlightColor, 0.6)
    context.set_source(gradient)
    context.arc(x, y, r+5, 0, 2 * 3.14)
    context.fill()

    context.set_source_rgb(*highlightColor)
    context.arc(x, y, r+1.5, 0, 2 * 3.14)
    context.fill()

    context.set_source_rgba(*color, 1)
    context.arc(x, y, r, 0, 2 * 3.14)
    context.fill()

    gradient = cairo.RadialGradient(x-20, y-30, 4, x, y, r)
    gradient.add_color_stop_rgba(0, *color, 0.0)
    gradient.add_color_stop_rgba(1, *stop, 0.8)
    context.set_source(gradient)
    context.arc(x, y, r, 0, 2 * 3.14)
    context.fill()

    context.set_source_rgb(*fontColor)

    context.set_font_size(r*1.25)
    context.select_font_face(FONT_NAME, cairo.FONT_SLANT_NORMAL,
                             cairo.FONT_WEIGHT_BOLD)
    (a, b, w, h, c, d) = context.text_extents(text)
    shadowColor = [(a+b)/2.0 for a, b in zip(color, fontColor)]
    context.move_to(x-w/2-(0 if text == '1' else 0), y+h/2+1)
    context.set_source_rgb(*shadowColor)
    context.show_text(text)
    context.move_to(x-w/2-(2 if text == '1' else 2), y+h/2-1)
    context.set_source_rgb(*fontColor)
    context.show_text(text)


def printCosts(costs, y=580):
    offset = 120
    for cost, color in zip(costs, list(TokenColors)):
        if cost > 0:
            costCircle(offset, y, str(cost), color)
            offset += 100

        # if costs[1] > 0: costCircle(220, y, str(costs[1]), TokenColors.BLUE)
        # if costs[2] > 0: costCircle(320, y, str(costs[2]), TokenColors.GREEN)
        # if costs[3] > 0: costCircle(420, y, str(costs[3]), TokenColors.RED)
        # if costs[4] > 0: costCircle(520, y, str(costs[4]), TokenColors.BLACK)


def printValue(value, color=None):
    r = 600
    sy = 0.4
    cx = MARGIN
    cy = MARGIN / sy

    if color is not None:
        color = [a/2 for a in color.primary]

        gradient = cairo.RadialGradient(cx, cy, r, cx, cy, 0)
        gradient.add_color_stop_rgba(0, *color, 0.0)
        gradient.add_color_stop_rgba(0.6, *color, 0.8)
        gradient.add_color_stop_rgba(1, *color, 1)
        context.save()
        context.scale(1, sy)
        context.set_source(gradient)
        context.arc(cx, cy, r, 0, 2 * 3.14)
        context.fill()
        context.restore()

    if value == 0:
        return

    text = str(value)
    x = 125
    y = 135
    context.set_font_size(160)
    context.select_font_face(FONT_NAME, cairo.FONT_SLANT_NORMAL,
                             cairo.FONT_WEIGHT_BOLD)
    (a, b, w, h, c, d) = context.text_extents(text)
    # shadowColor = [(a+b)/2.0 for a, b in zip(color, (1, 1, 1))]
    shadowColor = (0.8, 0.7, 0.7)

    for xs, ys in [(-2, -2), (-2, 2), (5, 2), (2, -2)]:
        context.move_to(x-w/2+xs, y+h/2+ys)
        context.set_source_rgba(*shadowColor, 1)
        context.show_text(text)
        context.save()

    context.move_to(x-w/2, y+h/2)
    context.set_source_rgb(0, 0, 0)
    context.show_text(text)


def printHeaders(value, color):
    printValue(value, color)
    offset = 145
    costCircle(WIDTH-offset, offset, "", color, 70)


def printCard(image, cost, value, color):
    global context
    context = cairo.Context(surface)
    addImage(image)
    printCosts(cost)
    printHeaders(value, color)

    surface.show_page()


def printCardData(data: CardData):
    print(f"Printing {data}")
    printCard(f"img/{data.color.letter}{data.level}.png", data.cost, data.value, data.color)


def costRectangle(x, y, text, colorScheme, w=150, h=110, fontSize=90):
    r = math.sqrt(w*w+h*h)
    x -= w/2
    y -= h/2
    color = colorScheme.primary
    stop = colorScheme.shadow
    fontColor = colorScheme.text
    highlightColor=(0.1 ,0.1 ,0)

    m = 5
    context.set_source_rgba(*colorScheme.shadow, 0.2)
    context.rectangle(x-m, y-m, w+m*2, h+m*2)
    context.fill()

    m = 4
    context.set_source_rgba(*colorScheme.shadow, 0.2)
    context.rectangle(x-m, y-m, w+m*2, h+m*2)
    context.fill()

    m = 3
    context.set_source_rgba(*colorScheme.shadow, 0.2)
    context.rectangle(x-m, y-m, w+m*2, h+m*2)
    context.fill()

    m = 0
    context.set_source_rgba(*colorScheme.primary, 1)
    context.rectangle(x-m, y-m, w+m*2, h+m*2)
    context.fill()

    m = 0
    gradient = cairo.RadialGradient(x+w-20, y+h-30, 4, x+w-20, y+h-30, r)
    gradient.add_color_stop_rgba(0, *color, 0.0)
    gradient.add_color_stop_rgba(1, *stop, 1)
    context.set_source(gradient)
    context.rectangle(x-m, y-m, w+m*2, h+m*2)
    context.fill()
    context.save()

    context.translate(x+w/2, y+h/2)
    context.rotate(math.pi/2)

    context.set_source_rgb(*fontColor)

    context.set_font_size(fontSize)
    context.select_font_face(FONT_NAME, cairo.FONT_SLANT_NORMAL,
                             cairo.FONT_WEIGHT_BOLD)
    (a, b, tw, th, c, d) = context.text_extents(text)
    shadowColor = [(a+b)/2.0 for a, b in zip(color, fontColor)]
    context.move_to(-(tw/2), (tw/2)+2)
    context.set_source_rgb(*shadowColor)
    context.show_text(text)
    context.move_to(-(tw/2)-2, (tw/2))
    context.set_source_rgb(*fontColor)
    context.show_text(text)
    context.restore()


def printNobleCost(cost):
    cnt = sum(1 for c in cost if c > 0)

    cx = 180
    cy = HEIGHT/2
    sy = 150
    sx = 200

    positions = {
        2: ((cx, cy-sy/2), (cx, cy+sy/2)),
        3: ((cx, cy-sy), (cx, cy), (cx, cy+sy)),
        5: ((cx+sx, cy-sy/2), (cx+sx, cy+sy/2), (cx, cy-sy), (cx, cy), (cx, cy+sy))
    }

    cv = zip(list(TokenColors), cost)
    cv = [v for v in cv if v[1] > 0]

    for data, pos in zip(cv, positions[cnt]):
        color = data[0]
        value = data[1]
        costRectangle(*pos, str(value), color)


def printNobleValue(value):
    context.save()
    context.translate(WIDTH, 0)
    context.rotate(math.pi/2)
    printValue(value)
    context.restore()


def printNoble(data: NobleData):
    print(f"Printing noble {data}")
    global context
    context = cairo.Context(surface)
    image = f"img/xichty/{data.index}.png"

    with cairo.ImageSurface.create_from_png(image) as photo:
        context.save()
        xScale = (1.0*WIDTH) / photo.get_width()
        yScale = HEIGHT / photo.get_height()
        context.scale(xScale, yScale)
        context.set_source_surface(photo, 0, 0)
        context.paint()
        context.restore()

    printNobleCost(data.cost)
    printNobleValue(data.value)
    surface.show_page()


def printBack(image):
    global context
    context = cairo.Context(surface)
    addImage(image)

    text = "SplendAssign"
    x = WIDTH/2
    y = HEIGHT-150
    context.set_font_size(100)
    context.select_font_face(FONT_NAME, cairo.FONT_SLANT_NORMAL,
                             cairo.FONT_WEIGHT_BOLD)
    (a, b, w, h, c, d) = context.text_extents(text)
    shadowColor = (0.8, 0.7, 0.7)

    for xs, ys in [(-2, -2), (-2, 2), (26, 2), (2, -2)]:
        context.move_to(x-w/2+xs, y+h/2+ys)
        context.set_source_rgba(*shadowColor, 1)
        context.show_text(text)

    context.move_to(x-w/2, y+h/2)
    context.set_source_rgb(0, 0, 0)
    context.show_text(text)
    context.rotate(math.pi/2)
    surface.show_page()


def setSurface(srf):
    global surface
    surface = srf


context = None

if __name__ == "__main__":

    surface = cairo.PDFSurface("pdffile.pdf", WIDTH, HEIGHT)
    context = cairo.Context(surface)

    printCard("Eventy/4.png", [1, 2,3,4,5], 1, TokenColors.WHITE)
    printCard("Eventy/2.png", [1, 2,3,4,5], 2, TokenColors.BLUE)
    printCard("Eventy/5.png", [1, 2,3,4,5], 3, TokenColors.GREEN)
    printCard("Eventy/1.png", [1, 2,3,4,5], 4, TokenColors.RED)
    printCard("Eventy/3.png", [1, 2,3,4,5], 5, TokenColors.BLACK)


__all__ = ['TokenColors', 'CardData', 'NobleData', 'printCard', 'printCardData', 'printBack', 'printNoble', 'setSurface']
