from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Task, TaskCreate, Database

app = FastAPI()

# Dependency to obtain the database session
def get_db():
    db = Database()
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

# API routes for CRUD operations

@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = db.TaskModel(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(db.TaskModel).filter(db.TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskCreate, db: Session = Depends(get_db)):
    existing_task = db.query(db.TaskModel).filter(db.TaskModel.id == task_id).first()
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_update.dict().items():
        setattr(existing_task, key, value)
    db.commit()
    db.refresh(existing_task)
    return existing_task

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    existing_task = db.query(db.TaskModel).filter(db.TaskModel.id == task_id).first()
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(existing_task)
    db.commit()
    return existing_task

# Run the application using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)



