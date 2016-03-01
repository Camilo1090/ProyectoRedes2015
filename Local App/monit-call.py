import subprocess
import json
import thread
import time
import psycopg2
import datetime


# funcion que ejecuta la herramienta de monitoreo
# se asume que la herramienta esta en el mismo directorio que este archivo
def monitor():
 subprocess.call(["python", "RESTMonitoring.py"])

# funcion para preguntar por el usuario logueado en el sistema
def who():
 output = subprocess.check_output(["curl", "http://0.0.0.0:5000/who"])
 who = json.loads(output)
 #print output
 return who["users"]

# funcion para preguntar por el estado de la cpu del sistema
def cpu(s):
 output = subprocess.check_output(["curl", "http://0.0.0.0:5000/cpu/"+s])
 cpu = json.loads(output)
 #print output
 return cpu["cpu "+s] 

# funcion para preguntar por el estado de la memoria del sistema
def mem(s):
 output = subprocess.check_output(["curl", "http://0.0.0.0:5000/mem/"+s])
 mem = json.loads(output)
 #print output
 return mem["mem "+s]

# funcion para preguntar por el estado de la memoria swap del sistema
def swap(s):
 output = subprocess.check_output(["curl", "http://0.0.0.0:5000/swap/"+s])
 swap = json.loads(output)
 #print output
 return swap["swap "+s]

# funcion que reune todas las partes del estado del sistema
# y las escribe en una URL de modo que sea recibida por la app en openshift
# y de esta manera se inserte el estado de la maquina en la pasarela
def insert_state():
 now = datetime.datetime.now()
 w = who().replace("\n", "")
 cpu_us = cpu("us").replace("\n", "")
 cpu_sy = cpu("sy").replace("\n", "")
 cpu_id = cpu("id").replace("\n", "")
 cpu_wa = cpu("wa").replace("\n", "")
 cpu_st = cpu("st").replace("\n", "")
 mem_swpd = mem("swpd").replace("\n", "")
 mem_free = mem("free").replace("\n", "")
 mem_buff = mem("buff").replace("\n", "")
 mem_cache = mem("cache").replace("\n", "")
 swap_si = swap("si").replace("\n", "")
 swap_so = swap("so").replace("\n", "")
 data = "year="+str(now.year)+"&month="+str(now.month)+"&day="+str(now.day)+"&hour="+str(now.hour)+"&minute="+str(now.minute)+"&second="+str(now.second)+"&who="+w+"&cpu_us="+cpu_us+"&cpu_sy="+cpu_sy+"&cpu_id="+cpu_id+"&cpu_wa="+cpu_wa+"&cpu_st="+cpu_st+"&mem_swpd="+mem_swpd+"&mem_free="+mem_free+"&mem_buff="+mem_buff+"&mem_cache="+mem_cache+"&swap_si="+swap_si+"&swap_so="+swap_so
 print data
 subprocess.call(["curl", "http://proyecto-redestest.rhcloud.com/monitor/insert?"+data])

# funcion que comienza la aplicacion
def start():
 pid = thread.start_new_thread(monitor, ()) 			# se empieza la herramienta de monitoreo
 time.sleep(1) 							# tiempo para que arranque totalmente la herramienta
 insert_state() 						# se inserta el estado del sistema
 subprocess.call(["curl", "http://0.0.0.0:5000/shutdown"]) 	# se cierra la herramienta

# ejecucion
start()






