import random


class ContentBasedRecommender:
    def __init__(self):
        # Constructor to initialize the recommender. Further initialization (e.g., loading course data) can be added here.
        pass

    def get_recommendations(self, user_id, course_history, limit):
        """Return a list of dummy recommendation dictionaries.

        Each recommendation contains:
        - course_id: Identifier of the recommended course (dummy value).
        - score: Dummy relevance score between 0 and 1.
        - reason: Explanation for the recommendation (placeholder text).
        """
        recommendations = []
        for _ in range(limit):
            recommendation = {
                "course_id": f"course_{random.randint(1000, 9999)}",
                "score": round(random.uniform(0, 1), 2),
                "reason": "Placeholder recommendation"
            }
            recommendations.append(recommendation)
        return recommendations

    def get_similar_courses(self, course_id, limit):
        """Return a list of dummy similar courses for a given course_id.

        Each similar course contains:
        - course_id: Modified course id to indicate similarity (dummy value).
        - score: Dummy similarity score between 0 and 1.
        - reason: Explanation for the similarity (placeholder text).
        """
        similar_courses = []
        for _ in range(limit):
            similar_course = {
                "course_id": f"{course_id}_similar_{random.randint(1, 100)}",
                "score": round(random.uniform(0, 1), 2),
                "reason": "Placeholder for similar course"
            }
            similar_courses.append(similar_course)
        return similar_courses
