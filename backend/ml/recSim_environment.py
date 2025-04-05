"""
RecSim Environment for Learning Recommendation System

This module implements a custom RecSim environment that simulates user-course interactions
for reinforcement learning-based recommendation systems.
"""

import gym
import numpy as np
from gym import spaces
from typing import Dict, List, Tuple, Optional, Any


class User:
    """
    User model representing a learner in the system.
    
    Attributes:
        user_id: Unique identifier for the user
        interests: 5D vector representing user's interest in different topics
        skill_level: User's current skill level
        available_time: Time user can dedicate to learning
        completion_rate: Historical course completion rate
        satisfaction: Overall satisfaction with recommendations
    """
    
    def __init__(
        self, 
        user_id: int, 
        interests: np.ndarray = None, 
        skill_level: float = 0.5,
        available_time: float = 1.0,
        completion_rate: float = 0.7,
        satisfaction: float = 0.5
    ):
        self.user_id = user_id
        # Generate random interests if none provided
        self.interests = interests if interests is not None else np.random.rand(5)
        # Normalize interests to sum to 1
        self.interests = self.interests / np.sum(self.interests)
        self.skill_level = skill_level
        self.available_time = available_time
        self.completion_rate = completion_rate
        self.satisfaction = satisfaction
        self.history = []  # List of course IDs the user has interacted with
        
    def update_after_interaction(self, course, completed: bool):
        """Update user state after interaction with a course"""
        self.history.append(course.course_id)
        
        # Update skill level if course was completed
        if completed:
            # Skill increases more if course difficulty matches user skill level
            skill_match = 1.0 - abs(self.skill_level - course.difficulty)
            self.skill_level = min(1.0, self.skill_level + 0.05 * skill_match)
            
            # Update interests based on course content
            interest_update = 0.05 * course.content_features
            self.interests = (1 - 0.05) * self.interests + interest_update
            self.interests = self.interests / np.sum(self.interests)
            
            # Update completion rate
            self.completion_rate = 0.9 * self.completion_rate + 0.1
            
            # Update satisfaction
            interest_alignment = np.dot(self.interests, course.content_features)
            self.satisfaction = 0.9 * self.satisfaction + 0.1 * interest_alignment
        else:
            # Decrease completion rate and satisfaction if course was not completed
            self.completion_rate = 0.9 * self.completion_rate
            self.satisfaction = 0.9 * self.satisfaction
    
    def will_complete_course(self, course) -> bool:
        """Predict if user will complete the course based on various factors"""
        # Calculate interest alignment
        interest_alignment = np.dot(self.interests, course.content_features)
        
        # Calculate difficulty match (closer to 1 means better match)
        difficulty_match = 1.0 - abs(self.skill_level - course.difficulty)
        
        # Calculate time compatibility
        time_compatibility = 1.0 - abs(self.available_time - course.time_commitment)
        
        # Combine factors with weights
        completion_probability = (
            0.4 * interest_alignment + 
            0.3 * difficulty_match + 
            0.2 * time_compatibility + 
            0.1 * self.completion_rate
        )
        
        # Add some randomness
        completion_probability += np.random.normal(0, 0.1)
        
        # Decide based on probability
        return np.random.random() < completion_probability


class Course:
    """
    Course model representing a learning resource in the system.
    
    Attributes:
        course_id: Unique identifier for the course
        content_features: 5D vector representing course content topics
        difficulty: Course difficulty level (0-1)
        time_commitment: Time required to complete the course
        popularity: Course popularity score
        quality: Course quality rating
    """
    
    def __init__(
        self, 
        course_id: int, 
        content_features: np.ndarray = None, 
        difficulty: float = 0.5,
        time_commitment: float = 0.5,
        popularity: float = 0.5,
        quality: float = 0.7
    ):
        self.course_id = course_id
        # Generate random content features if none provided
        self.content_features = content_features if content_features is not None else np.random.rand(5)
        # Normalize content features to sum to 1
        self.content_features = self.content_features / np.sum(self.content_features)
        self.difficulty = difficulty
        self.time_commitment = time_commitment
        self.popularity = popularity
        self.quality = quality


