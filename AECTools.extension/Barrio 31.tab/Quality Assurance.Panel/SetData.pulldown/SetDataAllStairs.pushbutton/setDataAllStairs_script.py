from pyrevit import revit, DB

__title__ = "Set Data in All Stairs"
__doc__ = "Sets data in all stairs in the model."

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
t = DB.Transaction(doc, 'Set Data in Stairs')

def get_element_phase(element, phase):
	r = element.LookupParameter(phase).AsValueString()
	return r

def project_information_info(doc,param):
	project_info_collector = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_ProjectInformation).ToElements()
	for p in project_info_collector:
		value = p.LookupParameter(param).AsString()
		return value
		


allStairs = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Stairs).WhereElementIsNotElementType().ToElements()
#Start Transaction
t.Start()

for s in allStairs:
	#barrio = project_information_info(doc,"Barrio")
	#s.LookupParameter("Barrio").Set(barrio)
	
	#sector = project_information_info(doc,"Sector")
	#s.LookupParameter("Sector").Set(sector)

	if get_element_phase(s, "Phase Created") == "Mejoramiento":
		etapa_d = s.LookupParameter("Etapa").Set("M")
		n_item = s.LookupParameter("Numero de Tarea A").Set("8.03")
		n_rubro = s.LookupParameter("Numero de Rubro").Set("8")
		rubro = s.LookupParameter("Rubro").Set("Escaleras")	

	elif get_element_phase(s, "Phase Created") == "Existente":
		if get_element_phase(s, "Phase Demolished") == "None":
			etapa_d = s.LookupParameter("Etapa").Set("E")
			n_item = s.LookupParameter("Numero de Tarea A").Set("8.08")
			n_rubro = s.LookupParameter("Numero de Rubro").Set("8")
			rubro = s.LookupParameter("Rubro").Set("Escaleras")
		elif get_element_phase(s, "Phase Demolished") == "Mejoramiento":
			etapa_d = s.LookupParameter("Etapa").Set("R")
			n_item = s.LookupParameter("Numero de Tarea A").Set("2.20")
			n_rubro = s.LookupParameter("Numero de Rubro").Set("2")
			rubro = s.LookupParameter("Rubro").Set("Demoliciones y Retiro")

		
		
t.Commit()