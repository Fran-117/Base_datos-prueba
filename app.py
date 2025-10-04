from flask import Flask, render_template, request, redirect
#FLASK= crear una aplicacion web, RENDER_TEMPLATE= para mostrar archivos html, REQUEST= para recibir datos de los formularios, REDIRECT= para redirigir a otras rutas

from flask_pymongo import PyMongo
#FLASK_PYMONGO= para conectar flask con mongodb

from bson.objectid import ObjectId
#Mongo usa un ID especial para identificar cada documento, este ID es un ObjectId, esto nos permite trabajar con esos IDs en Python



app = Flask(__name__)
#Indica el punto donde arranca flask y la creación de la aplicacion web

app.config["MONGO_URI"] = "mongodb://localhost:27017/primer_crud"
#Configuracion de la base de datos, indicando la URI de conexion y el nombre de la base de datos

mongo = PyMongo(app)
#Crea el objeto, que nos permite interactuar con la base de datos

@app.route('/') #READ
def index():
    users = mongo.db.users.find()
    return render_template('index.html', users=users)
#Ruta principal, obtiene todos los usuarios de la coleccion "users" y los pasa a la plantilla index.html


@app.route('/add', methods=['POST']) #CREATE
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')
    mongo.db.users.insert_one({'name': name, 'email': email})
    return redirect('/')
#Ruta para agregar un nuevo usuario, recibe los datos del formulario, los inserta en la coleccion "users" y redirige a la ruta principal


@app.route('/delete/<user_id>') #DELETE
def delete_user(user_id):
    mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    return redirect('/')
#Ruta para eliminar un usuario, recibe el ID del usuario en la URL, lo convierte a ObjectId y lo elimina de la coleccion "users", luego redirige a la ruta principal


@app.route('/edit/<user_id>') #EDITA EL FORMULARIO
def edit_user(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return render_template('edit.html', user=user)
#Ruta para mostrar el formulario de edicion, recibe el ID del usuario en la URL, obtiene el usuario de la coleccion "users" y lo pasa a la plantilla edit.html

@app.route('/update/<user_id>', methods=['POST']) #UPDATE
def update_user(user_id):
    name = request.form['name']
    email = request.form['email']
    mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'name': name, 'email': email}})
    return redirect('/')
#Ruta para actualizar un usuario, recibe el ID del usuario en la URL, obtiene los datos del formulario, actualiza el usuario en la coleccion "users" y redirige a la ruta principal

if __name__ == '__main__':
    app.run(debug=True)
#Ejecuta la aplicacion en modo debug, para que se reinicie automaticamente al hacer cambios
