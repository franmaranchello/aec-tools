from pyrevit import revit, DB

__title__ = "Replace Railings"
__doc__ = "Replace Demolished Railings"

#Tool Works if Walls are selected.
__context__= "Railings"

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
t = DB.Transaction(doc, 'Replace Railings')


railings = list()
#Select elements from revit.
elements = [doc.GetElement(x) for x in uidoc.Selection.GetElementIds()]
if isinstance(elements, list):
	railings = elements
else:
	railings.append(elements)

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
 		if phase.Name==phase_name:
  			return phase.Id

def set_element_phase(element, phase, value):
	r = element.LookupParameter(phase).Set(value)
	return r


def project_information_info(doc,param):
	project_info_collector = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_ProjectInformation).ToElements()
	for p in project_info_collector:
		value = p.LookupParameter(param).AsString()
		return value
	

#Start Transaction
t.Start()

#Set Phase Demolished
for r in railings:
	
	#barrio = project_information_info(doc,"Barrio")
	#r.LookupParameter("Barrio").Set(barrio)
	
	#sector = project_information_info(doc,"Sector")
	#r.LookupParameter("Sector").Set(sector)



	element_phase_created = get_element_phase(r,phase_created)
	value = get_phase_id_by_name(mejoramiento)
	#Check Element Phase Created
	if element_phase_created == existente:
		if r.Name == "0-E-002-100-Baranda Existente":
			set_elem_phase = set_element_phase(r,phase_demolished,value)

		
		direction = DB.XYZ(0,0,0)
		#Id of New Railing.
		id = DB.ElementTransformUtils.CopyElement(doc,r.Id,direction)
		 	
 		#New Railing
 		n_elem = doc.GetElement(id[0])
		n_elem.LookupParameter("Etapa").Set("M")
		n_elem.LookupParameter("Numero de Tarea A").Set("10.01")
		n_elem.LookupParameter("Numero de Rubro").Set("10")
		n_elem.LookupParameter("Rubro").Set("Postigos, Barandas y Herrajes")
		r.LookupParameter("Etapa").Set("R")
		n_rubro = r.LookupParameter("Numero de Rubro").Set("2")
		rubro = r.LookupParameter("Rubro").Set("Demoliciones y Retiro")
		rubro = r.LookupParameter("Numero de Tarea A").Set("2.25")

		#Append new roofs in new list.
		new_elements.append(n_elem)

		
	else:
		pass

	typename = "0-M-007-100-Baranda Fa01"
	for n in new_elements:
		x = set_element_phase(n, phase_created,value)
		railing_types = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_StairsRailing).WhereElementIsElementType().ToElements()
		for railing in railing_types:
			try:
				if railing.LookupParameter("Type Name").AsString() == typename:
  					n.ChangeTypeId(railing.Id)
			except:
				pass
			
t.Commit()