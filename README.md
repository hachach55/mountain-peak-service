# Mountain Peak Service

This project provides a simple web service for storing and retrieving mountain peak information using FastAPI and asynchronous programming.

## Features

- REST API endpoints for CRUD operations on mountain peaks.
- Retrieve a list of peaks within a given geographical bounding box.
- API documentation page.
- High test coverage (> 90%)
- Dockerized application.
- CI/CD with Github Actions.

## Prerequisites

- Docker
- Docker Compose
- Git

## Getting Started

### Clone the repository
```bash
git clone https://github.com/your-username/mountain-peak-api.git
cd mountain-peak-api
```
### Environment Variables
Create a ```.env```file in the project root and the following variables
```
CAT_FOOD_SAFE_CODE = 1234
SECRET_KEY = your_secret_key
```

### Build and run with Docker Compose
```bash
docker-compose up --build
```

The API will be available at
```http://localhost:8000```.

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: ```http://localhost:8000/docs```

### Running Tests

To run the tests, use the following command:
```bash
docker-compose run --rm app pytest --cov=app tests/
```

## CI/CD
This project uses Github Actions for CI/CD. The workflow builds Docker images on each push or pull request on the main branch

