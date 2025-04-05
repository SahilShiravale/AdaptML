from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

# Assuming these imports based on project structure
from ..database import get_db
from ..models import Course, User, UserCourse
from .auth import get_current_user

router = APIRouter(
    prefix="/courses",
    tags=["courses"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models for request/response
class CourseBase(BaseModel):
    title: str
    description: str
    category: str
    difficulty: str
    duration: int  # in minutes
    instructor: str
    image_url: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    rating: Optional[float] = None
    
    class Config:
        orm_mode = True

class UserCourseCreate(BaseModel):
    course_id: int

@router.get("/", response_model=List[CourseResponse])
def list_courses(
    skip: int = 0, 
    limit: int = 100, 
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all available courses with optional filtering by category and difficulty.
    """
    query = db.query(Course)
    
    if category:
        query = query.filter(Course.category == category)
    
    if difficulty:
        query = query.filter(Course.difficulty == difficulty)
    
    courses = query.offset(skip).limit(limit).all()
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific course.
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course

@router.post("/learning-list", status_code=status.HTTP_201_CREATED)
def add_to_learning_list(
    course_data: UserCourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a course to the user's learning list.
    """
    # Check if course exists
    course = db.query(Course).filter(Course.id == course_data.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if course is already in user's learning list
    existing = db.query(UserCourse).filter(
        UserCourse.user_id == current_user.id,
        UserCourse.course_id == course_data.course_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course already in learning list"
        )
    
    # Add course to user's learning list
    user_course = UserCourse(
        user_id=current_user.id,
        course_id=course_data.course_id,
        progress=0,  # Initial progress is 0%
        completed=False
    )
    
    db.add(user_course)
    db.commit()
    
    return {"message": "Course added to learning list successfully"}

@router.delete("/learning-list/{course_id}", status_code=status.HTTP_200_OK)
def remove_from_learning_list(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove a course from the user's learning list.
    """
    user_course = db.query(UserCourse).filter(
        UserCourse.user_id == current_user.id,
        UserCourse.course_id == course_id
    ).first()
    
    if not user_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found in learning list"
        )
    
    db.delete(user_course)
    db.commit()
    
    return {"message": "Course removed from learning list successfully"}

@router.get("/learning-list", response_model=List[CourseResponse])
def get_learning_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all courses in the user's learning list.
    """
    user_courses = db.query(UserCourse).filter(
        UserCourse.user_id == current_user.id
    ).all()
    
    course_ids = [uc.course_id for uc in user_courses]
    courses = db.query(Course).filter(Course.id.in_(course_ids)).all()
    
    return courses

@router.put("/learning-list/{course_id}/progress", status_code=status.HTTP_200_OK)
def update_course_progress(
    course_id: int,
    progress: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update the progress of a course in the user's learning list.
    Progress is a percentage value between 0 and 100.
    """
    if progress < 0 or progress > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Progress must be between 0 and 100"
        )
    
    user_course = db.query(UserCourse).filter(
        UserCourse.user_id == current_user.id,
        UserCourse.course_id == course_id
    ).first()
    
    if not user_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found in learning list"
        )
    
    user_course.progress = progress
    user_course.completed = (progress == 100)
    
    db.commit()
    
    return {"message": "Course progress updated successfully"}