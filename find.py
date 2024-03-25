from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo

from bson.objectid import ObjectId

MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_TIME_OUT = 1000

MONGO_URL = 'mongodb://'+MONGO_HOST+":"+MONGO_PORT+"/"

MONGO_DB = 'integradora'
MONGO_COLLECTION = 'integrantes'

cliente = pymongo.MongoClient(
    MONGO_URL, serverSelectionTimeoutMS=MONGO_TIME_OUT)
db = cliente[MONGO_DB]
collection = db[MONGO_COLLECTION]

integranteID = ''


def showData(nombre="", rol=""):
    objectoBuscar = {}
    if len(nombre) != 0:
        objectoBuscar["nombre"] = nombre
    if len(rol) != 0:
        objectoBuscar["rol"] = rol
    try:
        registros = table.get_children()
        for registro in registros:
            table.delete(registro)
        for document in collection.find():
            table.insert('', 0, text=document['_id'], values=(
                document['nombre'], document['rol']))
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo exedido " + errorTiempo)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a mongodb " + errorConexion)


def crearRegistro():
    if len(nombre.get()) != 0 and len(rol.get()) != 0:
        try:
            document = {'nombre': nombre.get(), 'rol': rol.get()}
            collection.insert_one(document)
            nombre.delete(0, END)
            rol.delete(0, END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message='Los campos no pueden estar vacios')
    showData()


def dobleClickTabla(event):
    global integranteID
    integranteID = str(table.item(table.selection())["text"])
    document = collection.find({'_id': ObjectId(integranteID)})[0]
    nombre.delete(0, END)
    nombre.insert(0, document['nombre'])
    rol.delete(0, END)
    rol.insert(0, document['rol'])
    create['state'] = 'disabled'
    edit['state'] = 'normal'
    delete['state'] = 'normal'


def editarRegistro():
    global integranteID
    if len(nombre.get()) != 0 and len(rol.get()) != 0:
        try:
            idBuscar = {'_id': ObjectId(integranteID)}
            nuevosValores = {
                "$set": {'nombre': nombre.get(), 'rol': rol.get()}}
            collection.update_one(idBuscar, nuevosValores)
            nombre.delete(0, END)
            rol.delete(0, END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror('Los campos no pueden estar vacios')
    showData()
    create['state'] = 'normal'
    edit['state'] = 'disabled'
    delete['state'] = 'disabled'


def borrarRegistro():
    global integranteID
    try:
        idBuscar = {'_id': ObjectId(integranteID)}
        collection.delete_one(idBuscar)
        nombre.delete(0, END)
        rol.delete(0, END)
    except pymongo.errors.ConnectionFailure as error:
        print(error)
    showData()
    create['state'] = 'normal'
    edit['state'] = 'disabled'
    delete['state'] = 'disabled'


def buscarRegistro():
    showData(buscarNombre.get(), buscarRol.get())


window = Tk()
table = ttk.Treeview(window, columns=('nombre', 'rol'))
table.grid(row=1, column=0, columnspan=2)
table.heading("#0", text="ID")
table.heading("nombre", text="Nombre")
table.heading("rol", text="Rol")
table.bind("<Double-Button-1>", dobleClickTabla)

# Name
Label(window, text='Nombre').grid(row=2, column=0, sticky=W+E)
nombre = Entry(window)
nombre.grid(row=2, column=1, sticky=W+E)
nombre.focus()

# Rol
Label(window, text='Rol').grid(row=3, column=0, sticky=W+E)
rol = Entry(window)
rol.grid(row=3, column=1, sticky=W+E)

# Button create
create = Button(window, text='Agregar integrante',
                command=crearRegistro, bg='green', fg='white')
create.grid(row=4, column=0, padx=(10, 2), pady=5)  # Ajuste de padx

# Button edit
edit = Button(window, text='Editar Integrante',
              command=editarRegistro, bg='yellow')
edit.grid(row=4, column=1, padx=2, pady=5)  # Ajuste de padx
edit['state'] = 'disabled'

# Button delete
delete = Button(window, text='Borrar integrante',
                command=borrarRegistro, bg='red', fg='white')
delete.grid(row=4, column=2, padx=(2, 10), pady=5)  # Ajuste de padx
delete['state'] = 'disabled'

# Search Name
Label(window, text='Buscar por nombre').grid(row=5, column=0, sticky=W+E)
buscarNombre = Entry(window)
buscarNombre.grid(row=5, column=1, sticky=W+E)  # Corrección aquí

# Search Rol
Label(window, text='Buscar por rol').grid(row=6, column=0, sticky=W+E)
buscarRol = Entry(window)
buscarRol.grid(row=6, column=1, sticky=W+E)  # Corrección aquí

# Button search
search = Button(window, text='Buscar integrante',
                command=buscarRegistro, bg='blue', fg='white')
search.grid(row=7, columnspan=2, sticky=W+E)

showData()
window.mainloop()
