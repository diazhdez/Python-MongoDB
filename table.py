from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo

MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_TIME_OUT = 1000

MONGO_URL = 'mongodb://'+MONGO_HOST+":"+MONGO_PORT+"/"

MONGO_DB = 'integradora'
MONGO_COLLECTION = 'integrantes'


def showData(table):
    try:
        cliente = pymongo.MongoClient(
            MONGO_URL, serverSelectionTimeoutMS=MONGO_TIME_OUT)
        db = cliente[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        for document in collection.find():
            table.insert(
                '', 0, text=document['_id'], values=document['nombre'])
        cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo exedido "+errorTiempo)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a mongodb "+errorConexion)


window = Tk()
table = ttk.Treeview(window, columns=2)
table.grid(row=1, column=0, columnspan=2)
table.heading("#0", text="ID")
table.heading("#1", text="Nombre")
showData(table)
window.mainloop()
