import math

# Task 1
class Geometry(object):
    # Task 1 Incrementing Geometry Class
    geoid = 0
    def __init__(self):
        self.id = self.geoid; self.__class__.geoid += 1
geo1 = Geometry()

# Task 2
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
            pass
        return result

# Task 3
def collinear(p1,p2,p3):
    # Calculate if points are collinear #
    m = (p1.y-p2.y)/(p1.x - p2.x)
    m2 = (p2.y - p3.y)/ (p2.x - p3.x)
    if m == m2:
        return True
    else:
        return False

# Task4
class Line(Geometry):
    # Task 3 
    # Auto Increment a Unique ID for Point
        
    def __init__(self,p1,p2):
        # Calculate slope and Intercept
        Geometry.__init__(self)
        self.p1 = p1
        self.p2 = p2
        m = (p2.y - p1.y)/ (p2.x - p1.x)
        self.m = m
        b = p1.y + (m*p1.x)
        self.b= b
    
    def __repr__(self):
        # Return string of Equation #
        return 'y = {:.2f} * x + {:.2f}'.format(self.m,self.b)
    
    def parallel(self,other):
        # Determine if slope is parallel #
        if self.m == other.m:
            result= True
        else:
            result = False
        return result


# Test Input
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


def linearTest():
    print "***Linearity Test***"
    p1 = Point(0,0)
    p2 = Point(1,1)
    p3 = Point(2,3)
    print p1, p2, p3
    print "Are P1, P2, and P3 on the same line?", collinear(p1,p2,p3)
    p4 = Point(0,0)
    p5 = Point(-1,-3)
    p6 = Point(-2,-6)
    print p4, p5, p6
    print "Are P4, P5, and P6 on the same line?", collinear(p4,p5,p6)

linearTest()


def lineTest():
    print "***Line Class Test***"
    p1 = Point(-1,-1)
    p2 = Point(1,1)
    p3 = Point(3,4)
    print p1, p2, p3
    line1 = Line(p1,p2)
    line2 = Line(p2,p3)
    print "L1) ID = %d, Equation = %s" % (line1.id, line1)
    print "L2) ID = %d, Equation = %s" % (line2.id, line2)
    print "Are L1 and L2 parallel?", line1.parallel(line2)

lineTest()