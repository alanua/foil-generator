import sys
import math
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

        # Get the minimim point
        minDomainValue = curveDomain[0]
        minPoint = rs.EvaluateCurve(curve,minDomainValue)

        # get the maximum point
        maxDomainValue = curveDomain[1]
        maxPoint = rs.EvaluateCurve(curve,maxDomainValue)

        yLength = abs(minPoint[1] - maxPoint[1])

        points = []

        for i in range (0,self.numberOfDivisions+1):
            print minPoint
            startingPoint = (minPoint[0],(yLength/self.numberOfDivisions)*i,minPoint[2])
            print startingPoint
            endPoint = (100,startingPoint[1],startingPoint[2])
            tmpLine = rs.AddLine(startingPoint,endPoint)


            # get the point where the new line and the traling edge curve is
            intersection_list = rs.CurveCurveIntersection(curve, tmpLine)
            if intersection_list is None:
                print "Selected curves do not intersect."
                return
            for intersection in intersection_list:
                if intersection[0] == 1:
                    print intersection[1]
                    #rs.AddPoint(intersection[1])
                points.append(intersection[1])
            rs.DeleteObject(tmpLine)
        return points

    def dihedralFunction(self,Epsilon):
        # This funtion sets the dihedral of the foil.
        # This allows for one single bend which starts at Transition1 and finishes at Transiiton2.
        # With the dihedral angles set as D1 and D2

        BaseDihedral = 0
        Dihedral = -0
        TransitionStart = 0.5
        TransitionEnd = 0.55

        if Epsilon < TransitionStart:
            return BaseDihedral
        elif Epsilon > TransitionEnd:
            return Dihedral
        else:
            return BaseDihedral + ((Epsilon - TransitionStart)/(TransitionEnd - TransitionStart))*(Dihedral-BaseDihedral)

    def washoutFunction(self,Epsilon):
        # This function lets you set a washout value for the foil.
        BaseTwist = 0
        Washout = 0
        WashoutStart = 0.70

        if Epsilon < WashoutStart:
            return BaseTwist
        else:
            return BaseTwist + ((Epsilon - WashoutStart)/(1 - WashoutStart))*(Washout-BaseTwist)

    def generateLeadingEdgeWithDihedral(self,originalLeadingEdgePoints, numberOfSegments):
        # Due to the fixed rotation that we have to draw in we can get the
        # length by subtracting coordinate values at each tip.
        # A more generic solution would be to get all 3 axies and use the max length
        # insted of hardcoding to the Y axis

        n = len(originalLeadingEdgePoints)-1

        YLength = originalLeadingEdgePoints[n][1] - originalLeadingEdgePoints[0][1]
        SegmentLength = YLength/numberOfSegments
        # Start the leading edge at the origin
        XLE = [0.0]
        YLE = [0.0]
        ZLE = [0.0]

        LEPoints = []
        list.append(LEPoints,([0, 0, 0]))
        previousDepth = 0.0
        pointZ = 0.0

        for i in range(1,numberOfSegments+1):
            TiltAngle = self.dihedralFunction(((i-1)/float(numberOfSegments)+i/float(numberOfSegments))/2)

            DeltaY = (originalLeadingEdgePoints[i][1] - originalLeadingEdgePoints[i-1][1])*math.cos(TiltAngle*math.pi/180.0)
            DeltaZ = (originalLeadingEdgePoints[i][1] - originalLeadingEdgePoints[i-1][1])*math.tan(TiltAngle*math.pi/180.0)

            pointX = originalLeadingEdgePoints[i-1][0]
            pointY = originalLeadingEdgePoints[i-1][1]
            pointZ = originalLeadingEdgePoints[i-1][2] + DeltaZ + previousDepth
            previousDepth = pointZ
            list.append(LEPoints,(pointX, pointY, pointZ))

        print LEPoints
        return LEPoints

    def _GenerateLeadingEdge(self):
        # Epsilon coordinate attached to leading edge defines sweep
        # Returns airfoil leading edge points

        # Start the leading edge at the origin
        XLE = [0.0]
        YLE = [0.0]
        ZLE = [0.0]

        SegmentLength = 1.0/self.SegmentNo

        LEPoints = []
        list.append(LEPoints,rs.AddPoint(XLE[0], YLE[0], ZLE[0]))


        for i in range(1,self.SegmentNo+1):
            # We are essentially reconstructing a curve from known slopes at
            # known curve length stations - a sort of Hermite interpolation without
            # knowing the ordinate values. If SegmentNo -> Inf, the actual slope
            # at each point -> the sweep angle specified by SweepFunct

            TiltAngle = self.DihedralFunct(((i-1)/float(self.SegmentNo)+i/float(self.SegmentNo))/2)
            SweepAngle = self.SweepFunct(((i-1)/float(self.SegmentNo)+i/float(self.SegmentNo))/2)

            DeltaX = SegmentLength*math.sin(SweepAngle*math.pi/180.0)
            DeltaY = SegmentLength*math.cos(TiltAngle*math.pi/180.0)*math.cos(SweepAngle*math.pi/180.0)
            DeltaZ = DeltaY*math.tan(TiltAngle*math.pi/180.0)

            list.append(XLE, XLE[i-1] + DeltaX)
            list.append(YLE, YLE[i-1] + DeltaY)
            list.append(ZLE, ZLE[i-1] + DeltaZ)

            list.append(LEPoints,rs.AddPoint(XLE[i], YLE[i], ZLE[i]))

        return LEPoints

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

    def AerofoilAtPoint(self,numberOfSegments, epsilon,leadingEdgePoint,chordLength):

        # Create a 3d point
        #LEPoint = (leadingEdgePoint[0],leadingEdgePoint[1],leadingEdgePoint[2])

        # Determine the twist for any washout
        Twist = self.washoutFunction(epsilon)


        ### Determine the dihedral at the given section

        # Start with the dihedral angle of the foil
        Angle = self.dihedralFunction(epsilon)

        # Create a 3d point
        #LEPoint = [0,0,0]

        LEPoint = (leadingEdgePoint[0],leadingEdgePoint[1],leadingEdgePoint[2])

        # Instantiate class to set up a generic airfoil with these basic parameters
        Af = primitives.Airfoil(LEPoint,chordLength, Angle , Twist , airconics_setup.SeligPath)

        # Name of the file containing the airfoil coordinates + smoothing
        AirfoilSeligName = 'dae11'
        SmoothingPasses = 1

        # Add airfoil curve to document, and retrieve handles to it and its chord
        #AfCurve,Chrd = primitives.Airfoil.AddAirfoilFromSeligFile(Af, AirfoilSeligName, SmoothingPasses)
        return primitives.Airfoil.AddAirfoilFromSeligFile(Af, AirfoilSeligName, SmoothingPasses)

