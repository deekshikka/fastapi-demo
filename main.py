from fastapi import FastAPI,Depends,HTTPException
from schemas import TodoCreate,TodoUpdate as ToDoSchema
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Todo
from database import Base,engine


Base.metadata.create_all(bind=engine)
app = FastAPI()

#Dependency for DB session
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

#POST - create TODO

@app.post("/todo",response_model=ToDoSchema)
def create(todo:TodoCreate,db: Session = Depends(get_db)):
    db_todo=Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

#GET - All TODOS
@app.get("/todo",response_model=list[ToDoSchema])
def read_all(db: Session = Depends(get_db)):
    todos=db.query(Todo).all()
    return todos

#GET - TODO by ID
@app.get("/todo/{id}",response_model=ToDoSchema)
def read_one(id:int,db: Session = Depends(get_db)):
    todos=db.query(Todo).filter_by(id=id).first()
    if not todos:
        raise HTTPException(status_code=404,detail=f"Todo with id {id} not found")
    else:
        return todos

#PUT - Update TODO by ID
@app.put("/todo/{id}",response_model=ToDoSchema)
def update(id:int, todo:TodoCreate,db: Session = Depends(get_db)):
    todos=db.query(Todo).filter_by(id=id).first()
    if not todos:
        raise HTTPException(status_code=404,detail=f"Todo with id {id} not found")
    for key,value in todo.dict().items():
        setattr(todos,key,value)
    db.commit()
    db.refresh(todos)
    return todos
 
#DELETE - Delete TODO by ID
@app.delete("/todo/{id}")
def delete_todo(id:int,db: Session = Depends(get_db)):
    todos=db.query(Todo).filter_by(id=id).first()
    if not todos:
        raise HTTPException(status_code=404,detail=f"Todo with id {id} not found")
    db.delete(todos)
    db.commit()
    return {"detail":f"Todo with id {id} deleted successfully"}