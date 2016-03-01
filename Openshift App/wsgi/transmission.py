import psycopg2
import os
import datetime
import json


# funcion para insertar un nuevo magnet link en la base de datos
def insert_magnet(magnet):
 local_cursor = get_cursor()
 d = datetime.datetime.now()
 fecha = str(d.year)+"-"+str(d.month)+"-"+str(d.day)+" "+str(d.hour)+":"+str(d.minute)+":"+str(d.second)
 local_cursor.execute("BEGIN;")
 sql = "INSERT INTO transmission (fecha_insert, fecha_update, magnet, estado, progreso) VALUES('"+fecha+"','"+fecha+"','"+magnet+"', 'New', '0%');"
 local_cursor.execute(sql)
 local_cursor.execute("COMMIT;")
 return "INSERT SUCCESFUL\n"

# funcion para consultar los nuevos magnet links
def consult_magnets():
 local_cursor = get_cursor()
 local_cursor.execute("BEGIN;")
 sql = "SELECT * FROM transmission WHERE estado = 'New';"
 local_cursor.execute(sql)
 rows = local_cursor.fetchall()
 local_cursor.execute("COMMIT;")
 return magnets_json(rows)

# funcion para convertir a formato JSON los nuevos magnet links
def magnets_json(rows):
 lista = []
 for row in rows:
  lista.append(row[3])
 return json.dumps(lista)

# funcion para consultar el estado de los magnet links
def consult_states():
 local_cursor = get_cursor()
 sql = "SELECT fecha_insert, fecha_update, magnet, estado, progreso FROM transmission ORDER BY fecha_insert DESC;"
 local_cursor.execute(sql)
 rows = local_cursor.fetchall()
 return states_table(rows)

# funcion que genera una tabla con la informacion del estado de los magnet links
def states_table(rows):
 lines = ""
 for row in rows:
  lines += "<tr>"
  for f in row:
   lines += "<td>"+str(f)+"</td>"
  lines += "</tr>"
 return """<!DOCTYPE html> 
<html>
<head>
	<title>Magnet Links Status Log</title>
	<meta charset="utf-8">
	<link rel="stylesheet" media="screen" href="//netdna.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
	<style type="text/css">
  	body {padding-top:70px;}
	</style>
</head>
<body>
	<div class="row">
		<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
			<nav class="navbar navbar-default navbar-fixed-top" role="navigation">
				<p class="navbar-brand">Magnet Links Status Log</p>
			</nav>
		</div>
	</div>
		<div class="row">
			<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
				<table class="table table-hover">
					<thead>
						<tr>
							<th>Date Inserted</th>
							<th>Last Update</th>
							<th>Magnet Link</th>
							<th>State</th>
							<th>Progress</th>
						</tr>
					</thead>
					<tbody>
						"""+lines+"""
					</tbody>
				</table>
			</div>
		</div>
	</div>
</body>
</html>"""

# funcion que actualiza el estado de un magnet link en la base de datos
def update_state(year, month, day, hour, minute, second, magnet_hash, state, progress):
 local_cursor = get_cursor()
 fecha = str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(second)
 local_cursor.execute("BEGIN;")
 sql = "UPDATE transmission SET fecha_update = '"+fecha+"', estado = '"+str(state)+"', progreso = '"+str(progress)+"' WHERE magnet LIKE '"+str(magnet_hash)+"%';"
 local_cursor.execute(sql)
 local_cursor.execute("COMMIT;")
 return "UPDATE SUCCESSFUL\n"

# funcion para obtener una conexion a la base de datos
def get_cursor():
 conn = psycopg2.connect(database=os.environ['OPENSHIFT_APP_NAME'],
               user=os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
               password=os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
               host=os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
               port=os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'] )
 cursor = conn.cursor()
 return cursor

# funcion para cerrar una conexion a la base de datos
def close_cursor(cursor):
 conn = cursor.connection
 cursor.close()
 conn.close()
