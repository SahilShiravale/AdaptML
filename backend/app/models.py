from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime
from uuid import uuid4

# Assuming Base is defined in database.py
from app.database import Base

class UserRole(enum.Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"

class InteractionType(enum.Enum):
    VIEW = "view"
    CLICK = "click"
    BOOKMARK = "bookmark"
    COMPLETE = "complete"
    RATE = "rate"
    SEARCH = "search"

# Association table for many-to-many relationship between users and courses (for bookmarks/favorites)
user_course_bookmarks = Table(
    'user_course_bookmarks',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('created_at', DateTime, default=func.now())
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    full_name = Column(String(100))
    bio = Column(Text, nullable=True)
    profile_image = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    learning_history = relationship("LearningHistory", back_populates="user")
    interactions = relationship("UserInteraction", back_populates="user")
    bookmarked_courses = relationship("Course", secondary=user_course_bookmarks, back_populates="bookmarked_by")
    # UserCourse relationship is defined with backref in the UserCourse model
    
    def __repr__(self):
        return f"<User {self.username}>"

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    description = Column(Text)
    instructor_name = Column(String(100))
    thumbnail_url = Column(String(255), nullable=True)
    category = Column(String(100), index=True)
    subcategory = Column(String(100), nullable=True)
    difficulty_level = Column(String(20), index=True)  # beginner, intermediate, advanced
    duration_minutes = Column(Integer)
    tags = Column(String(255), nullable=True)  # Comma-separated tags
    price = Column(Float, default=0.0)
    discount_price = Column(Float, nullable=True)
    average_rating = Column(Float, default=0.0)
    total_ratings = Column(Integer, default=0)
    total_students = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    learning_histories = relationship("LearningHistory", back_populates="course")
    interactions = relationship("UserInteraction", back_populates="course")
    bookmarked_by = relationship("User", secondary=user_course_bookmarks, back_populates="bookmarked_courses")
    # UserCourse relationship is defined with backref in the UserCourse model
    
    def __repr__(self):
        return f"<Course {self.title}>"

class LearningHistory(Base):
    __tablename__ = "learning_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    progress_percentage = Column(Float, default=0.0)
    last_accessed_at = Column(DateTime, default=func.now())
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    user_rating = Column(Integer, nullable=True)  # 1-5 rating
    review_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="learning_history")
    course = relationship("Course", back_populates="learning_histories")
    
    def __repr__(self):
        return f"<LearningHistory User={self.user_id} Course={self.course_id}>"

class UserInteraction(Base):
    __tablename__ = "user_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    interaction_type = Column(Enum(InteractionType))
    interaction_data = Column(Text, nullable=True)  # JSON data for additional context
    session_id = Column(String(100), nullable=True)
    timestamp = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="interactions")
    course = relationship("Course", back_populates="interactions")
    
    def __repr__(self):
        return f"<UserInteraction User={self.user_id} Course={self.course_id} Type={self.interaction_type}>"


class UserCourse(Base):
    """
    Model for tracking user course enrollments (learning list).
    This is distinct from LearningHistory as it represents the enrollment relationship
    rather than detailed learning progress and history.
    """
    __tablename__ = "user_courses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    enrolled_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", backref="enrolled_courses")
    course = relationship("Course", backref="enrolled_users")
    
    def __repr__(self):
        return f"<UserCourse User={self.user_id} Course={self.course_id}>"
