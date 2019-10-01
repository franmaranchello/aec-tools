from pyrevit import revit, DB

__title__ = "Replace Doors"
__doc__ = "Replace Demolished Doors"

#Tool Works if Walls are selected.
__context__= "Doors"

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
t = DB.Transaction(doc, 'Replace Doors')


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
 		if phase.Name == phase_name:
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

def all_door_types(document):
	#Wall types collector:
	door_types = DB.FilteredElementCollector(document).OfCategory(DB.BuiltInCategory.OST_Doors).WhereElementIsElementType().ToElements()

def change_door_type(element, typename):
	all_dt = all_door_types()
	for dt in all_dt:
 		if dt.Name.Equals(typename):
  			element.ChangeTypeId(dt.Id)
  		else:
  			pass
	
#Start Transaction
t.Start()

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
		

		#For copy Win or Doors. 
		#WHY NEED TO MOVE 0.1 TO SEE?
		direction = DB.XYZ(0,0,0)

		#Id of New Door or Win.
		id = DB.ElementTransformUtils.CopyElement(doc,s.Id,direction)
 	
 		#New Wall
 		n_elem = doc.GetElement(id[0])
	
		#Append new walls in new list.
		new_elements.append(n_elem)

		
	else:
		pass

	#nn = get_phase_id_by_name(none)
	typename = "002-000-Pu08 0.80 Con Reja"
	for n in new_elements:
		x = set_element_phase(n, phase_created,value)
		door_types = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Doors).WhereElementIsElementType().ToElements()
		for door in door_types:
			if door.LookupParameter("Type Name").AsString() == typename:
  				n.ChangeTypeId(door.Id)

t.Commit()	