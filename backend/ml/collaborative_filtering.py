import numpy as np


class CollaborativeFilteringRecommender:
    """Stub class for Collaborative Filtering Recommendation System. This is a placeholder implementation using dummy data."""

    def __init__(self):
        # Initialization placeholder (if any initialization is needed, implement here)
        pass

    def get_recommendations(self, user_id, course_history, limit):
        """
        Returns a list of dummy recommendation dictionaries for a given user based on his/her course history.
        Each recommendation is a dictionary with keys: 'course_id', 'score', and 'reason'.
        """
        recommendations = []
        for _ in range(limit):
            dummy_course_id = int(np.random.randint(1000, 9999))  # Dummy course ID
            dummy_score = float(np.random.uniform(0, 1))            # Dummy score between 0 and 1
            recommendation = {
                'course_id': dummy_course_id,
                'score': dummy_score,
                'reason': 'Based on your course history'  # Placeholder reason
            }
            recommendations.append(recommendation)
        return recommendations

    def get_trending_recommendations(self, time_period, limit):
        """
        Returns a list of dummy trending recommendation dictionaries for a given time period.
        Each recommendation is a dictionary with keys: 'course_id', 'score', and 'reason'.
        """
        trending = []
        for _ in range(limit):
            dummy_course_id = int(np.random.randint(1000, 9999))
            dummy_score = float(np.random.uniform(0, 1))
            recommendation = {
                'course_id': dummy_course_id,
                'score': dummy_score,
                'reason': 'Trending course'  # Placeholder reason
            }
            trending.append(recommendation)
        return trending

    def get_recommendations_based_on_course(self, user_id, course_id, limit):
        """
        Returns a list of dummy recommendations based on a specific course for a given user.
        Each recommendation is a dictionary with keys: 'course_id', 'score', and 'reason'.
        """
        recommendations = []
        for _ in range(limit):
            dummy_course_id = int(np.random.randint(1000, 9999))
            dummy_score = float(np.random.uniform(0, 1))
            recommendation = {
                'course_id': dummy_course_id,
                'score': dummy_score,
                'reason': f"Because you showed interest in course {course_id}"  # Placeholder reason
            }
            recommendations.append(recommendation)
        return recommendations
