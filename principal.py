from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///personas.sqlite'
app.config['SECRET_KEY'] = "random string"

tabla = SQLAlchemy(app)

class personas(tabla.Model):
   __tablename__ = "persona"
   
   id = tabla.Column('persona_id', tabla.Integer, primary_key = True)
   identificacion = tabla.Column(tabla.String(50))
   foto = tabla.Column(tabla.String(50))
   nombre = tabla.Column(tabla.String(50))
   apellido = tabla.Column(tabla.String(50))
   telefono = tabla.Column(tabla.String(50))
   direccion = tabla.Column(tabla.String(80))

   def __init__(self, identificacion, foto, nombre, apellido, telefono, direccion ):
      self.identificacion = identificacion
      self.foto = foto
      self.nombre = nombre
      self.apellido = apellido
      self.telefono = telefono
      self.direccion = direccion

class academico(tabla.Model):
   __tablename__ = "academico"
   
   id = tabla.Column('persona_id', tabla.Integer, primary_key = True)
   primaria = tabla.Column(tabla.String(50))
   secundaria = tabla.Column(tabla.String(50))
   universidad = tabla.Column(tabla.String(50))
   otros = tabla.Column(tabla.String(50))

   def __init__(self, primaria, secundaria, universidad, otros):
      self.primaria = primaria
      self.secundaria = secundaria
      self.universidad = universidad
      self.otros = otros

@app.route('/')
def show_all():
   return render_template('show_all.html', personas = personas.query.all() )

@app.route('/showAcademic')
def showAcademic():
   return render_template('showAcademic.html', academico = academico.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['identificacion'] or not request.form['foto'] or not request.form['nombre'] or not request.form['apellido'] or not request.form['telefono'] or not request.form['direccion']:
         flash('Please enter all the fields', 'error')
      else:
         persona = personas(request.form['identificacion'], request.form['foto'], request.form['nombre'], request.form['apellido'],request.form['telefono'], request.form['direccion'])
         tabla.session.add(persona)
         tabla.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

@app.route('/newAcademic', methods = ['GET', 'POST'])
def newAcademic():
   if request.method == 'POST':
      if not request.form['primaria'] or not request.form['secundaria'] or not request.form['universidad'] or not request.form['otros']:
         flash('Please enter all the fields', 'error')
      else:
         academi = academico(request.form['primaria'], request.form['secundaria'], request.form['universidad'], request.form['otros'])
         tabla.session.add(academi)
         tabla.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('showAcademic'))
   return render_template('newAcademic.html')
    

if __name__ == '__main__':
   tabla.create_all()
   app.run(debug = True)
    