# Example script for generating a transonic airliner wing external geometry.
# ==============================================================================
# AirCONICS
# Aircraft CONfiguration through Integrated Cross-disciplinary Scripting
# version 0.2.0
# Andras Sobester, 2015.
# Bug reports to a.sobester@soton.ac.uk or @ASobester on Twitter please.
# ==============================================================================
from __future__ import division
import math
import primitives, airconics_setup, liftingsurface, AirCONICStools as act
import rhinoscriptsyntax as rs


#===============================================================================
# Transonic passanger airliner wing geometry example
# (planform similar to that of the Boeing 787 family)
#===============================================================================


def myDihedralFunctionAirliner(Epsilon):
    # User-defined function describing the variation of dihedral as a function
    # of the leading edge coordinate

    BaseDihedral = 7

    # A simple model of a loaded wing shape:
    return BaseDihedral + Epsilon*Epsilon*10

def myTwistFunctionAirliner(Epsilon):
    # User-defined function describing the variation of twist as a function
    # of the leading edge coordinate. The coefficients of the polynomial below
    # come from the following twist values taken off the CRM (used for the AIAA
    # drag prediction workshops):
    # Epsilon = 0: twist = 4.24
    # Epsilon =0.3: twist = 0.593
    # Epsilon = 1: twist = -3.343
    return -(6.53*Epsilon*Epsilon -14.1*Epsilon + 4.24)

def myChordFunctionAirliner(Epsilon):
    # User-defined function describing the variation of chord as a function of
    # the leading edge coordinate

    ChordLengths = [0.5, 0.3792, 0.2867, 0.232, 0.1763, 0.1393, 0.1155, 0.093,
    0.0713, 0.055, 0.007]

    EpsArray = []
    for i in range(0, 11):
        list.append(EpsArray, float(i)/10)
    f = act.linear_interpolation(EpsArray, ChordLengths)
    return f(Epsilon)

def myAirfoilFunctionAirliner(Epsilon, LEPoint, ChordFunct, ChordFactor, DihedralFunct, TwistFunct):
    # Defines the variation of cross section as a function of Epsilon

    AirfoilChordLength = (ChordFactor*ChordFunct(Epsilon))/math.cos(math.radians(TwistFunct(Epsilon)))

    Af = primitives.Airfoil(LEPoint, AirfoilChordLength, DihedralFunct(Epsilon), TwistFunct(Epsilon),
    airconics_setup.SeligPath)
    SmoothingPasses = 1
    #Airf, Chrd = primitives.Airfoil.AddCRMLinear(Af, Epsilon, SmoothingPasses)
    #Airf,Chrd = primitives.Airfoil.AddAirfoilFromSeligFile(Af, 'naca63a412', SmoothingPasses)
    Airf, Chrd = primitives.Airfoil.AddAirfoilFromSeligFile(Af, 'h105-11%', SmoothingPasses)
    #Airf,Chrd = primitives.Airfoil.AddNACA4(Af, 2, 2, 12, SmoothingPasses)
    return Airf, Chrd

def mySweepAngleFunctionAirliner(Epsilon):
    # User-defined function describing the variation of sweep angle as a function
    # of the leading edge coordinate

    SweepAngles = [90, 87, 35, 35, 35, 35, 35, 35, 35, 35, 80]

    EpsArray = []
    for i in range(0, 11):
        list.append(EpsArray, float(i)/10)
    f = act.linear_interpolation(EpsArray, SweepAngles)

    return f(Epsilon)


if __name__ == "__main__":

    # Position of the apex of the wing
    P = (0,0,0)

    # Class definition
    LooseSurf = 1
    SegmentNo = 10

    Wing = liftingsurface.LiftingSurface(P, mySweepAngleFunctionAirliner,
    myDihedralFunctionAirliner,
    myTwistFunctionAirliner,
    myChordFunctionAirliner,
    myAirfoilFunctionAirliner,
    LooseSurf, SegmentNo, TipRequired = True)

    # Instantiate the class
    ChordFactor = 1
    ScaleFactor = 50

    rs.EnableRedraw(False)
    WingSurf, ActualSemiSpan, LSP_area,  RootChord, AR, WingTip = Wing.GenerateLiftingSurface(ChordFactor, ScaleFactor)
    rs.EnableRedraw()
