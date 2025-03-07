from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 📌 Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 📌 Definir el modelo de la base de datos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'Producto({self.nombre}, ${self.precio})'

# 📌 Crear la base de datos si no existe
with app.app_context():
    db.create_all()

# 📌 Ruta principal
@app.route('/')
def home():
    return render_template('index.html')

# 📌 Ruta para la tienda (muestra productos)
@app.route('/tienda')
def tienda():
    productos = Producto.query.all()  # Obtener todos los productos
    return render_template('tienda.html', productos=productos)

# 📌 Ruta para agregar productos con un formulario
@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        imagen = request.form['imagen']

        nuevo_producto = Producto(nombre=nombre, precio=precio, imagen=imagen)
        db.session.add(nuevo_producto)
        db.session.commit()

        return redirect(url_for('tienda'))  # Redirige a la tienda después de agregar

    return render_template('agregar_producto.html')  # Muestra el formulario

# 📌 Ruta para la página de contacto
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# 📌 Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
