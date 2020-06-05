import math


class Geometry(object):
    geoid = 0
    def __init__(self):
        self.id = self.geoid; self.__class__.geoid += 1
geo1 = Geometry()


class Point(Geometry):
    # Auto Increment a Unique ID for Point
    def __init__(self,x,y):
        Geometry.__init__(self)
        self.x = x
        self.y = y
    # Round to two decimal places
    def __repr__(self):
        return "{:.2f} {:.2f}".format(self.x,self.y)
    # Override equal method to check point x,y equality
    def __eq__(self, other):
        if self.x == other.x \
        and self.y == other.y:
            return True
        else:
            return False
    # Measure distance between two points
    def distance(self,other):
        x1 = self.x
        x2 = other.x
        y1 = self.y
        y2 = other.y
        distance = math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )
        return distance
    # Find which quadrant point lies in cartesian plane
    def quadrant(self):
        x = self.x
        y = self.y
        if x > 0 and y > 0:
            result = "Quad I"
        elif x < 0 and y > 0:
            result = "Quad II"
        elif x < 0 and y < 0:
            result = "Quad III"
        elif x > 0 and y < 0 :
            result = "Quad IV"
        elif x == 0:
            result = "Y-axis"
        elif y == 0:
            result = "X-axis"
        elif x == 0 and y == 0:
            result = "Origin"
        else:
            None
        return result

# Test Data
def pointTest():
    print "***Point Class Test***"
    p1 = Point(0,3)
    p2 = Point(-3,7)
    p3 = Point(-3,7)
    print "P1) ID = %d, Coords = %s, Location = %s" % (p1.id, p1, p1.quadrant())
    print "P2) ID = %d, Coords = %s, Location = %s" % (p2.id, p2, p2.quadrant())
    print "P3) ID = %d, Coords = %s, Location = %s" % (p3.id, p3, p3.quadrant())
    print "Distance between P1 and P2 = %.2f" % p1.distance(p2)
    print "Distance between P2 and P3 = %.2f" % p2.distance(p3)
    print "Distance between P1 and P3 = %.2f" % p1.distance(p3)
    print "P1 == P2?", p1 == p2
    print "P2 == P3?", p2 == p3
    print "P1 == P3?", p1 == p3
pointTest()