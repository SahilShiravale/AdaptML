# AI-Powered Learning Recommendation System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/yourusername/AI-Recommendation/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/yourusername/AI-Recommendation/actions/workflows/ci-cd.yml)

## Overview

This project is an AI-powered learning recommendation system that provides personalized course and learning material recommendations to users based on their preferences, learning history, and behavior. The system uses a hybrid recommendation approach combining collaborative filtering, content-based filtering, and reinforcement learning with RecSim to continuously improve recommendation quality.

Key features:
- Personalized learning recommendations
- User behavior tracking and analysis
- Adaptive recommendation engine that improves over time
- Interactive UI with course carousels and detailed information
- User dashboard with learning progress and recommendation insights

## Architecture

The application follows a modern microservices architecture with three main components:

### Frontend
- Built with Next.js (React) and Tailwind CSS
- Responsive design with interactive components
- User authentication and profile management
- Dashboard for tracking learning progress
- Course exploration and recommendation interfaces

### Backend
- FastAPI for RESTful API and WebSocket support
- PostgreSQL database with SQLAlchemy ORM
- Redis for caching and session management
- JWT authentication and OAuth integration
- API endpoints for user management, courses, and recommendations

### Machine Learning
- Hybrid recommendation engine combining multiple approaches:
  - Collaborative filtering for user similarity-based recommendations
  - Content-based filtering for course attribute matching
  - Gradient boosting for feature-based recommendations
  - Reinforcement learning with RecSim for adaptive recommendations
- Continuous model training and evaluation pipeline

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Git
- Node.js 16+ (for local frontend development)
- Python 3.9+ (for local backend development)
- PostgreSQL (optional for local development without Docker)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AI-Recommendation.git
   cd AI-Recommendation
   ```

2. Set up environment variables:
   ```bash
   cp .env.backend.example .env.backend
   cp .env.frontend.example .env.frontend
   ```
   
   **Important:** Edit the `.env.backend` and `.env.frontend` files with your configuration. For production environments, ensure you use secure values for secrets, API keys, and database credentials.

3. Install dependencies (for local development):
   
   Frontend:
   ```bash
   cd frontend
   npm install
   ```
   
   Backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## Running Locally

There are two ways to run the project:

### 1. Using Docker (recommended)

Start all services with Docker Compose:

```bash
docker-compose up --build
```

This will build and start the frontend, backend, PostgreSQL database, Redis, and other required services.

### 2. Manual Setup

1. Start the backend:
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

**Note:** For development, the backend runs with `--reload` flag and debugging enabled. In production environments, ensure `DEBUG=False` in your environment configuration to enhance security and performance.

## Deployment

The project supports multiple deployment workflows:

### Docker Deployment

1. Build and push Docker images:
   ```bash
   docker-compose build
   docker tag ai-recommendation-frontend:latest yourusername/ai-recommendation-frontend:latest
   docker tag ai-recommendation-backend:latest yourusername/ai-recommendation-backend:latest
   docker push yourusername/ai-recommendation-frontend:latest
   docker push yourusername/ai-recommendation-backend:latest
   ```

2. Deploy using Docker Compose on your server:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

   **Important:** Ensure all environment variables in `.env.backend` and `.env.frontend` are configured with secure production values before deployment, and that `DEBUG=False` is set.

### Cloud Deployment

The project includes CI/CD workflows for GitHub Actions that can deploy to various cloud providers:

1. AWS Deployment:
   - Configure AWS credentials in GitHub repository secrets
   - Push to the `main` branch to trigger deployment
   - The workflow will build, test, and deploy to AWS ECS or EKS

2. Azure/GCP:
   - Similar workflows are available for Azure and GCP
   - Configure the appropriate credentials in GitHub secrets

**Note:** Regardless of deployment method, always ensure that development settings (like `DEBUG=True`) are turned off in production environments to enhance security.

## Developer Guidelines

### Code Style

- Frontend: Follow the Airbnb JavaScript Style Guide
- Backend: Follow PEP 8 style guide for Python code
- Use ESLint and Prettier for JavaScript/TypeScript
- Use Black and isort for Python

### Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `release/*`: Release preparation

### Testing

- Write unit tests for all new features
- Maintain minimum 80% code coverage
- Run tests locally before pushing:
  ```bash
  # Frontend
  cd frontend
  npm test
  
  # Backend
  cd backend
  pytest
  ```

## RecSim Integration Guide

The recommendation system uses RecSim to simulate user interactions and train reinforcement learning models for adaptive recommendations.

### RecSim Environment

The RecSim environment is defined in `backend/ml/recSim_environment.py` and models:
- User states (preferences, history, skills)
- Course items (content, difficulty, topics)
- Reward functions based on user engagement and learning outcomes

### Recommendation Models

The system uses a hybrid approach with multiple recommendation strategies:

1. **Collaborative Filtering**:
   - User-based: Recommends courses based on similar users' preferences
   - Item-based: Recommends courses similar to those the user has engaged with

2. **Content-Based Filtering**:
   - Matches user preferences with course attributes
   - Uses NLP for processing course descriptions and extracting features

3. **Reinforcement Learning with RecSim**:
   - Agent: Stable-Baselines3 PPO algorithm
   - State: User profile, history, and context
   - Actions: Course recommendations
   - Rewards: User engagement, completion rates, and learning outcomes

### Training Pipeline

The training pipeline in `backend/ml/training.py`:
1. Collects user interaction data
2. Preprocesses data for model training
3. Trains the recommendation models
4. Evaluates model performance
5. Deploys the best-performing model

### Integration Points

- **API Integration**: The trained models are exposed via the `/recommendations` API endpoint
- **Real-time Updates**: WebSockets provide real-time recommendation updates
- **Feedback Loop**: User interactions are logged and fed back into the training pipeline
- **A/B Testing**: Different recommendation strategies can be tested simultaneously

### Monitoring and Evaluation

- Track recommendation quality metrics (CTR, engagement, completion)
- Monitor model drift and performance degradation
- Regularly retrain models with new interaction data

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
