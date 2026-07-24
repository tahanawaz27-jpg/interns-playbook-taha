'''
Task Manager API — starter codebase

A tiny task-tracking API. Users can create tasks assigned to them,
list their tasks, and delete tasks.

Everything lives in this one file for now. Run it with:
    uvicorn main:app --reload

Then check out the interactive docs at http://127.0.0.1:8000/docs
'''

from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,EmailStr,Field
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship

# --- database setup ---

DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- models ---

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Integer, default=1)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="tasks")


Base.metadata.create_all(bind=engine)


# --- schemas ---

class UserCreate(BaseModel):
    name: str=Field(min_length=3,max_length=50)
    email: EmailStr


class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str=Field(max_length=50)
    description: Optional[str] = None
    priority: int = 1
    user_id: int=Field(gt=0)


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: int
    completed: bool
    user_id: int

    class Config:
        from_attributes = True


# --- app setup ---

app = FastAPI(title="Task Manager API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- routes ---

@app.post("/users", response_model=UserOut)
def create_user(user: UserCreate):
    db = SessionLocal()
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/tasks", response_model=TaskOut)
def create_task(task: TaskCreate):
    db = SessionLocal()
    user = db.query(User).filter(User.id == task.user_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        user_id=task.user_id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.close()
    return new_task


@app.get("/tasks/{user_id}", response_model=List[TaskOut])
def get_tasks_for_user(user_id: int):
    # returns a user's tasks
    db = SessionLocal()
    tasks = db.query(Task).filter(user_id==Task.user_id)
    db.close()
    return tasks


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    db.close()
    return {"detail": "Task deleted"}

@app.delete("/User/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    db.query(Task).filter(Task.user_id==user_id).delete()
    db.delete(user)
    db.commit()
    db.close()
    return {"detail": f"User and Task deleted for user_id: {user_id}"}

@app.get("/")
def root():
    return {"message": "Task Manager API is running"}