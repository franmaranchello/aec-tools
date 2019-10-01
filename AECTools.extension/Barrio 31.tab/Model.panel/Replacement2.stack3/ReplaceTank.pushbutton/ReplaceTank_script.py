from pyrevit import revit,DB


__title__ = "Replace Tank"
__doc__ = "Replace and Demolish Tank"

#Tool Works if Walls are selected.
__context__= "Generic Models"

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
t= DB.Transaction(doc, "Replace Tank")

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
 		if phase.Name ==phase_name:
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

def all_gen_types(document):
	#Generic Model types collector:
	generic_types = DB.FilteredElementCollector(document).OfCategory(DB.BuiltInCategory.OST_GenericModel).WhereElementIsElementType().ToElements()

def change_gen_type(element, typename):
	all_gt = all_gen_types()
	for gt in all_st:
 		if gt.Name == typename:
  			element.ChangeTypeId(gt.Id)
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

		
		#For Stairs. 
		#WHY NEED TO MOVE 0.1 TO SEE?
		direction = DB.XYZ(0,0,6.3)

		collector =  DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_GenericModel).WhereElementIsElementType().ToElements()
		for c in collector:
			type_name = c.LookupParameter("Type Name").AsString()
			if  "012-000-Estructura Tanque" == type_name:
				symbol = c

		
		symbol.Activate()
		position = s.Location.Point

		newobj = revit.doc.Create.NewFamilyInstance(DB.XYZ(position.X,position.Y,position.Z),symbol, DB.Structure.StructuralType.NonStructural)
	

		#Id of New Tank.
		id = DB.ElementTransformUtils.CopyElement(doc,s.Id,direction)
 	
 		#New Tank
 		n_elem = doc.GetElement(id[0])
		#Append new walls in new list.
		new_elements.append(n_elem)

		
	else:
		pass

	#nn = get_phase_id_by_name(none)
	typename = "012-000-Tanque 600 lts"
	for n in new_elements:
		x = set_element_phase(n, phase_created,value)
		gen_types = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_GenericModel).WhereElementIsElementType().ToElements()
		for gen in gen_types:
			if gen.LookupParameter("Type Name").AsString() == typename:
  				n.ChangeTypeId(gen.Id)

	
t.Commit()