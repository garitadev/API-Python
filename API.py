import requests
import json
import pyodbc


##Parametros Necesarios para el API
publicKey = "b1d3cb7a0a2a98a8ba1d7752151053d8"
privateKey = "e5682578653c74f03ddb4c3651430de617e653d4"
ts=1
hashGenerate= "5d089accc9c22798c56b3b2435996d66"
urlRequest = f"https://gateway.marvel.com:443/v1/public/characters?ts={ts}&apikey={publicKey}&hash={hashGenerate}"
print(urlRequest)



##Función que obtiene los personajes del API y los almacena en el tabla de personajes correspondiente
def obtenerPersonajes(conn):
    lista = []
    cursor = conn.cursor()
    response = requests.get(urlRequest)


    if response.status_code==200:
        response_json = json.loads(response.text)
        
        #for para recorrer el array que retorna el request
        for i in response_json["data"]["results"]:
            id=i["id"]
            name = i["name"]
            description = i["description"]
            comics_available = i["comics"]["available"]
            series_available = i["series"]["available"]
            did = {"id":id,"name":name,"description":description, "comics_available":comics_available, "series_available":series_available}
            lista.append(did)
            querry =  'insert  into Characters (idCharacter, name, comics_available, series_available, description) values ('+str(id)+','+"'"+name+"'"','+str(comics_available)+','+str(series_available)+','+"'"+description+"'"')'
            cursor.execute(querry)
            conn.commit()
    print(lista)
            
            
##Función que obtiene los comics respectivos de cada personaje y los inserta en la bd, se usa el id del personaje como llama llave foranea para hacer la consulta
def obtenerComicsXPersonaje(conn):
    response = requests.get(urlRequest)
    cursor = conn.cursor()
    listaComicsXPersonajes = []

    if response.status_code==200:
        response_json = json.loads(response.text)
        
        #for para recorrer el array que retorna el request
        for i in response_json["data"]["results"]:
            id=i["id"]
            comics_names =i["comics"]["items"]
            comics_names =i["name"]
            comicsXPersonajes ={"id":id, "comics_names":comics_names}
            listaComicsXPersonajes.append(comicsXPersonajes)
            querry =  'insert into Comics (idCharacter, name) values ('+str(id)+','+"'"+comics_names+"'"')'
            cursor.execute(querry)
            conn.commit()
    
    print(listaComicsXPersonajes)

##Función que obtiene las respectivas series los de cada personaje y los inserta en la bd, se usa el id del personaje como llama llave foranea para hacer la consulta

def obtenerSeriesXPersonaje(conn):
    response = requests.get(urlRequest)
    cursor = conn.cursor()
    listaSeriesXPersonajes = []

    if response.status_code==200:
        response_json = json.loads(response.text)
        
        #for para recorrer el array que retorna el request
        for i in response_json["data"]["results"]:
            id=i["id"]
            series_names =i["series"]["items"]
            series_names =i["name"]
            seriesXPersonajes ={"id":id, "series_names":series_names}
            listaSeriesXPersonajes.append(seriesXPersonajes)
            querry =  'insert into Series (idCharacter, name) values ('+str(id)+','+"'"+series_names+"'"')'
            cursor.execute(querry)
            conn.commit()
    
    print(listaSeriesXPersonajes)


##Conexión de la bd
conn = pyodbc.connect("Driver={SQL Server};"
                      "Server=DLAP\SQLEXPRESS;"
                      "Database=API_Marvel;"
                      "Trusted_Connection=yes;")

obtenerPersonajes()
obtenerComicsXPersonaje()
obtenerSeriesXPersonaje()