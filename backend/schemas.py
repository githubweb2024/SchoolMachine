from pydantic import BaseModel
from typing import List

# --- Note schemas ---
class NoteCreate(BaseModel):
    content: str

class Note(BaseModel):
    id: int
    content: str
    class Config:
        orm_mode = True

# --- Lesson schemas ---
class LessonBase(BaseModel):
    title: str
    description: str
    category: str

class LessonCreate(LessonBase):
    pass  # agar alohida yaratish uchun qo‘shimcha maydonlar bo‘lsa shu yerga qo‘shiladi

class Lesson(BaseModel):
    id: int
    title: str
    description: str
    category: str
    notes: List[Note] = []
    class Config:
        orm_mode = True
