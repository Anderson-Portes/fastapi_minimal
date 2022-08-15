from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

class Person(BaseModel):
  id: Optional[int] = None
  name: str
  age: int
  gender: str
  employed: bool

with open('database.json', 'r') as data:
  people = json.load(data)['people']

app = FastAPI()

@app.get('/')
def index():
  return people

@app.get('/{id}', status_code=200)
def get_person(id: int):
  person = [p for p in people if p['id'] == id]

  return person[0] if len(person) > 0 else {}

@app.post('/', status_code=200)
def add_person(person: Person):
  id = max([p['id'] for p in people]) + 1

  new_person = {
    "id": id,
    "name": person.name,
    "age": person.age,
    "gender": person.gender,
    "employed": person.employed
  }

  people.append(new_person)

  with open('database.json', 'w') as data:
    json.dump({ "people": people }, data)
  
  return new_person

@app.put('/{id}', status_code=200)
def update_person(id: int, person: Person):
  new_person = {
    "id": id,
    "name": person.name,
    "age": person.age,
    "gender": person.gender,
    "employed": person.employed
  }

  person_list = [p for p in people if p['id'] == id]

  if len(person_list) > 0:
    people.remove(person_list[0])
    people.append(new_person)
    
    with open('database.json', 'w') as data:
      json.dump({ "people": people }, data)

    return new_person
  
  return HTTPException(status_code=404, detail=f"Person with id {id} does not exists!")

@app.delete('/{id}', status_code=200)
def delete_person(id: int):
  person_list = [p for p in people if p['id'] == id]

  if len(person_list) > 0:
    people.remove(person_list[0])

    with open('database.json', 'w') as data:
      json.dump({ "people": people }, data)

    return { "message": "Person deleted successfully!" }

  return HTTPException(status_code=404, detail=f"Person with id {id} does not exists!")