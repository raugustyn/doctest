#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


from pygeotoolbox.sharedtools.planarmath import Point


unknownKeys = []
pathElements = {
    'M': 'moveto',
    'L': 'lineto',
    'H': 'horizontal lineto',
    'V': 'vertical lineto',
    'C': 'curveto',
    'S': 'smooth curveto',
    'Q': 'quadratic Bézier curve',
    'T': 'smooth quadratic Bézier curveto',
    'A': 'elliptical Arc',
    'Z': 'closepath',
}
pathKeys = pathElements.keys()
for key in pathElements.keys():
    pathKeys.append(key.lower())


class PathShapeItem:
    def __init__(self, paramName, params, penPosition):
        """Reads paramName, creates vertex list and move penPosition."""
        relativePosition = paramName.islower()
        self.params = params
        self.relativePosition = relativePosition
        self.vertexes = []
        pathItemConvertors = {
            'M': self.MoveToPathItem,
            'L': self.LineToPathItem,
            'H': self.HorizontalLineToPathItem,
            'V': self.VerticalLineToPathItem,
            'Q': self.QuadraticBezierCurvePathItem,
            'T': self.SmoothQuadraticBezierCurvePathItem
        }

        if paramName.upper() in pathItemConvertors:
            self.vertexes = pathItemConvertors[paramName.upper()](params, relativePosition, penPosition)
        else:
            if not paramName in unknownKeys:
                import pygeotoolbox.sharedtools.log as log
                log.warning("\t\t!!! Warning " + paramName + " not found")
                unknownKeys.append(paramName)


    def MoveToPathItem(self, params, relativePosition, penPosition):
        dx = params[0]
        dy = params[1]
        if relativePosition:
            x = penPosition.x + dx
            y = penPosition.y + dy
        else:
            x = dx
            y = dy

        penPosition.x = x
        penPosition.y = y

        return [Point(x, y)]


    def LineToPathItem(self, params, relativePosition, penPosition):
        dx = params[0]
        dy = params[1]
        if relativePosition:
            x = penPosition.x + dx
            y = penPosition.y + dy
        else:
            x = dx
            y = dy

        penPosition.x = x
        penPosition.y = y

        return [Point(x, y)]


    def HorizontalLineToPathItem(self, params, relativePosition, penPosition):
        dx = params[0]
        if relativePosition:
            x = penPosition.x + dx
        else:
            x = dx

        penPosition.x = x
        return [Point(x, penPosition.y)]

    def VerticalLineToPathItem(self, params, relativePosition, penPosition):
        dy = params[0]
        if relativePosition:
            y = penPosition.y + dy
        else:
            y = dy

        penPosition.y = y
        return [Point(penPosition.x, y)]


    def QuadraticBezierCurvePathItem(self, params, relativePosition, penPosition):
        x1 = params[0]
        y1 = params[1]
        x = params[2]
        y = params[3]
        if relativePosition:
            x1 += penPosition.x
            y1 += penPosition.y
            x += penPosition.x
            y += penPosition.y

        penPosition.x = x
        penPosition.y = y

        return [Point(x, y)]


    def SmoothQuadraticBezierCurvePathItem(self, params, relativePosition, penPosition):
        x = params[0]
        y = params[1]
        if relativePosition:
            x += penPosition.x
            y += penPosition.y

        penPosition.x = x
        penPosition.y = y

        return [Point(x, y)]