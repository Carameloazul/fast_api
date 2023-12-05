from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Annotated, List
from jwt_manager import create_token
# JSONresponse no es obligatorio, ya que fastapi lo usa por debajo
# https://fastapi.tiangolo.com/advanced/response-directly/

# Puedo validar y poner valores por defecto a las variables
# Con el parametro le(less equal) declaro que el valor entrante
# Tiene que ser menor o igual al que se le asigne eje: le = 1000
# El parametro ge(greater equal) establece un minimo

class User(BaseModel):
    email:str
    password:str

class Movies(BaseModel):
    #id : int | None = None
    id: Optional[int] 
    title:str = Field(default="Ninguno", min_length=5, max_length=50, description= "El nombre de la pelicula")
    overview:str = Field(default="Algo sobre la pelicula",min_length=15, max_length=50, description="Una descripcion del filme")
    year:int = Field(default=2019,le=2022, title="Ano de este siglo")
    rating:float = Field(default=9.8,ge=1,le=10)
    category:str = Field(default="Accion",max_length=200)

    # El contenido por defecto se puede poner de la sgt manera:


    # Tambien se puede usar json_schema_extra pero es mas complicado
    #model_config ={
        #"json_schema_extra":{
    class Config:
              example=[
                  {
                    "id":1,                 
                    "title" : "Mi pelicula",
                    "overview" : "Descripcion de la pelicula",
                    "year" : 2022,
                    "rating" : 9.8,
                    "category" : "Accion"
                   }
                    ]                
               #   }
           # }
        

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

@app.post('/',tags=['tags'])
def login(user:User):
    if user.email == "pepito@gmail.com" and user.password == "admin":
        token = create_token(user.model_dump(exclude_unset=True))
    return token

movies = [
    {
        "id" : 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi",
        "year" : 1999,
        "rating" : 7.8,
        "category" : "Accion"
    },
    {
        "id" : 2,
        "title": "Titanic",
        "overview": "Una historia de amor que se desarrolla en un gran barco que se hunde por el choque de un iceberg",
        "year" : 1988,
        "rating" : 7.8,
        "category" : "Accion"
    }

]

@app.get('/movies', tags=['movies'],response_model=List[Movies])
def get_movies()->List[Movies]:
    
    return JSONResponse(content=jsonable_encoder(movies))

@app.get('/movies/{id}',tags=['movies'], response_model=Movies)
def get_movie(id:int = Path(ge=1, le=2000))->Movies|list:
    for item in movies:
        if item["id"] == id:
            #return item
            return JSONResponse(content=item)

    return JSONResponse(status_code=404,content=[])
    #return JSONResponse(content=[])

# Sino agrego nada luego del parametro de entrada, la funcion
# Lo toma como una query
@app.get('/movies/', tags=['movies'], status_code=200)
def get_movies_by_category(category:str= Query(max_length=10), year:int = Query(le=2000)):
    movie = list(filter(lambda x: x['category'] == category and x['year'] == year, movies))
    
    return movie

@app.post('/movies',tags=['movies'],response_model=dict ,status_code=201)
# def add_movie(id:int = Body(),title:str= Body(), 
#               overview:str= Body(), year:int= Body(),
#               rating:float= Body(), category:str = Body() ):
def add_movie(movie:Movies=Body())->dict:
    movies.append(movie)
    #return list(movies)
    return JSONResponse(content={"message":"Se ha registrado la pelicula",
                                 "movies":jsonable_encoder(movies)})

# El metodo PUT es idempotente lo cual hace que aunque se vuelva a llamar
# Se va a obtener el mismo resultado

@app.put('/movies/{id}', tags=['movies'],response_model=List[Movies], status_code=200)
# def update_movies(id:int, title:str=Body(), 
#                   overview:str=Body(), year:int=Body(), 
#                   rating:float= Body(), category:str=Body()):
def update_movies(id:int|None =Path(ge=1),movie:Movies = Body()):
    for item in movies:
        if item['id'] == id:
           
            item['title']= movie.title
            item['overview']= movie.overview
            item['year']= movie.year
            item['rating']= movie.rating
            item['category']= movie.category
            
            return JSONResponse(content=jsonable_encoder(movies))

@app.delete('/movies/{id}', tags=['movies'], response_model=List[Movies],status_code=200)
def delete_movies(id:int= Path(le=2000)):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
        
            return JSONResponse(content=jsonable_encoder(movies))

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
