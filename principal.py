from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from pip._internal import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hojas_de_vida.sqlite3'
app.config['SECRET_KEY'] = "random string"

tabla = SQLAlchemy(app)

class personas(tabla.Model):
   __tablename__ = "persona"
   
   id = tabla.Column('id', tabla.Integer, primary_key = True)
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
   
   id = tabla.Column('id', tabla.Integer, primary_key = True)
   institucion = tabla.Column(tabla.String(50))
   titulo = tabla.Column(tabla.String(50))
   anio = tabla.Column(tabla.Integer)
   persona_id = tabla.Column(tabla.Integer , tabla.ForeignKey("persona.id"))

   def __init__(self, institucion, titulo, anio, persona_id):
        self.institucion = institucion
        self.titulo = titulo
        self.año = año
        self.persona_id = persona_id

class intereses(tabla.Model):
    __tablename__ = "intereses"
    
    id = tabla.Column('id', tabla.Integer, primary_key = True)
    tipo = tabla.Column(tabla.String(50))
    descripcion = tabla.Column(tabla.String(150))
    persona_id = tabla.Column(tabla.Integer, tabla.ForeignKey('persona.id'))

    def __init__(self, tipo, descripcion, persona_id):
        self.tipo = tipo
        self.descripcion = descripcion
        self.persona_id = persona_id

@app.route('/')
def show_all():
   return render_template('show_all.html', personas = personas.query.all() )

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
      if not request.form['institucion'] or not request.form['titulo'] or not request.form['anio']:         
         flash('Please enter all the fields', 'error')
      else:
         academi = academico(request.form['institucion'], request.form['titulo'], request.form['anio'], request.form['pesona_id'])
         tabla.session.add(academi)
         tabla.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('showAcademic'))
   return render_template('newAcademic.html')

@app.route('/showAcademic')
def showAcademic():
   return render_template('showAcademic.html', academico = academico.query.all() )

@app.route('/newIntereses', methods = ['GET', 'POST'])
def newIntereses():
   if request.method == 'POST':
      if not request.form['tipo'] or not request.form['descripcion']:         
         flash('Please enter all the fields', 'error')
      else:
         interes = intereses(request.form['tipo'], request.form['descripcion'], request.form['pesona_id'])
         tabla.session.add(interes)
         tabla.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('showIntereses'))
   return render_template('newIntereses.html')

@app.route('/showIntereses')
def showIntereses():
   return render_template('showIntereses.html', intereses = intereses.query.all() )


@app.route("/update", methods=["POST"])
def update():
    name = request.form.get("oldname")
    persona = personas.query.filter_by(id=name).first()
    return render_template('update.html', result = persona, oldname = name)

@app.route("/update_record", methods=["POST"])
def update_record():
    name = request.form.get("oldname")
    persona = personas.query.filter_by(id=name).first()
    persona.identificacion = request.form['identificacion']
    persona.foto = request.form['foto'] 
    persona.nombre = request.form['nombre']
    persona.apellido = request.form['apellido']
    persona.telefono = request.form['telefono'] 
    persona.direccion = request.form['direccion']
    tabla.session.commit()
    return redirect('/')

@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("oldname")
    persona = personas.query.filter_by(id=name).first()
    tabla.session.delete(persona)
    tabla.session.commit()
    return redirect("/")
    

if __name__ == '__main__':
   tabla.create_all()
   app.run(debug = True)
    