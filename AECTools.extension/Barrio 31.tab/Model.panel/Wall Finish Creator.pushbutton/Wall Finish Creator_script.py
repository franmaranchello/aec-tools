from pyrevit import revit, DB

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#Select elements from revit.
multi_sel = [doc.GetElement(x) for x in uidoc.Selection.GetElementIds()]

#Get Wall/s
walls = list()
if isinstance(multi_sel, list):
	walls = multi_sel
else:
	walls.append(multi_sel)

__title__ = "Wall Finish Creator"
__doc__ = "Create new wall or finish wall picking one or multiple walls. It works like wall by pick face"

#Tool Works if Walls are selected.
__context__= "Walls"
# Initiate Transaction
t = DB.Transaction(doc, 'Create Wall Finish')

#Append elements here.
new_walls = list()
hosted_elements = list()
loc_points= list()
ids = list()

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

#Wall types collector:
wall_types = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Walls).WhereElementIsElementType().ToElements()

for wall in walls:
	if wall.LookupParameter("Location Line").AsString() != "FinishFaceExterior":
		#Start Transaction
		t.Start()

		for wall in walls:
			wall.LookupParameter("Location Line").Set(2)

		t.Commit()

t.Start()	
	
for wall in walls:
		
	#For copy Walls.
	direction = DB.XYZ(0,0,0)

	#Id of New Wall.
	id = DB.ElementTransformUtils.CopyElement(doc,wall.Id,direction)
 	
 	#New Wall
 	n_wall = doc.GetElement(id[0])
	
	#Append new walls in new list.
	new_walls.append(n_wall)
	
	#Get information from given type
	wall_wallType = wall.WallType

	#Get Level
	wall_level = set_by_level(wall)

	current_wallType = wall_wallType.LookupParameter("Type Name").AsString()

	if current_wallType == "0-E-110-Bloque Ceramico": 
		if wall_level == 0:
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (hasta 4m)"
		elif wall_level == 1:
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (de 4.1m a 8m)"
		elif wall_level > 1:	
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (+8m)"

	elif current_wallType == "0-E-010-Con Revoque": 
		if wall_level == 0:
			walltype_finish = "PAQ. AHV+ FINO+ RP (hasta 4m)"
		elif wall_level == 1:
			walltype_finish = "PAQ. AHV+ FINO+ RP (de 4.1m a 8m)"
		elif wall_level > 1:	
			walltype_finish = "PAQ. AHV+ FINO + RP (+8m)"

	elif current_wallType == "0-E-010-Con Revoque Doble Cara": 
		if wall_level == 0:
			walltype_finish = "PAQ. AHV+ FINO+ RP (hasta 4m)"
		elif wall_level == 1:
			walltype_finish = "PAQ. AHV+ FINO+ RP (de 4.1m a 8m)"
		elif wall_level > 1:	
			walltype_finish = "PAQ. AHV+ FINO + RP (+8m)"

	elif current_wallType == "MP 04-Mamposteria de ladrillo hueco 18x18x33": 
		if wall_level == 0:
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (hasta 4m)"
		elif wall_level == 1:
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (de 4.1m a 8m)"
		elif wall_level > 1:	
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (+8m)"

	elif current_wallType == "MP 03-Mamposteria de ladrillo hueco 12x18x33": 
		if wall_level == 0:
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (hasta 4m)"
		elif wall_level == 1:
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (de 4.1m a 8m)"
		elif wall_level > 1:	
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (+8m)"

	elif current_wallType == "MP 02-Mamposteria de ladrillo hueco 8x18x33": 
		if wall_level == 0:
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (hasta 4m)"
		elif wall_level == 1:
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (de 4.1m a 8m)"
		elif wall_level > 1:	
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (+8m)"

	elif current_wallType == "0-E-111-Estructura de hormigon": 
		if wall_level == 0:
			walltype_finish = "RECUADRE DE LOSAS,CORNISAS,VIGAS,COLUMNAS, MENSULAS"
		elif wall_level == 1:
			walltype_finish = "RECUADRE DE LOSAS,CORNISAS,VIGAS,COLUMNAS, MENSULAS"
		elif wall_level > 1:	
			walltype_finish = "RECUADRE DE LOSAS,CORNISAS,VIGAS,COLUMNAS, MENSULAS"
	
	elif current_wallType == "0-E-110-Contrafrente Ladrillo": 
		if wall_level == 0:
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (hasta 4m)"
		elif wall_level == 1:
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (de 4.1m a 8m)"
		elif wall_level > 1:	
			walltype_finish = "PAQ. AHV+ GRUESO+ RP (+8m)"

	elif current_wallType == "0-E-110-Ladrillo visto": 
		if wall_level == 0:
			walltype_finish = "SILICONA SOBRE HORMIGON O LADRILLO VISTO"
		elif wall_level == 1:
			walltype_finish = "SILICONA SOBRE HORMIGON O LADRILLO VISTO"
		elif wall_level > 1:	
			walltype_finish = "SILICONA SOBRE HORMIGON O LADRILLO VISTO"

	else:
		walltype_finish = current_wallType	
	
	#For get WallType Finish
	for w in wall_types:
		type_name = w.LookupParameter("Type Name").AsString()
		if  walltype_finish == type_name:
			n_wall.WallType = w

	#Flip new wall		
	n_wall.Flip()

	#collector:
	door_types = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Doors).WhereElementIsElementType().ToElements()
	win_types = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Windows).WhereElementIsElementType().ToElements()

	incopenings,incshadows,incwalls,incshared = False, False, False, False
	for new_wall in new_walls:
		try:
			inserts = new_wall.FindInserts(incopenings,incshadows,incwalls,incshared)
			for insert in inserts:
				elem = new_wall.Document.GetElement(insert)
				doc.Delete(elem.Id)
							
							
		except:
			pass

		if len(inserts)>0:
			DB.JoinGeometryUtils.JoinGeometry(doc,new_wall,wall)	

t.Commit()
	