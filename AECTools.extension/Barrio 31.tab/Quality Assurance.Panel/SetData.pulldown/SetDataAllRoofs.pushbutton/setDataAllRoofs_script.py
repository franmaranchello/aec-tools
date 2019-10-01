from pyrevit import revit, DB

__title__ = "Set Data in All Roofs"
__doc__ = "Sets data in all roofs in the model"

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
t = DB.Transaction(doc, 'Occupancy Assignment')

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

allRoofs = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Roofs).WhereElementIsNotElementType().ToElements()

allSoffits = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_RoofSoffit).WhereElementIsNotElementType().ToElements()

#Start Transaction
t.Start()

for r in allRoofs:
	#barrio = project_information_info(doc,"Barrio")
	#r.LookupParameter("Barrio").Set(barrio)
	
	#sector = project_information_info(doc,"Sector")
	#r.LookupParameter("Sector").Set(sector)

	if get_element_phase(r, "Phase Created") == "Mejoramiento":
		etapa = r.LookupParameter("Etapa").Set("M")
		n_rubro = r.LookupParameter("Numero de Rubro").Set("")
		rubro = r.LookupParameter("Rubro").Set("")
		rubro = r.LookupParameter("Numero de Tarea A").Set("")
		if r.Name == "0-M-006-010-Cubierta Nueva de Chapa":
			n_rubro = r.LookupParameter("Numero de Rubro").Set("18")
			rubro = r.LookupParameter("Rubro").Set("Cubiertas")
			rubro = r.LookupParameter("Numero de Tarea A").Set("18.03")
	elif get_element_phase(r, "Phase Demolished") == "Mejoramiento":
		etapa = r.LookupParameter("Etapa").Set("D")
		if r.Name == "0-E-006-010-Cubierta de Chapa":
			n_rubro = r.LookupParameter("Numero de Rubro").Set("2")
			rubro = r.LookupParameter("Rubro").Set("Demoliciones y Retiro")
			rubro = r.LookupParameter("Numero de Tarea A").Set("2.09")
	else:
		etapa = r.LookupParameter("Etapa").Set("E")
		n_rubro = r.LookupParameter("Numero de Rubro").Set("")
		rubro = r.LookupParameter("Rubro").Set("")
		rubro = r.LookupParameter("Numero de Tarea A").Set("")

for r in allSoffits:
	#barrio = project_information_info(doc,"Barrio")
	#r.LookupParameter("Barrio").Set(barrio)
	
	#sector = project_information_info(doc,"Sector")
	#r.LookupParameter("Sector").Set(sector)

	if get_element_phase(r, "Phase Created") == "Mejoramiento":
		etapa = r.LookupParameter("Etapa").Set("M")
		n_rubro = r.LookupParameter("Numero de Rubro").Set("16")
		rubro = r.LookupParameter("Rubro").Set("Cielorrasos")
		rubro = r.LookupParameter("Numero de Tarea A").Set("16.04")
	else:
		pass

t.Commit()		