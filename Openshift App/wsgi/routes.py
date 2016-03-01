import os
from flask import Flask, request, render_template
import monitor
import transmission

## archivo routes que sirve de direccionador de las rutas del web server
## cada ruta realiza una accion especifica
## se utiliza el microframework Flask

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

# ruta inicio
@app.route("/")
def welcome():
 return render_template('index.html')

# ruta para insertar un estado del sistema
@app.route("/monitor/insert")
def monitor_insert():
 return monitor.insert_state(request.args.get('year'), request.args.get('month'), request.args.get('day'), request.args.get('hour'), request.args.get('minute'), request.args.get('second'), request.args.get('who'), request.args.get('cpu_us'), request.args.get('cpu_sy'), request.args.get('cpu_id'), request.args.get('cpu_wa'), request.args.get('cpu_st'), request.args.get('mem_swpd'), request.args.get('mem_free'), request.args.get('mem_buff'), request.args.get('mem_cache'), request.args.get('swap_si'), request.args.get('swap_so'))

# ruta para consultar el historico de estados del sistema
@app.route("/monitor/consult")
def monitor_consult():
 return monitor.consult_states()

# ruta para mostrar el formulario para insertar un magnet link
@app.route("/transmission/insert")
def transmission_insert():
 return render_template('transmission_insert.html')

# ruta para adicionar un magnet link
@app.route("/transmission/magnet", methods=['POST'])
def transmission_magnet():
 if request.method == 'POST':
  return transmission.insert_magnet(request.form['mlink'])

# ruta para consultar el estado de los magnet links
@app.route("/transmission/consult")
def transmission_consult():
 return transmission.consult_states()

# ruta para consultar los nuevos magnet links
@app.route("/transmission/new")
def transmission_new():
 return transmission.consult_magnets()

# ruta para actualizar el estado de un magnet link
@app.route("/transmission/update")
def transmission_update():
 return transmission.update_state(request.args.get('year'), request.args.get('month'), request.args.get('day'), request.args.get('hour'), request.args.get('minute'), request.args.get('second'), request.args.get('hash'), request.args.get('state'), request.args.get('progress'))


if __name__ == "__main__":
 app.run()
