from pyrevit import revit, DB

__title__ = "Set Data in Walls"
__doc__ = "Set Data in Walls"

#Tool Works if Walls are selected.
__context__= "Walls"

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
t = DB.Transaction(doc, 'Set Data on Walls')

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

def set_by_level(element):
	level = element.LookupParameter("Base Constraint").AsValueString()
	if level == "Nivel 0":
		return 0
	elif level == "Nivel 1":
		return 1
	elif level == "Nivel 2":
		return 1
	elif level == "Nivel 3":
		return 2
	elif level == "Nivel 4":
		return 2
	elif level == "Nivel 5":
		return 2
	else:
		return 3

walls = list()
#Select elements from revit.
elements = [doc.GetElement(x) for x in uidoc.Selection.GetElementIds()]
if isinstance(elements, list):
	walls = elements
else:
	walls.append(elements)


t.Start()
for w in walls:
	wall_type = w.WallType.LookupParameter("Type Name").AsString()
	name = w.WallType.LookupParameter("Type Name").AsString()

	if ("MP") in name:
		w.LookupParameter("Rubro").Set("Mamposterias")
		w.LookupParameter("Numero de Rubro").Set("12")
		w.LookupParameter("Etapa").Set("C")
	if wall_type == "SILICONA SOBRE HORMIGON O LADRILLO VISTO":
		w.LookupParameter("Rubro").Set("Pinturas")
		w.LookupParameter("Numero de Rubro").Set("17")
		w.LookupParameter("Etapa").Set("M")
		#value_A = w.LookupParameter("Numero de Tarea A").Set("17.05")

	elif ("PARAPETOS") in name:
		w.LookupParameter("Rubro").Set("Mamposterias")
		w.LookupParameter("Numero de Rubro").Set("12")
		w.LookupParameter("Etapa").Set("C")
       
	elif "0-E" in name:
		if get_element_phase(w, "Phase Demolished") == "None":
		    w.LookupParameter("Etapa").Set("E")

		if wall_type == "0-E-110-Ladrillo visto":
			#w.LookupParameter("Rubro").Set("Pinturas")
			#w.LookupParameter("Numero de Rubro").Set("17")
			w.LookupParameter("Etapa").Set("E")
			#value_A = w.LookupParameter("Numero de Tarea A").Set("17.05")

		elif get_element_phase(w, "Phase Demolished") == "Mejoramiento":
			w.LookupParameter("Etapa").Set("D")
			w.LookupParameter("Rubro").Set("Demoliciones y Retiro")
			w.LookupParameter("Numero de Rubro").Set("2")
			value_A = w.LookupParameter("Numero de Tarea A").Set("2.03")

	elif ("0-E" or "MP" or "PARAPETOS") not in name:
		if get_element_phase(w, "Phase Created") == "Mejoramiento":
			w.LookupParameter("Etapa").Set("M")
			w.LookupParameter("Rubro").Set("Revoques")
			w.LookupParameter("Numero de Rubro").Set("13")

		elif wall_type == "MP 02-Mamposteria de ladrillo hueco 8x18x33":
			#value_A = w.LookupParameter("Numero de Tarea A").Set("12.04")
			w.LookupParameter("Etapa").Set("C")
				
		elif wall_type == "MP 03-Mamposteria de ladrillo hueco 12x18x33":
			#value_A = w.LookupParameter("Numero de Tarea A").Set("12.05")
			value_e = w.LookupParameter("Etapa").Set("C")

		elif wall_type == "MP 04-Mamposteria de ladrillo hueco 18x18x33":
			#value_A = w.LookupParameter("Numero de Tarea A").Set("12.06")
			 value_e = w.LookupParameter("Etapa").Set("C")

		elif wall_type == "PARAPETOS (h. 4m)":
			w.LookupParameter("Etapa").Set("C")
			#value_D = w.LookupParameter("Numero de Tarea D").Set("12.05")
			#value_A = w.LookupParameter("Numero de Tarea A").Set("13.01")
			#value_B = w.LookupParameter("Numero de Tarea B").Set("13.10")
			#value_C = w.LookupParameter("Numero de Tarea C").Set("11.05")
				
		elif wall_type == "PARAPETOS (desde 4.1m a 8m)":
			w.LookupParameter("Etapa").Set("C")
			#value_D = w.LookupParameter("Numero de Tarea D").Set("12.05")
			#value_A = w.LookupParameter("Numero de Tarea A").Set("13.02")
			#value_B = w.LookupParameter("Numero de Tarea B").Set("13.11")
			#value_C = w.LookupParameter("Numero de Tarea C").Set("11.06")

		elif wall_type == "PARAPETOS (a +8m)":
			w.LookupParameter("Etapa").Set("C")
			#value_D = w.LookupParameter("Numero de Tarea D").Set("12.05")
			#value_A = w.LookupParameter("Numero de Tarea A").Set("13.03")
			#value_B = w.LookupParameter("Numero de Tarea B").Set("13.12")
			#value_C = w.LookupParameter("Numero de Tarea C").Set("11.07")
			
		elif wall_type == "RECUADRE DE LOSAS,CORNISAS,VIGAS,COLUMNAS, MENSULAS":
			w.LookupParameter("Etapa").Set("M")
			#value_A = w.LookupParameter("Numero de Tarea A").Set("13.19")

	else:
		pass


t.Commit()




