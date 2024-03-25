import pymongo

MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_TIME_OUT = 1000

MONGO_URL = 'mongodb://'+MONGO_HOST+":"+MONGO_PORT+"/"

MONGO_DB = 'integradora'
MONGO_COLLECTION = 'integrantes'

try:
    cliente = pymongo.MongoClient(
        MONGO_URL, serverSelectionTimeoutMS=MONGO_TIME_OUT)
    db = cliente[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    for documento in collection.find():
        print(documento['nombre'])
    cliente.close()
except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
    print("Tiempo exedido "+errorTiempo)
except pymongo.errors.ConnectionFailure as errorConexion:
    print("Fallo al conectarse a mongodb "+errorConexion)
