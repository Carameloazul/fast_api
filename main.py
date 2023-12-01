from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
#Cambiando el titulo de docs
app.title = "Mi aplicacion con FastAPI"
#Cambiando la version
app.version = "0.0.1"

#Cambiando la etiqueta de la direccion
@app.get('/', tags=['home'])
def message():
    # Puedo retornar lo que quiera, incluso html
    #return {"Hello ","World!"}
    return HTMLResponse('<h1>Hello World!</h1>')

movies = [
    {
        "id" : 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi",
        "year" : 2009,
        "rating" : 7.8,
        "category" : "Accion"
    },
    {
        "id" : 2,
        "title": "Titanic",
        "overview": "Una historia de amor que se desarrolla en un gran barco que se hunde por el choque de un iceberg",
        "year" : 2009,
        "rating" : 7.8,
        "category" : "Accion"
    }

]

@app.get('/movies', tags=['movies'])
def get_movies():
    
    return movies

@app.get('/movies/{id}',tags=['movies'])
def get_movie(id:int):
    for item in movies:
        if item["id"] == id:
            return item

    return []

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category:str, year:int):
    movie = list(filter(lambda x: x['category'] == category and x['year'] == year, movies))
    
    return movie

@app.post('/movies',tags=['movies'])
def add_movie(id:int = Body(),title:str= Body(), 
              overview:str= Body(), year:int= Body(),
              rating:float= Body(), category:str = Body() ):
    movies.append({
        "id":id,
        "title":title,
        "overview": overview,
        "year":year,
        "rating":rating,
        "category":category
    })
    return movies

# Para ejecutar el servicio se utiliza la libreria uvicorn
# Se indica el fichero y luego el nombre de la aplicacion en este caso app
# uvicorn main:app

# Para que se recargue en cada cambio se pasa el argumento reload
# uvicorn main:app --reload

# Para cambiar el puerto se pasa el argumento --port
# uvicorn main:app --port 5000

# Para que este disponible en cualquier dispositivo se usa -- host
# uvicorn main:app --host 0.0.0.0

# Y para que funcione todo de una vez se pasa todos los argumentos de una
# uvicorn main:app --reload --port 5000 --host 0.0.0.0
