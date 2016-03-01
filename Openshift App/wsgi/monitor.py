import psycopg2
import os


# funcion para insertar un estado del sistema en la base de datos
def insert_state(year, month, day, hour, minute, second, who, cpu_us, cpu_sy, cpu_id, cpu_wa, cpu_st, mem_swpd, mem_free, mem_buff, mem_cache, swap_si, swap_so):
 local_cursor = get_cursor()
 fecha = str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(second)
 begin = "BEGIN;"
 local_cursor.execute(begin)
 sql = "INSERT INTO monitor (fecha, who, cpu_us, cpu_sy, cpu_id, cpu_wa, cpu_st, mem_swpd, mem_free, mem_buff, mem_cache, swap_si, swap_so) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
 local_cursor.execute(sql, (fecha, str(who), str(cpu_us), str(cpu_sy), str(cpu_id), str(cpu_wa), str(cpu_st), str(mem_swpd), str(mem_free), str(mem_buff), str(mem_cache), str(swap_si), str(swap_so)))
 commit = "COMMIT;"
 local_cursor.execute(commit) 
 return "INSERT SUCCESSFUL\n"

# funcion para consultar el historico de estados del sistema
def consult_states():
 local_cursor = get_cursor()
 sql = "SELECT * FROM monitor ORDER BY fecha DESC;"
 local_cursor.execute(sql)
 rows = local_cursor.fetchall()
 return states_table(rows)

# funcion que genera una tabla con la informacion de los estados del sistema
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
	<title>System Status Log</title>
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
				<p class="navbar-brand">System Status Log</p>
			</nav>
		</div>
	</div>
		<div class="row">
			<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
				<table class="table table-hover">
					<thead>
						<tr>
							<th>Date</th>
							<th>User</th>
							<th>CPU user (%)</th>
							<th>CPU system (%)</th>
							<th>CPU idle (%)</th>
							<th>CPU wait (%)</th>
							<th>CPU st (%)</th>
							<th>Memory swapped (KB)</th>
							<th>Memory free (KB)</th>
							<th>Memory buffered (KB)</th>
							<th>Memory cached (KB)</th>
							<th>Swap in (KB)</th>
							<th>Swap out (KB)</th>
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
