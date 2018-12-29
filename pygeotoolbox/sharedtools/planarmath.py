#  -*- coding: utf-8 -*-
###########################################################
#                                                         #
# Copyright (c) 2018 Radek Augustýn, licensed under MIT.  #
#                                                         #
###########################################################
__author__ = "radek.augustyn@email.cz"
# @PRODUCTION MODULE [Full]

from base import sqr
from math import sqrt, pi, cos, sin, atan2, fabs
import shapely.geometry


def normalizeAngle(value, limit = 2*pi):
    """ Returns normalized angle in interval (0, 2*Pi) or given value.

    :param float value: Value to be normalized.
    :param limit: Normalization high limit.
    :return: Value in interval (0, limit)

    >>> normalizeAngle(78.2)
    2.801776313844968

    """
    while value < 0: value = value + 2*pi
    if limit:
        while value >= limit: value = value - 2*pi

    return value


class Point:
    def __init__(self, x = 0, y = 0, point=None):
        """" Initialize planar point object on coordinates (x, y). if you want to initialize it by shapely point tuple, use the point parameter hook.

        >> p = Point(3, 4)
        >> print p
        Point(3, 4)
        >> shapelyPoint = (3, 4)
        >> Point(point=shapelyPoint
        Point(3, 4)
        """
        if point:
            x = point[0]
            y = point[1]

        self.x = float(x)
        self.y = float(y)


    def distance(self, point):
        """ Calculates planar distance to point.

        :param Point point: Object to calculate distance to.
        :return float: Planar distance between self and point.

        >>> a = Point(1, 1)
        >>> b = Point(6, 6)
        >>> a.distance(b)
        7.0710678118654755

        """
        return sqrt(sqr(point.x - self.x) + sqr(point.y - self.y))


    def __repr__(self):
        """ Returns string representation of the object.

        :return String: String representation of the point.

        >>> Point(3, 2)
        Point(3.000000, 2.000000)

        """
        return "Point(%f, %f)" % (self.x, self.y)


    def move(self, dx, dy):
        """ Moves point by given distances in each coordinate.

        :param float dx: Move distance in X axis.
        :param float dy: Move distance in Y axis.

        >>> a = Point(3, 5)
        >>> a.move(1, 2)
        >>> print a
        Point(4.000000, 7.000000)

        """
        self.x = self.x + dx
        self.y = self.y + dy


    def equals(self, point):
        return self.x == point.x and self.y == point.y


    @property
    def coords(self):
        return [[self.x, self.y]]


    @property
    def asShape(self):
        return shapely.geometry.Point(self.x, self.y)



def normalizePoint(point):
    if (isinstance(point, list) or isinstance(point, tuple)) and len(point) == 2:
        return Point(point=point)
    elif isinstance(point, Point):
        return point
    elif hasattr(point, 'x') and hasattr(point, 'y'):
        return Point(point.x, point.y)
    else:
        return point


class Vector:
    def __init__(self, startPoint, endPoint = None, length = None, direction = None):
        """ Initialize vector object.

        :param Point startPoint:
        :param Point endPoint:
        :param float length:
        :param float direction:

        >>> Vector(Point(3, 3), Point(5, 5))
        Vector(Point(3.000000, 3.000000), Point(5.000000, 5.000000))
        >>> Vector(Point(3, 3), length=1, direction=0)
        Vector(Point(3.000000, 3.000000), Point(4.000000, 3.000000))

        """
        if endPoint == None:
            endPoint = Point(startPoint.x + length*cos(direction), startPoint.y + length*sin(direction))

        self.startPoint = normalizePoint(startPoint)
        self._normalized = None
        self.endPoint = normalizePoint(endPoint)


    def __repr__(self):
        """ Returns string representation of the object.

        :return String: String representation of the point.
        >>> Vector(Point(3, 3), Point(5, 5))
        Vector(Point(3.000000, 3.000000), Point(5.000000, 5.000000))

        """
        return "Vector(%s, %s)" % (str(self.startPoint), str(self.endPoint))


    @property
    def normalized(self):
        if not self._normalized:
            self._normalized = Vector(self.startPoint, self.endPoint)
            self._normalized.normalize()
        return self._normalized


    def length(self):
        """ Calculates vector lenght.

        :return float: Length of the vector.

        >>> edge = Vector(Point(3, 3), Point(5, 5))
        >>> edge.length()
        2.8284271247461903

        """
        return self.endPoint.distance(self.startPoint)


    @property
    def coords(self):
        return [self.startPoint.coords[0], self.endPoint.coords[0]]


    def getDirection(self):
        """ Returns direction from the start point to the end point.

        :return float: Direction from the start point to the end point.

        >>> edge = Vector(Point(0, 0), Point(-1, 0))
        >>> edge.getDirection()
        3.141592653589793

        """
        from math import atan2
        return atan2(self.endPoint.y - self.startPoint.y, self.endPoint.x - self.startPoint.x)


    def normalize(self):
        """ Builds unit vector of the same direction starting from the origin.

        >>> edge = Vector(Point(10, 10), Point(50, 50))
        >>> edge.normalize()
        >>> print edge
        Vector(Point(0.000000, 0.000000), Point(0.707107, 0.707107))
        >>> print edge.length()
        1.0
        """
        len = self.length()
        if len:
            dx = (self.endPoint.x - self.startPoint.x)/len
            dy = (self.endPoint.y - self.startPoint.y)/len
            self.startPoint = Point(0, 0)
            self.endPoint = Point(dx, dy)


    def Interpolate_Point(self, t, normalized = True):
        """ Alias to the function calcPointOn.     """
        return self.calcPointOn(t, normalized)


    def calcPointOn(self, t, normalized = True):
        """ Returns a point interpolated along a line.

        :param float t: Distance or length fraction from the start point.
        :param boolean normalized: If normalised set to True, then second argument t is a float between 0 and 1 representing fraction of total length of linestring the point has to be located.
        If not, then t means length from the start point to the resulting point.
        :return Point: Interpolated point.

        >>> edge = Vector(Point(10, 10), Point(50, 50))
        >>> edge.calcPointOn(0.5, True)
        >>> edge.calcPointOn(0.5, True)
        Point(30.000000, 30.000000)

        """
        if normalized:
            t = t*self.length()

        x = self.startPoint.x + t*self.normalized.endPoint.x
        y = self.startPoint.y + t*self.normalized.endPoint.y

        return Point(x, y)


    def extent(self, targetLength):
        """ Adjust the vector so it's resulting length is as of targetLength parameter.

        :param float targetLength:

        >>> edge = Vector(Point(10, 10), Point(50, 50))
        >>> edge.extent(12)
        >>> print edge, edge.length()
        Vector(Point(10.000000, 10.000000), Point(18.485281, 18.485281)) 12.0

        """
        selfLength = self.length()
        if selfLength <> 0:
            scale = targetLength/selfLength
            dx = scale*(self.endPoint.x - self.startPoint.x)
            dy = scale*(self.endPoint.y - self.startPoint.y)
            self.endPoint = Point(self.startPoint.x + dx, self.startPoint.y + dy)


    @property
    def asShape(self):
        return shapely.geometry.LineString([self.startPoint.coords[0], self.endPoint.coords[0]])





