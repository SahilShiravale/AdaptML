from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from enum import Enum
import numpy as np

from app.database import get_db
from app.models import User, Course, UserCourseInteraction
from app.routes.auth import get_current_user

# Import recommendation engines
from ml.collaborative_filtering import CollaborativeFilteringRecommender
from ml.content_based import ContentBasedRecommender
from ml.gradient_boosting import GradientBoostingRecommender
from ml.reinforcement_learning import RLRecommender

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
    responses={404: {"description": "Not found"}},
)

class RecommendationMethod(str, Enum):
    COLLABORATIVE = "collaborative"
    CONTENT_BASED = "content_based"
    GRADIENT_BOOSTING = "gradient_boosting"
    REINFORCEMENT_LEARNING = "reinforcement_learning"
    HYBRID = "hybrid"

# Initialize recommenders
collaborative_recommender = CollaborativeFilteringRecommender()
content_based_recommender = ContentBasedRecommender()
gradient_boosting_recommender = GradientBoostingRecommender()
rl_recommender = RLRecommender()

def standardize_recommendations(recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Standardize recommendation outputs to ensure consistent format for UI consumption.
    
    Args:
        recommendations: List of recommendation dictionaries
        
    Returns:
        List of standardized recommendation dictionaries
    """
    standardized = []
    
    for rec in recommendations:
        # Ensure each recommendation has required fields
        standardized_rec = {
            "course_id": rec.get("course_id"),
            "score": float(rec.get("score", 0.0)),
            "reason": rec.get("reason", ""),
            "method": rec.get("method", "unknown")
        }
        standardized.append(standardized_rec)
    
    return standardized

def aggregate_recommendations(recommendations_by_method: Dict[str, List[Dict[str, Any]]], 
                             limit: int = 10) -> List[Dict[str, Any]]:
    """
    Aggregate recommendations from different methods using a weighted approach.
    
    Args:
        recommendations_by_method: Dictionary mapping method names to recommendation lists
        limit: Maximum number of recommendations to return
        
    Returns:
        List of aggregated recommendations
    """
    # Define weights for each method
    weights = {
        RecommendationMethod.COLLABORATIVE: 0.3,
        RecommendationMethod.CONTENT_BASED: 0.2,
        RecommendationMethod.GRADIENT_BOOSTING: 0.2,
        RecommendationMethod.REINFORCEMENT_LEARNING: 0.3
    }
    
    # Create a dictionary to store aggregated scores by course_id
    aggregated_scores = {}
    
    # Process recommendations from each method
    for method, recs in recommendations_by_method.items():
        if method not in weights:
            continue
            
        method_weight = weights[method]
        
        for rank, rec in enumerate(recs):
            course_id = rec["course_id"]
            score = rec["score"]
            
            # Apply method weight and rank penalty
            weighted_score = score * method_weight
            
            if course_id not in aggregated_scores:
                aggregated_scores[course_id] = {
                    "course_id": course_id,
                    "score": 0,
                    "methods": [],
                    "reasons": []
                }
            
            aggregated_scores[course_id]["score"] += weighted_score
            aggregated_scores[course_id]["methods"].append(method)
            
            if "reason" in rec and rec["reason"]:
                aggregated_scores[course_id]["reasons"].append(rec["reason"])
    
    # Convert to list and sort by score
    result = list(aggregated_scores.values())
    result.sort(key=lambda x: x["score"], reverse=True)
    
    # Limit results and format
    result = result[:limit]
    
    # Format final recommendations
    final_recommendations = []
    for rec in result:
        # Join methods and reasons
        methods = list(set(rec["methods"]))
        reasons = list(set(rec["reasons"]))
        
        final_rec = {
            "course_id": rec["course_id"],
            "score": rec["score"],
            "method": "hybrid",
            "reason": "; ".join(reasons) if reasons else "Multiple recommendation methods suggest this course"
        }
        final_recommendations.append(final_rec)
    
    return final_recommendations

@router.get("/", response_model=List[Dict[str, Any]])
async def get_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    method: Optional[RecommendationMethod] = Query(RecommendationMethod.HYBRID, description="Recommendation method to use"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of recommendations to return"),
    category_id: Optional[int] = Query(None, description="Filter recommendations by category ID"),
    difficulty: Optional[str] = Query(None, description="Filter recommendations by difficulty level")
):
    """
    Get course recommendations for the current user.
    
    Args:
        method: Recommendation method to use
        limit: Maximum number of recommendations to return
        category_id: Optional category filter
        difficulty: Optional difficulty level filter
        
    Returns:
        List of recommended courses
    """
    try:
        # Get user's course history
        user_interactions = db.query(UserCourseInteraction).filter(
            UserCourseInteraction.user_id == current_user.id
        ).all()
        
        # Extract course IDs and ratings
        course_history = {
            interaction.course_id: interaction.rating 
            for interaction in user_interactions
        }
        
        # Get recommendations based on the specified method
        if method == RecommendationMethod.COLLABORATIVE:
            recommendations = collaborative_recommender.get_recommendations(
                user_id=current_user.id,
                course_history=course_history,
                limit=limit
            )
            for rec in recommendations:
                rec["method"] = RecommendationMethod.COLLABORATIVE
                
        elif method == RecommendationMethod.CONTENT_BASED:
            recommendations = content_based_recommender.get_recommendations(
                user_id=current_user.id,
                course_history=course_history,
                limit=limit
            )
            for rec in recommendations:
                rec["method"] = RecommendationMethod.CONTENT_BASED
                
        elif method == RecommendationMethod.GRADIENT_BOOSTING:
            recommendations = gradient_boosting_recommender.get_recommendations(
                user_id=current_user.id,
                course_history=course_history,
                limit=limit
            )
            for rec in recommendations:
                rec["method"] = RecommendationMethod.GRADIENT_BOOSTING
                
        elif method == RecommendationMethod.REINFORCEMENT_LEARNING:
            recommendations = rl_recommender.get_recommendations(
                user_id=current_user.id,
                course_history=course_history,
                limit=limit
            )
            for rec in recommendations:
                rec["method"] = RecommendationMethod.REINFORCEMENT_LEARNING
                
        elif method == RecommendationMethod.HYBRID:
            # Get recommendations from all methods
            collaborative_recs = collaborative_recommender.get_recommendations(
                user_id=current_user.id,
                course_history=course_history,
                limit=limit
            )
            
            content_based_recs = content_based_recommender.get_recommendations(
                user_id=current_user.id,
                course_history=course_history,
                limit=limit
            )
            
            gradient_boosting_recs = gradient_boosting_recommender.get_recommendations(
                user_id=current_user.id,
                course_history=course_history,
                limit=limit
            )
            
            rl_recs = rl_recommender.get_recommendations(
                user_id=current_user.id,
                course_history=course_history,
                limit=limit
            )
            
            # Aggregate recommendations
            recommendations_by_method = {
                RecommendationMethod.COLLABORATIVE: collaborative_recs,
                RecommendationMethod.CONTENT_BASED: content_based_recs,
                RecommendationMethod.GRADIENT_BOOSTING: gradient_boosting_recs,
                RecommendationMethod.REINFORCEMENT_LEARNING: rl_recs
            }
            
            recommendations = aggregate_recommendations(recommendations_by_method, limit=limit)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid recommendation method: {method}")
        
        # Standardize recommendations
        standardized_recommendations = standardize_recommendations(recommendations)
        
        # Apply filters if specified
        if category_id is not None or difficulty is not None:
            filtered_recommendations = []
            
            # Get course details for filtering
            course_ids = [rec["course_id"] for rec in standardized_recommendations]
            courses = db.query(Course).filter(Course.id.in_(course_ids)).all()
            course_details = {course.id: course for course in courses}
            
            for rec in standardized_recommendations:
                course = course_details.get(rec["course_id"])
                if not course:
                    continue
                    
                # Apply category filter
                if category_id is not None and course.category_id != category_id:
                    continue
                    
                # Apply difficulty filter
                if difficulty is not None and course.difficulty != difficulty:
                    continue
                    
                filtered_recommendations.append(rec)
                
            standardized_recommendations = filtered_recommendations
        
        # Limit results to requested number
        return standardized_recommendations[:limit]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@router.get("/personalized-for-you", response_model=List[Dict[str, Any]])
async def get_personalized_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of recommendations to return")
):
    """
    Get highly personalized recommendations using the hybrid approach with emphasis on user history.
    
    Args:
        limit: Maximum number of recommendations to return
        
    Returns:
        List of personalized recommended courses
    """
    try:
        # This endpoint always uses the hybrid method with custom weights
        return await get_recommendations(
            db=db,
            current_user=current_user,
            method=RecommendationMethod.HYBRID,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating personalized recommendations: {str(e)}")

@router.get("/trending", response_model=List[Dict[str, Any]])
async def get_trending_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of recommendations to return"),
    time_period: str = Query("week", description="Time period for trending courses (day, week, month)")
):
    """
    Get trending course recommendations based on recent popularity.
    
    Args:
        limit: Maximum number of recommendations to return
        time_period: Time period for trending calculation
        
    Returns:
        List of trending recommended courses
    """
    try:
        # Get trending courses from collaborative filtering with recency bias
        trending_recommendations = collaborative_recommender.get_trending_recommendations(
            time_period=time_period,
            limit=limit
        )
        
        for rec in trending_recommendations:
            rec["method"] = "trending"
            rec["reason"] = f"Popular in the last {time_period}"
            
        # Standardize recommendations
        standardized_recommendations = standardize_recommendations(trending_recommendations)
        
        return standardized_recommendations[:limit]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating trending recommendations: {str(e)}")

@router.get("/similar-to/{course_id}", response_model=List[Dict[str, Any]])
async def get_similar_courses(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of recommendations to return")
):
    """
    Get courses similar to the specified course.
    
    Args:
        course_id: ID of the reference course
        limit: Maximum number of recommendations to return
        
    Returns:
        List of similar courses
    """
    try:
        # Check if course exists
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail=f"Course with ID {course_id} not found")
            
        # Get similar courses using content-based filtering
        similar_courses = content_based_recommender.get_similar_courses(
            course_id=course_id,
            limit=limit
        )
        
        for rec in similar_courses:
            rec["method"] = "content_based"
            rec["reason"] = f"Similar to {course.title}"
            
        # Standardize recommendations
        standardized_recommendations = standardize_recommendations(similar_courses)
        
        return standardized_recommendations[:limit]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding similar courses: {str(e)}")

@router.get("/because-you-liked/{course_id}", response_model=List[Dict[str, Any]])
async def get_recommendations_based_on_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of recommendations to return")
):
    """
    Get recommendations based on a specific course the user liked.
    
    Args:
        course_id: ID of the course the user liked
        limit: Maximum number of recommendations to return
        
    Returns:
        List of recommended courses
    """
    try:
        # Check if course exists
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail=f"Course with ID {course_id} not found")
            
        # Get recommendations from multiple methods
        collaborative_recs = collaborative_recommender.get_recommendations_based_on_course(
            user_id=current_user.id,
            course_id=course_id,
            limit=limit
        )
        
        content_based_recs = content_based_recommender.get_similar_courses(
            course_id=course_id,
            limit=limit
        )
        
        # Combine and weight recommendations
        recommendations_by_method = {
            RecommendationMethod.COLLABORATIVE: collaborative_recs,
            RecommendationMethod.CONTENT_BASED: content_based_recs
        }
        
        # Custom weights for this specific recommendation type
        weights = {
            RecommendationMethod.COLLABORATIVE: 0.4,
            RecommendationMethod.CONTENT_BASED: 0.6
        }
        
        # Aggregate recommendations
        recommendations = []
        
        # Process recommendations from each method
        for method, recs in recommendations_by_method.items():
            method_weight = weights[method]
            
            for rec in recs:
                rec["score"] = rec.get("score", 0) * method_weight
                rec["method"] = method
                rec["reason"] = f"Because you liked {course.title}"
                recommendations.append(rec)
        
        # Sort by score and limit
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        recommendations = recommendations[:limit]
        
        # Standardize recommendations
        standardized_recommendations = standardize_recommendations(recommendations)
        
        return standardized_recommendations
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@router.get("/next-steps", response_model=List[Dict[str, Any]])
async def get_next_step_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(5, ge=1, le=20, description="Maximum number of recommendations to return")
):
    """
    Get recommendations for the next courses to take based on learning path analysis.
    
    Args:
        limit: Maximum number of recommendations to return
        
    Returns:
        List of recommended next steps
    """
    try:
        # Get user's completed courses
        completed_interactions = db.query(UserCourseInteraction).filter(
            UserCourseInteraction.user_id == current_user.id,
            UserCourseInteraction.completed == True
        ).all()
        
        completed_course_ids = [interaction.course_id for interaction in completed_interactions]
        
        # Use RL recommender for next steps as it's designed for sequential decision making
        next_steps = rl_recommender.get_next_step_recommendations(
            user_id=current_user.id,
            completed_course_ids=completed_course_ids,
            limit=limit
        )
        
        for rec in next_steps:
            rec["method"] = "reinforcement_learning"
            rec["reason"] = "Recommended next step in your learning journey"
            
        # Standardize recommendations
        standardized_recommendations = standardize_recommendations(next_steps)
        
        return standardized_recommendations[:limit]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating next step recommendations: {str(e)}")

@router.get("/explore", response_model=List[Dict[str, Any]])
async def get_exploration_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of recommendations to return")
):
    """
    Get recommendations that encourage exploration of new topics and skills.
    
    Args:
        limit: Maximum number of recommendations to return
        
    Returns:
        List of exploration recommendations
    """
    try:
        # Get user's course history
        user_interactions = db.query(UserCourseInteraction).filter(
            UserCourseInteraction.user_id == current_user.id
        ).all()
        
        # Extract course IDs
        course_history = {interaction.course_id for interaction in user_interactions}
        
        # Use a mix of methods with emphasis on diversity
        exploration_recs = rl_recommender.get_exploration_recommendations(
            user_id=current_user.id,
            course_history=course_history,
            limit=limit
        )
        
        for rec in exploration_recs:
            rec["method"] = "exploration"
            rec["reason"] = "Expand your knowledge into new areas"
            
        # Standardize recommendations
        standardized_recommendations = standardize_recommendations(exploration_recs)
        
        return standardized_recommendations[:limit]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating exploration recommendations: {str(e)}")