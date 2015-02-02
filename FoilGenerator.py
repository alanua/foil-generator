import sys
sys.path.append("../airconicsv021")
import primitives, airconics_setup
import rhinoscriptsyntax as rs

class CurveSplit:

    def __init__(self,_leadingEdgeCurve,_trailingEdgeCurve,_numberOfDivisions):
        self.leadingEdgeCurve = _leadingEdgeCurve
        self.trailingEdgeCurve = _trailingEdgeCurve
        self.numberOfDivisions = _numberOfDivisions

    def GetPoints(self,curve):
        curveDomain = rs.CurveDomain(curve)
        minDomainValue = curveDomain[0]
        maxDomainValue = curveDomain[1]

        points = []

        for i in range (0,self.numberOfDivisions+1):
            param = (maxDomainValue-minDomainValue)/self.numberOfDivisions * i
            pt = rs.EvaluateCurve(curve,param)
            points.append(pt)
            #rs.AddPoint(pt)
        return points

    def GetPointsOnSecondCurve(self,trailingEdgeCurve, pointsOnFirstCurve):

        TrailingEdgePoints = []

        for i in range (0,len(pointsOnFirstCurve)):
            # draw a line from the point on the first curve
            startingPoint = pointsOnFirstCurve[i]
            endPoint = (100,startingPoint[1],startingPoint[2])
            tmpLine = rs.AddLine(startingPoint,endPoint)

            # get the point where the new line and the traling edge curve is
            intersection_list = rs.CurveCurveIntersection(trailingEdgeCurve, tmpLine)
            if intersection_list is None:
                print "Selected curves do not intersect."
                return
            for intersection in intersection_list:
                if intersection[0] == 1:
                    print intersection[1]
                    #rs.AddPoint(intersection[1])

                    TrailingEdgePoints.append(intersection[1])

            rs.DeleteObject(tmpLine)
        return TrailingEdgePoints

    def AerofoilAtPoint(self,leadingEdgePoint,trailingEdgePoint):

        LEPoint = (leadingEdgePoint[0],leadingEdgePoint[1],leadingEdgePoint[2])
        ChordLength = abs(leadingEdgePoint[0] - trailingEdgePoint[0])

        # TODO: Work out how to set twist and dihedral at the given section

        Rotation = 0
        Twist = 0


        # Instantiate class to set up a generic airfoil with these basic parameters
        Af = primitives.Airfoil(LEPoint,ChordLength, Rotation, Twist, airconics_setup.SeligPath)

        # Name of the file containing the airfoil coordinates + smoothing
        AirfoilSeligName = 'dae11'
        SmoothingPasses = 1

        # Add airfoil curve to document, and retrieve handles to it and its chord
        #AfCurve,Chrd = primitives.Airfoil.AddAirfoilFromSeligFile(Af, AirfoilSeligName, SmoothingPasses)
        return primitives.Airfoil.AddAirfoilFromSeligFile(Af, AirfoilSeligName, SmoothingPasses)


leCurve = rs.GetObject("Select the leading edge curve")
if leCurve is not None:
    teCurve = rs.GetObject("Select the trailing edge curve")

    if teCurve is not None:
        if rs.IsCurve(leCurve):

            obj = CurveSplit(leCurve,teCurve,10)
            lePoints = obj.GetPoints(leCurve)
            tePoints = obj.GetPointsOnSecondCurve(teCurve,lePoints)

    print "leading"
    print lePoints

    print"Trailing"
    print tePoints

    Sections = []

    for i in range (0,len(lePoints)):
        Airfoil, ChordLine = obj.AerofoilAtPoint(lePoints[i],tePoints[i])
        rs.DeleteObjects(ChordLine)
        list.append(Sections,Airfoil)
        #lss = rs.AddLoftSrf(Sections,)
    LS = rs.AddLoftSrf(Sections)
    rs.DeleteObjects(Sections)

    if LS==None:
            # Failed to fit loft surface. Try another fitting algorithm
        print "loft failed"