def calcArea(vertexes):
    """

    :param vertexes:
    :return Float: Area of the polygon, Positive value means clockwise direction, negative counter-clockwise.

    >>> calcArea([Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)])
    -1.0

    >>> calcArea([Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)])
    1.0
    """
    if not vertexes[0].equals(vertexes[len(vertexes)-1]):
        vertexes.append(vertexes[0])

    prevVertex = None
    sum = 0
    for vertex in vertexes:
        if prevVertex:
            sum += (prevVertex.x*vertex.y-prevVertex.y*vertex.x)
        prevVertex = vertex

    return sum/2


def isLeft(a, b, c):
    return ((b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)) > 0;


def calcLineBearing(ax, ay, bx, by):
    """

    :param ax:
    :param ay:
    :param bx:
    :param by:
    :return:
    """

    result = atan2(ay - by, ax - bx)

    while result < 0:
        result = result + pi

    while result > pi:
        result = result - pi

    return result


def calcBearingsDifference(a, b):
    a = normalizeAngle(a, pi)
    b = normalizeAngle(b, pi)

    result = fabs(a - b)
    result = normalizeAngle(result, pi/2)

    return result


def constructPoint(point, bearing, lenght, vertical):
    """Constructs point by given parameters.

    :param point: Point for constructing line from.
    :param bearing: Bearing for calculation.
    :param lenght: Length of constructing vector.
    :param vertical: if True, then calculate vertial.
    :return: Point as shapely array [x, y]
    """
    if vertical:
        bearing = bearing + pi / 2

    return [point[0] + lenght * cos(bearing), point[1] + lenght * sin(bearing)]


def moveShapeCenterToIntersection(shape, stream):
    """ Centers shape element around stream element.

    :param shape: Shapely shape to be centered.
    :param stream: Shapely element as center line.
    :return: Moved shape element.
    """
    # Shapely library imports
    from shapely.affinity import translate
    center = shape.interpolate(0.5, normalized=True)
    newCenter = shape.intersection(stream)
    movedShape = translate(shape, newCenter.x-center.x, newCenter.y-center.y)

    return movedShape


def calcShapeBearingAt(shape, point):
    """Calculates bearing of the shape element at the spot nearest to the point.

    :param shape: Element to calculate bearing at.
    :param point: Point to calculate element spot for bearing.
    :return: Bearing at the projected sopt from point in radians.
    """
    from shapely.geometry import LineString

    if shape.type == "Polygon":
        return calcShapeBearingAt(shape.boundary, point)

    if hasattr(shape, "geoms"):
        for (geom, index) in zip(shape.geoms, range(len(shape.geoms))):
            distance = shape.distance(point)
            if distance < 0.1:
                return calcShapeBearingAt(geom, point)
    else:
        firstPoint = None
        minDistance = None
        streamBearing = None
        for coord in shape.coords:
            if firstPoint:
                secondPoint = coord
                distance = LineString([firstPoint, secondPoint]).distance(point)
                if not minDistance or distance < minDistance:
                    minDistance = distance
                    streamBearing = calcLineBearing(firstPoint[0], firstPoint[1], secondPoint[0], secondPoint[1])
                firstPoint = secondPoint
            else:
                firstPoint = coord
        return streamBearing