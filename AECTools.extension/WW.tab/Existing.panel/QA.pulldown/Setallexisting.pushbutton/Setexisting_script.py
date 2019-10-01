__title__ = "Set all to existing"
__doc__ = "Moves everything to existing phase"

import clr

import math
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from pyrevit import revit, DB, UI
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.UI import *
from System import *

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
selection = list(__revit__.ActiveUIDocument.Selection.Elements)
uidoc = __revit__.ActiveUIDocument
selection = __revit__.ActiveUIDocument.Selection.Elements


#methods
def cleanReferencePlane():
    # grab all reference planes
    rpInstancesFilter = ElementClassFilter(clr.GetClrType(ReferencePlane))
    collector = FilteredElementCollector(doc)
    rPlaneId = collector.WherePasses(rpInstancesFilter).ToElementIds()
    # go through ids delete unnamed ones.
    for id in rPlaneId:
        s = doc.get_Element(id).Name
        if s.Equals("Reference Plane", StringComparison.Ordinal):
            doc.Delete(id)
def cleanSection():
    print ("to be done...")
#define a transaction variable and describe the transaction
t = Transaction(doc,'Clean Section ReferencePlane')

#start a transaction in the Revit database
t.Start()

#************ ADD YOUR OWN CODES HERE.******************
#get all filled regions

y=int(raw_input("clean sections and reference planes: 1.clean both 2.clean sections 3. clean reference planes: "))
if y==1:
    print "clean sections and reference planes..."
    cleanReferencePlane()
    cleanSection()
elif y==2:
    print "clean sections only..."
    cleanSection()
elif y==3:
    print "clean reference plane only..."
    cleanReferencePlane()
   


print "end"
   

#commit the transaction to the Revit database
t.Commit()

#close the script window
raw_input("Enter to Quit.....")
#__window__.Hide()
__window__.Close()
#__window__.Show()