NumberOfSegments = 20

leCurve = rs.GetObject("Select the leading edge curve")
if leCurve is not None:
    teCurve = rs.GetObject("Select the trailing edge curve")

    if teCurve is not None:
        if rs.IsCurve(leCurve):

            obj = CurveSplit(leCurve,teCurve,NumberOfSegments)
            lePoints = obj.GetPoints(leCurve)
            tePoints = obj.GetPointsOnSecondCurve(teCurve,lePoints)

            # Adjust the leading edge point locaiton based on the desired dihedral
            newLEPoints = obj.generateLeadingEdgeWithDihedral(lePoints, NumberOfSegments)


    Sections = []

    for i in range (0,len(lePoints)):
        epsilon = i/len(lePoints)
        print "Epsilon %.2f" % (epsilon)

        # Determine the length of the chord to generate
        chordLength = abs(lePoints[i][0] - tePoints[i][0])

        Airfoil, ChordLine = obj.AerofoilAtPoint(NumberOfSegments, epsilon, lePoints[i],chordLength)

        #Airfoil, ChordLine = obj.AerofoilAtPoint(NumberOfSegments, epsilon, newLEPoints[i],chordLength)
        rs.DeleteObjects(ChordLine)
        list.append(Sections,Airfoil)
        #lss = rs.AddLoftSrf(Sections,)
    LS = rs.AddLoftSrf(Sections)
    rs.DeleteObjects(Sections)

    if LS==None:
            # Failed to fit loft surface. Try another fitting algorithm
        print "loft failed"