class RecSimEnv(gym.Env):
    """
    Custom RecSim environment for course recommendations.
    
    This environment simulates user-course interactions for reinforcement learning
    based recommendation systems. It models user interests, course features,
    and the dynamics of user engagement with recommended courses.
    """
    
    metadata = {'render.modes': ['human']}
    
    def __init__(
        self, 
        num_users: int = 100, 
        num_courses: int = 500, 
        max_steps: int = 100,
        observation_dim: int = 15  # Combined dimensions of user and context features
    ):
        super(RecSimEnv, self).__init__()
        
        self.num_users = num_users
        self.num_courses = num_courses
        self.max_steps = max_steps
        self.current_step = 0
        self.observation_dim = observation_dim
        
        # Define action space (selecting a course to recommend)
        self.action_space = spaces.Discrete(num_courses)
        
        # Define observation space (user features + context)
        self.observation_space = spaces.Box(
            low=0, 
            high=1, 
            shape=(observation_dim,), 
            dtype=np.float32
        )
        
        # Initialize users and courses
        self.users = self._initialize_users()
        self.courses = self._initialize_courses()
        
        # Current user and state
        self.current_user_id = None
        self.state = None
        
    def _initialize_users(self) -> Dict[int, User]:
        """Initialize user models"""
        users = {}
        for user_id in range(self.num_users):
            # Create users with random initial attributes
            interests = np.random.rand(5)
            skill_level = np.random.uniform(0.1, 0.9)
            available_time = np.random.uniform(0.2, 1.0)
            completion_rate = np.random.uniform(0.5, 0.9)
            satisfaction = np.random.uniform(0.3, 0.7)
            
            users[user_id] = User(
                user_id=user_id,
                interests=interests,
                skill_level=skill_level,
                available_time=available_time,
                completion_rate=completion_rate,
                satisfaction=satisfaction
            )
        return users
    
    def _initialize_courses(self) -> Dict[int, Course]:
        """Initialize course models"""
        courses = {}
        for course_id in range(self.num_courses):
            # Create courses with random initial attributes
            content_features = np.random.rand(5)
            difficulty = np.random.uniform(0.1, 0.9)
            time_commitment = np.random.uniform(0.2, 1.0)
            popularity = np.random.uniform(0.1, 0.9)
            quality = np.random.uniform(0.3, 0.9)
            
            courses[course_id] = Course(
                course_id=course_id,
                content_features=content_features,
                difficulty=difficulty,
                time_commitment=time_commitment,
                popularity=popularity,
                quality=quality
            )
        return courses
    
    def _get_observation(self) -> np.ndarray:
        """
        Construct the observation vector from current user state and context.
        
        Returns:
            np.ndarray: The observation vector combining user features and context
        """
        user = self.users[self.current_user_id]
        
        # User features (11 dimensions)
        user_features = np.concatenate([
            user.interests,                      # 5D interests
            [user.skill_level],                  # Skill level
            [user.available_time],               # Available time
            [user.completion_rate],              # Completion rate
            [user.satisfaction],                 # Satisfaction
            [len(user.history) / self.max_steps] # Normalized interaction count
        ])
        
        # Context features (4 dimensions) - could be time of day, day of week, etc.
        # Here we just use random values as placeholders
        context_features = np.random.rand(4)
        
        # Combine all features
        observation = np.concatenate([user_features, context_features])
        
        return observation.astype(np.float32)
    
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict]:
        """
        Take a step in the environment by recommending a course (action) to the current user.
        
        Args:
            action: Course ID to recommend
            
        Returns:
            observation: New state observation
            reward: Reward for the action
            done: Whether the episode is finished
            info: Additional information
        """
        assert self.action_space.contains(action), f"Invalid action: {action}"
        
        # Get current user and recommended course
        user = self.users[self.current_user_id]
        course = self.courses[action]
        
        # Check if course has already been recommended to this user
        if action in user.history:
            reward = -0.5  # Penalty for recommending the same course
            completed = False
        else:
            # Determine if user completes the course
            completed = user.will_complete_course(course)
            
            # Assign reward based on completion
            if completed:
                reward = 1.0  # Reward for course completion
            else:
                reward = -1.0  # Penalty for dropout
            
            # Update user state based on interaction
            user.update_after_interaction(course, completed)
        
        # Increment step counter
        self.current_step += 1
        
        # Check if episode is done
        done = self.current_step >= self.max_steps
        
        # Update state
        self.state = self._get_observation()
        
        # Additional info
        info = {
            'user_id': self.current_user_id,
            'course_id': action,
            'completed': completed,
            'user_satisfaction': user.satisfaction,
            'step': self.current_step
        }
        
        return self.state, reward, done, info
    
    def reset(self) -> np.ndarray:
        """
        Reset the environment to start a new episode.
        
        Returns:
            np.ndarray: Initial observation
        """
        # Reset step counter
        self.current_step = 0
        
        # Select a random user for this episode
        self.current_user_id = np.random.randint(0, self.num_users)
        
        # Get initial state
        self.state = self._get_observation()
        
        return self.state
    
    def render(self, mode='human'):
        """
        Render the environment.
        
        Args:
            mode: Rendering mode
        """
        if mode == 'human':
            user = self.users[self.current_user_id]
            print(f"Step: {self.current_step}/{self.max_steps}")
            print(f"User ID: {self.current_user_id}")
            print(f"Interests: {user.interests}")
            print(f"Skill Level: {user.skill_level:.2f}")
            print(f"Completion Rate: {user.completion_rate:.2f}")
            print(f"Satisfaction: {user.satisfaction:.2f}")
            print(f"History: {user.history}")
            print("-" * 50)
    
    def seed(self, seed=None):
        """Set random seed for reproducibility"""
        np.random.seed(seed)
        return [seed]