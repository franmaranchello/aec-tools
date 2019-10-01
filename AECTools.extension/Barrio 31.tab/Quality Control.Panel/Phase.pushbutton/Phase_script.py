"""Provides options for overriding Visibility/Graphics on selected elements."""
#pylint: disable=E0401,C0103
import re
from collections import OrderedDict

from pyrevit import revit, DB, UI
from pyrevit import forms
from pyrevit import script

__title__ = "Phase"
__doc__ = "Check if elements have phase parameter loaded"

curview = revit.activeview

logger = script.get_logger()

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

def get_element_phase(element, phase):
	r = element.LookupParameter(phase).AsValueString()
	return r

def project_information_info(doc,param):
	project_info_collector = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_ProjectInformation).ToElements()
	for p in project_info_collector:
		value = p.LookupParameter(param).AsString()
		return value
		
def get_type(element):
	element.LookupParameter("Type Name").AsString()

selection= list()
selection2= list()

elements = DB.FilteredElementCollector(doc,doc.ActiveView.Id).ToElements()

for w in elements:
    try:
        a= w.LookupParameter("Etapa").AsString()
        if (a != None):
            selection2.append(w)
        else:
            selection.append(w)
    except:
        pass        

def set_transparency():
    with revit.Transaction('Halftone Elements in View'):
        for el in selection2:
            if isinstance(el, DB.Group):
                for mem in el.GetMemberIds():
                    selection2.append(revit.doc.GetElement(mem))
            ogs = DB.OverrideGraphicSettings()
            ogs.SetSurfaceTransparency(80)
            # ogs.SetProjectionFillPatternVisible(False)
            revit.doc.ActiveView.SetElementOverrides(el.Id, ogs)




def find_solid_fillpat():
    solid_fill_regex = re.compile('[<]?solid fill[>]?')
    existing_pats = DB.FilteredElementCollector(revit.doc)\
                      .OfClass(DB.FillPatternElement)\
                      .ToElements()
    for pat in existing_pats:
        fpat = pat.GetFillPattern()
        if solid_fill_regex.match(fpat.Name.lower()) \
                and fpat.Target == DB.FillPatternTarget.Drafting:
            return pat

   
def set_override():
    if isinstance(curview, DB.View3D):
        if len(selection)<1:
            forms.alert("No Elements to Review")
        else:
            if len(selection)== 1:
                forms.alert("1 Element to Review")
                set_transparency()
                mark_red()
               
            else:
                mark_red()
                set_transparency()
                forms.alert(str(len(selection))+" Elements to Review")

           
    else:
        forms.alert('You must be on a 3D view for this tool to work.')

def colorvg(r, g, b, projline_only=False, xacn_name=None):
    color = DB.Color(r, g, b)
    with revit.Transaction(xacn_name or 'Set Color VG override'):
        for el in selection:
            if isinstance(el, DB.Group):
                for mem in el.GetMemberIds():
                    selection.append(revit.doc.GetElement(mem))
            ogs = DB.OverrideGraphicSettings()
            ogs.SetProjectionLineColor(color)
            if not projline_only:
                ogs.SetProjectionFillColor(color)
                solid_fpattern = find_solid_fillpat()
                if solid_fpattern:
                    ogs.SetProjectionFillPatternId(solid_fpattern.Id)
                else:
                    logger.warning('Can not find solid fill pattern in model'
                                   'to assign as projection pattern.')
            revit.doc.ActiveView.SetElementOverrides(el.Id, ogs)

def reset_vg():
    with revit.Transaction('Reset Element Override'):
        for el in elements:
            ogs = DB.OverrideGraphicSettings()
            revit.doc.ActiveView.SetElementOverrides(el.Id, ogs)

def mark_red():
    # F7F303
    colorvg(0xf7, 0xf3, 0x03, xacn_name= 'Mark Selected with Yellow')

reset_vg()
set_override()




    
