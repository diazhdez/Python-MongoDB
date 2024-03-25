import pymongo

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

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


def showData():
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


window = Tk()
table = ttk.Treeview(window, columns=('nombre', 'rol'))
table.grid(row=1, column=0, columnspan=2)
table.heading("#0", text="ID")
table.heading("nombre", text="Nombre")
table.heading("rol", text="Rol")
table.bind("<Double-Button-1>", dobleClickTabla)

# Name
Label(window, text='Nombre').grid(row=2, column=0)
nombre = Entry(window)
nombre.grid(row=2, column=1)

# Rol
Label(window, text='Rol').grid(row=3, column=0)
rol = Entry(window)
rol.grid(row=3, column=1)

# Button create
create = Button(window, text='Agregar integrante',
                command=crearRegistro, bg='green', fg='white')
create.grid(row=4, columnspan=2)

# Button edit
edit = Button(window, text='Editar Integrante',
              command=editarRegistro, bg='yellow')
edit.grid(row=5, columnspan=2)
edit['state'] = 'disabled'

showData()
window.mainloop()
