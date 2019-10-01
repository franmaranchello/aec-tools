from pyrevit import revit, DB

__title__ = "Replace Windows"
__doc__ = "Replace Demolished Windows"

#Tool Works if Walls are selected.
__context__= "Windows"

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


lst = list()
#Select elements from revit.
elements = [doc.GetElement(x) for x in uidoc.Selection.GetElementIds()]
if isinstance(elements, list):
	lst = elements
else:
	lst.append(elements)

#Vars
phase_created = "Phase Created"
phase_demolished = "Phase Demolished"
mejoramiento = "Mejoramiento"
existente = "Existente"
none = "None"
retiro = "Retiro"
new_elements = list()

def str_contains(given_string,cont):
	if cont in given_string:
		return True
	else:
		return False

def do_iterable(elements, lst):
	if isinstance(elements, list):
		lst = elements
	else:
		lst.append(elements)

def get_element_phase(element, phase):
	r = element.LookupParameter(phase).AsValueString()
	return r

def get_phase_id_by_name(phase_name):
	phase_collector = DB.FilteredElementCollector(doc).OfClass(DB.Phase)
	for phase in phase_collector:
 		if phase.Name==phase_name:
  			return phase.Id

def set_element_phase(element, phase, value):
	r = element.LookupParameter(phase).Set(value)
	return r

def check_toogle_param(elem,param):
	p = elem.LookupParameter(param).AsValueString()
	if p == "No":
		return True
	else:
		return False

def all_win_types(document):
	#Wall types collector:
	win_types = DB.FilteredElementCollector(document).OfCategory(DB.BuiltInCategory.OST_Windows).WhereElementIsElementType().ToElements()

def change_win_type(element, typename):
	all_dt = all_win_types()
	for dt in all_dt:
 		if dt.Name==typename:
  			element.ChangeTypeId(dt.Id)
  		else:
  			pass

def get_choice(element):

	#If existing win contains Bars
	bars = str_contains(element.Name, "004-01")
	#Get Height
	height = element.LookupParameter("Height").AsDouble()
	#Get Width
	width = element.LookupParameter("Width").AsDouble()

#Start Transaction
with revit.Transaction('Repleace Windoes'):

	#Set Phase Demolished
	for s in lst:
		element_phase_created = get_element_phase(s,phase_created)
		
		#Check Element Phase Created
		if element_phase_created == existente:
			value = get_phase_id_by_name(mejoramiento)
			set_elem_phase = set_element_phase(s,phase_demolished,value)
			
			#Check Retiro
			check = check_toogle_param(s,retiro)
			if check:
				s.LookupParameter(retiro).Set(1)
			else:
				pass
			

			#For copy Win or Windows. 
			#WHY NEED TO MOVE 0.1 TO SEE?
			direction = DB.XYZ(0,0,0)

			#Id of New win or Win.
			id = DB.ElementTransformUtils.CopyElement(doc,s.Id,direction)
	 	
	 		#New Wall
	 		n_elem = doc.GetElement(id[0])
		
			#Append new walls in new list.
			new_elements.append(n_elem)

			
		else:
			pass

		#nn = get_phase_id_by_name(none)
		typename = "003-010-Ve08 1.60x1.10 Con Reja"
		for n in new_elements:
			gcc=typename
			x = set_element_phase(n, phase_created,value)
			win_types = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Windows).WhereElementIsElementType().ToElements()
			for win in win_types:
				if win.LookupParameter("Type Name").AsString() == typename:
	  				n.ChangeTypeId(win.Id)
	  		
