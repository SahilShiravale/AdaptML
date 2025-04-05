# RUNNING.md

## Environment Setup

1. Copy the example environment file:
   - For the frontend, run: `cp .env.frontend.example .env.frontend`
   - Verify and update settings in `.env.backend` as necessary.
2. **Security Note:**
   - Ensure that sensitive keys like `JWT_SECRET_KEY` and OAuth secrets are secured in production environments.

## Local Development

1. **Frontend:**
   - Navigate to the `frontend` directory.
   - Install dependencies with: `npm install`.
   - Start the development server with: `npm run dev`.

2. **Backend:**
   - Navigate to the `backend` directory.
   - Install dependencies using: `pip install -r requirements.txt`.
   - Start the server with: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.

## Docker Deployment

1. Build and run all services using Docker Compose:
   - Execute: `docker-compose up --build`
2. This command references the `docker-compose.yml` and Dockerfiles for service configuration (includes frontend, backend, PostgreSQL, and Redis).

## Additional Recommendations

- Utilize CI/CD workflows for automated testing and cloud deployment.
- Change default credentials before deployment.
- Update API endpoints as needed for your production environment.
