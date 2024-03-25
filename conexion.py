import pymongo

MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_TIME_OUT = 1000

MONGO_URL = 'mongodb://'+MONGO_HOST+":"+MONGO_PORT+"/"

try:
    cliente = pymongo.MongoClient(
        MONGO_URL, serverSelectionTimeoutMS=MONGO_TIME_OUT)
    cliente.server_info()
    print("Coneccion a MongoDB exitosa")
    cliente.close()
except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
    print("Tiempo exedido "+errorTiempo)
except pymongo.errors.ConnectionFailure as errorConexion:
    print("Fallo al conectarse a mongodb "+errorConexion)
