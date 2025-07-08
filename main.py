from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Annotated ,Optional
import json


app = FastAPI()

class book_pydnatic(BaseModel):

    id : Annotated[int,Field(...,description='Enter the book id',examples=["Related to programing"])]
    title: Annotated[str,Field(...,description="Enter the book name",examples=["FastAPI for Beginners"])]
    author: Annotated[str,Field(...,description="Enter the auther name",examples=["John Doe"])]
    year : Annotated[int,Field(...,description="Enter the year",examples=[2021])]
    genre : Annotated[str,Field(...,description="Enter the genre",examples=["Programming"])]
    available :Annotated[bool,Field(...,description="enter the type",examples=[True])]

#this is class for validation of the data which is comming for put from user
class book_update_pydantic(BaseModel):
    title :Annotated[Optional[str],Field(default=None)]
    author :Annotated[Optional[str],Field(default=None)]
    year :Annotated[Optional[int],Field(default=None)]
    genre : Annotated[Optional[str],Field(default=None)]
    available : Annotated[Optional[bool],Field(default=None)]




@app.get("/")
def read_root():
    return {"Message":"Welcome to book invontry system"}

def load_data():
    try:
        with open('book.json', 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []  # empty list fallback
    
def save_data(data):
    with open('book.json','w') as f:
        json.dump(data, f)
            

#Route to get the all data of the books
@app.get("/book_store/Whole_data")
def whole_data():
    data = load_data()
    return data

#Route to get the specific Book data 

@app.get('/specific_book/{book_id}')
def Get_specific_book(book_id : int):
    books = load_data()   # load_data returns the LIST directly

    for book in books:
        if book["id"] == book_id:
            return book

    return {'message': "This book is not found in the database"}

@app.post('/new_entry')
def new_book_add(new_data:book_pydnatic):
    
    data = load_data()

    if new_data.id in [book['id'] for book in data]:
        return {'message': "This book id already exists"}

    data.append(new_data.dict()) #.dict is pydantic funcation to convert pydantic model to dict
    with open('book.json', 'w') as f:
        json.dump(data, f)

@app.put('/update_book/{book_id}')
def update_book(book_id: int, updated_data: book_update_pydantic):
    data = load_data()

    # Find if the book exists
    if book_id not in [book['id'] for book in data]:
        return {'message': "This book id does not exist in our database"}

    # Find the exact book dict
    for book in data:
        if book['id'] == book_id:
            existing_data = book
            break

    # Update the fields that are given
    update_data = updated_data.dict(exclude_unset=True)
    for key, val in update_data.items():
        existing_data[key] = val

    save_data(data)

    return {'message': "Book updated successfully", 'book': existing_data}


@app.delete('/delete/{delete_id}')
def delete_id(delete_id: int):
    data = load_data()

    if delete_id not in [book['id'] for book in data]:
        return {'message': 'This book is not found in data'}

    # Remove the book by filtering
    data = [book for book in data if book['id'] != delete_id]

    save_data(data)

    return {'message': 'Book deleted successfully'}