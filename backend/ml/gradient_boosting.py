import numpy as np


class GradientBoostingRecommender:
    def __init__(self):
        # Initialize any necessary parameters.
        # TODO: Add actual gradient boosting model initialization (e.g., using xgboost) in the future.
        pass

    def get_recommendations(self, user_id, course_history, limit=5):
        """
        Generate dummy recommendations for a given user.

        Parameters:
            user_id: Identifier for the user.
            course_history: List of courses the user has interacted with.
            limit: Number of recommendations to return.

        Returns:
            List of dictionaries, each containing course_id, score, and a reason.
        """
        # Dummy implementation using numpy to generate random scores.
        # TODO: Replace the dummy logic with actual gradient boosting recommendation logic.
        dummy_courses = [f"course_{i}" for i in range(1, limit + 1)]
        random_scores = np.random.rand(limit)
        dummy_recommendations = []

        for course, score in zip(dummy_courses, random_scores):
            recommendation = {
                "course_id": course,
                "score": float(score),
                "reason": "Dummy recommendation - replace with actual gradient boosting logic."
            }
            dummy_recommendations.append(recommendation)

        return dummy_recommendations
