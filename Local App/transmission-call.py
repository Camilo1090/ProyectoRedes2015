import json
import subprocess
import datetime


# funcion para consultar los nuevos magnet links en openshift
# se reciben en formato JSON
# si hay alguno nuevo se manda de inmediato a transmission
def consult_magnets():
 magnets_json = subprocess.check_output(["curl", "http://proyecto-redestest.rhcloud.com/transmission/new"]) # consulta
 print magnets_json
 magnets = json.loads(magnets_json)	# la lista en formato JSON
 if len(magnets) == 0:			# lista vacia, no hay nuevos
  print "No new magnets"
 for m in magnets:			# se procesan si hay
  print "Sending "+str(m)
  subprocess.call(["transmission-remote", "-a", str(m)]) # se envian a transmission

# funcion para consultar el estado de los links a transmission y enviarlo a openshift
def update_states():
 now = datetime.datetime.now()
 states = get_states() 		# se extraen los estados de todos los links en transmission
 for st in states:
  hash_id = str(st[0])		# se extrae el hash que sirve de identificador en openshift
  state = str(st[1])		# se extrae el estado del link 
  progress = str(st[2])		# se extrae el progreso del link
  data = "year="+str(now.year)+"&month="+str(now.month)+"&day="+str(now.day)+"&hour="+str(now.hour)+"&minute="+str(now.minute)+"&second="+str(now.second)+"&hash="+hash_id+"&state="+state+"&progress="+progress
  print subprocess.check_output(["curl", "http://proyecto-redestest.rhcloud.com/transmission/update?"+data]) # se envia a openshift

# funcion que extrae el estado de todos los links en transmission
def get_states():
 string = subprocess.check_output(["transmission-remote", "-l"]) # se extrae la lista de links
 ids = get_ids(string) # se traduce en una lista simple con los ids
 states = []
 for x in ids:
  text = subprocess.check_output(["transmission-remote", "-t", x, "-i"]) # por cada id se extrae la informacion de su estado
  print text
  lines = text.split('\n')
  hash_id = "magnet:?xt=urn:btih:"+(lines[3].split())[1] # se extrae el magnet link
  state = (lines[7].split())[1]				 # se extrae el estado
  progress = (lines[9].split())[2]			 # se extrae el progreso
  if (progress == "nan%"):
   progress = "0%"
  states.append([hash_id, state, progress]) # se adiciona a la lista de estados
 print states
 return states

# funcion para extraer la lista de IDs de los links en transmission
# transmission asigna un ID a cada link y asi los identifica
# se extraen todos para posteriormente consultar su estado
def get_ids(text):
 lineas = text.split('\n')
 print len(lineas)
 if (len(lineas) > 3):
  l = []
  i = 1
  while i < (len(lineas) - 2):
   l.append((lineas[i].split())[0])
   i += 1
  print l
  return l
 else:
  return []

# funcion que comienza la aplicacion
def start():
 consult_magnets()
 update_states()

# ejecucion
start()
