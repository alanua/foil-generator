# airconics_setup.py Setup file: here you can specify top level system variables
# ==============================================================================
# AirCONICS
# Aircraft CONfiguration through Integrated Cross-disciplinary Scripting
# version 0.2.1
# Andras Sobester, 2015.
# Bug reports to a.sobester@soton.ac.uk or @ASobester please.
# ==============================================================================
import sys

# *** There are three entries to edit here ***

# ONE:
# The string below should contain the path to your installation of AirCONICS
# Example: AirCONICSpath = "C:/Users/as/Documents/airconicsv021/"

AirCONICSpath = "/Users/bruce/Desktop/airconicsv02122/"

# TWO:
# The string below should contain the path to your library of Selig-formatted
# airfoils. If you are using the UIUC library included in this installation,
# this should be the path to the coord_seligFmt folder included.

# Example: SeligPath = "C:/Users/as/Documents/airconicsv021/coord_seligFmt/"
SeligPath = "/Users/bruce/Desktop/airconicsv021/coord_seligFmt/"
BrucePath = "/Users/bruce/Desktop/airconicsv021/coord_seligFmt/"

# THREE:
# Set this to
#       1 if you are running Rhino for Windows and
#       2 if you are running the MacOS version
RhinoVersion = 2

# ==============================================================================
print "System variables initialised."
sys.path.append(AirCONICSpath)
