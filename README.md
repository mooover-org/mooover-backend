# Mooover Backend

Welcome to the backend repository for Mooover!

## About

Mooover is a revolutionary online platform designed to make your moving experience better by making friends joining communities, doing challenges and taking part in public events all around the world! 

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Project Setup](#project-setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running Locally](#running-locally)
- [Deployment](#deployment)
- [Usage](#usage)
- [Microservices](#microservices)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

This repository contains the backend codebase, which handles the core functionality and data management using FastAPI, integrates with Auth0 for authentication, and leverages Neo4j's AuraDB for graph database capabilities.

## Features

- **FastAPI** for building a robust and high-performance backend.
- **Auth0** for secure authentication and authorization.
- **Neo4j AuraDB** for advanced graph database functionalities.
- **Docker Compose** for local development and deployment.
- **Microservices architecture** to ensure modularity and scalability.
- **Heroku deployment** for easy and free hosting.

## Architecture

The backend is structured into multiple microservices, each responsible for a specific domain of the application. This modular approach ensures better scalability and maintainability. Each microservice has its own folder with a detailed README explaining its specific functionality and setup.

## Project Setup

### Prerequisites

Before you begin, ensure you have the following tools installed:

- **Docker** and **Docker Compose**
- **Python 3.8+**
- **Git**
- **Auth0 account**
- **Neo4j AuraDB account**

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/adipopbv/mooover-backend.git
   cd mooover-backend
   ```
2. **Install dependencies:**
   It's recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
### Configuration

1. **Auth0 Setup:**
   - Create an Auth0 application and get the domain, client ID, and client secret.
   - Update each service's `.config` file with your Auth0 credentials.

2. **Neo4j AuraDB Setup:**
   - Create a Neo4j AuraDB instance and get the connection details.
   - Update each service's `.config` file with your Neo4j credentials.

3. **Database Password:**
   - Create a file called `db_password.txt` that contains only the database password. This is needed to access the database using Docker Compose.
   - Place it in the repo's root directory (`mooover-backend` if you followed the guide)

### Running Locally

1. **Start the Docker containers:**
   ```bash
   docker-compose build --no-cache # builds each service from scratch
   docker-compose up # starts the services in docker
   ```
   By default the API will be hosted on `http://localhost:80` and each service on `/api/v1/service`.
2. **Access the API documentation:**
   Visit `http://localhost:80/api/v1/service/docs` to see the interactive API documentation provided by FastAPI. Replace `service` with the service you want to check out.

## Deployment

You can deploy the backend side of the Mooover project on any other suitable hosting service, but for now the official backend is being hosted on Heroku.

## Usage

Once the application is up and running, you can interact with the backend via the provided API endpoints. Detailed documentation for each endpoint is available at `http://your-deployed-app.herokuapp.com/api/v1/service/docs` where `service` can be replaced by the service you want to check out.

## Microservices

Each microservice within the Mooover backend is located in the `services` directory. Refer to the individual README files within each service's folder for more detailed information on setup, configuration, and functionality.

## Contributing

We welcome contributions to improve Mooover! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

This project is licensed under the BSD-3-Clause License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, feel free to reach out at [adi.pop.bv@gmail.com](mailto:adi.pop.bv@gmail.com).

---

Let's get _Moooving!_
