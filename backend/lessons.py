from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import Lesson, Note
from .schemas import LessonCreate, Lesson as LessonSchema, LessonBase, NoteCreate, Note as NoteSchema

router = APIRouter(prefix="/lessons", tags=["Lessons"])

@router.get("/", response_model=list[LessonSchema])
def get_lessons(db: Session = Depends(get_db)):
    return db.query(Lesson).all()

@router.post("/", response_model=LessonSchema)
def create_lesson(lesson: LessonBase, db: Session = Depends(get_db)):
    db_lesson = Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

@router.delete("/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db.delete(lesson)
    db.commit()
    return {"message": "Lesson o‘chirildi"}

@router.get("/{lesson_id}", response_model=LessonSchema)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.post("/{lesson_id}/notes", response_model=NoteSchema)
def add_note(lesson_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db_note = Note(content=note.content, lesson_id=lesson_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
    
