from pyrevit import revit, DB

__title__ = "Set Data in All Railings"
__doc__ = "Sets data in all railings in the model."

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
t = DB.Transaction(doc, 'Set Data in Railings')

def get_element_phase(element, phase):
	r = element.LookupParameter(phase).AsValueString()
	return r

def project_information_info(doc,param):
	project_info_collector = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_ProjectInformation).ToElements()
	for p in project_info_collector:
		value = p.LookupParameter(param).AsString()
		return value



allRailings = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_StairsRailing).WhereElementIsNotElementType().ToElements()
#Start Transaction
t.Start()

for r in allRailings:
	etapa = r.LookupParameter("Etapa").Set("")
	tarea_A = r.LookupParameter("Numero de Tarea A").Set("")
	tarea_B = r.LookupParameter("Numero de Tarea B").Set("")
	n_rubro = r.LookupParameter("Numero de Rubro").Set("")
	rubro = r.LookupParameter("Rubro").Set("")

	if get_element_phase(r, "Phase Created") == "Mejoramiento":
		if r.Name == "0-M-007-100-Baranda Fa01":
			tarea_A = r.LookupParameter("Numero de Tarea A").Set("10.01")
			tarea_B = r.LookupParameter("Numero de Tarea B").Set("")
			n_rubro = r.LookupParameter("Numero de Rubro").Set("10")
			rubro = r.LookupParameter("Rubro").Set("Postigos, Barandas, Herrajes y Toldos")
			etapa = r.LookupParameter("Etapa").Set("M")	
		if r.Name == "0-M-002-100-Baranda Escalera":
			etapa = r.LookupParameter("Etapa").Set("M")	
			n_rubro = r.LookupParameter("Numero de Rubro").Set("")
			rubro = r.LookupParameter("Rubro").Set("")
			tarea_A = r.LookupParameter("Numero de Tarea A").Set("")
			tarea_B = r.LookupParameter("Numero de Tarea B").Set("")
		else:
			pass
		
	elif get_element_phase(r, "Phase Created") == "Existente":
		if r.Name == "0-E-002-100-Baranda Existente":
			if get_element_phase(r, "Phase Demolished") == "Mejoramiento":
				etapa = r.LookupParameter("Etapa").Set("R")
				tarea_A = r.LookupParameter("Numero de Tarea A").Set("2.25")
				tarea_B = r.LookupParameter("Numero de Tarea B").Set("")
				n_rubro = r.LookupParameter("Numero de Rubro").Set("2")
				rubro = r.LookupParameter("Rubro").Set("Demoliciones y Retiro")
			else: 
				etapa = r.LookupParameter("Etapa").Set("E")
				tarea_A = r.LookupParameter("Numero de Tarea A").Set("17.08")
				tarea_B = r.LookupParameter("Numero de Tarea B").Set("10.26")
				n_rubro = r.LookupParameter("Numero de Rubro").Set("")
				rubro = r.LookupParameter("Rubro").Set("")
		if r.Name == "0-E-002-100-Baranda Escalera":
			if get_element_phase(r, "Phase Demolished") == "None":
				etapa = r.LookupParameter("Etapa").Set("E")
				n_rubro = r.LookupParameter("Numero de Rubro").Set("")
				rubro = r.LookupParameter("Rubro").Set("")
				tarea_A = r.LookupParameter("Numero de Tarea A").Set("")
				tarea_B = r.LookupParameter("Numero de Tarea B").Set("")
			if get_element_phase(r, "Phase Demolished") == "Mejoramiento":
				etapa = r.LookupParameter("Etapa").Set("R")
				n_rubro = r.LookupParameter("Numero de Rubro").Set("")
				rubro = r.LookupParameter("Rubro").Set("")
				tarea_A = r.LookupParameter("Numero de Tarea A").Set("")
				tarea_B = r.LookupParameter("Numero de Tarea B").Set("")
		else:
			pass
				
t.Commit()