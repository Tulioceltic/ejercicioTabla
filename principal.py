from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///personas.sqlite'
app.config['SECRET_KEY'] = "random string"

tabla = SQLAlchemy(app)

class personas(tabla.Model):
   id = tabla.Column('persona_id', tabla.Integer, primary_key = True)
   nombre = tabla.Column(tabla.String(50))
   apellido = tabla.Column(tabla.String(50))
   telefono = tabla.Column(tabla.String(50))
   direccion = tabla.Column(tabla.String(80))
   estadoCivil = tabla.Column(tabla.String(15))
   def __init__(self, nombre, apellido, telefono, direccion, estadoCivil):
      self.nombre = nombre
      self.apellido = apellido
      self.telefono = telefono
      self.direccion = direccion
      self.estadoCivil = estadoCivil

@app.route('/')
def show_all():
   return render_template('show_all.html', personas = personas.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['nombre'] or not request.form['apellido'] or not request.form['telefono'] or not request.form['direccion'] or not request.form['estadoCivil']:
         flash('Please enter all the fields', 'error')
      else:
         persona = personas(request.form['nombre'], request.form['apellido'],request.form['telefono'], request.form['direccion'], request.form['estadoCivil'])
         tabla.session.add(persona)
         tabla.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')
    

if __name__ == '__main__':
   tabla.create_all()
   app.run(debug = True)
    