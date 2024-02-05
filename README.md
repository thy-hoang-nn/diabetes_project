# Installation & Getting Started 
## Prerequisites

Make sure you have the following installed on your system:

- [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
- [Python 3.9.0](https://www.python.org/downloads/release/python-390/)
- [Docker](https://www.docker.com/get-started)
## Setup
1. Clone the repo

```

git clone https://github.com/thy-hoang-nn/diabetes_project.git

```
2. Create new env

```

conda create -n diabetes python==3.9.0

```
3. Install dependencies

```

pip install pre-commit poetry

```

4. Setup pre-commit

```

pre-commit install

```
4. Setup poetry

```

poetry config virtualenvs.create false

```
5. Install pima diabetes project

```

cd diabetes && poetry install

```

## Running project with Docker
To deploy the monitoring system using Docker, navigate to the monitoring deployment folder:

```

cd deployment/monitoring && docker compose -f prom-graf-docker-compose.yaml up

```
Navigate to the metric instrument deployment folder and run:


```

cd deployement/instrument/metric && poetry run python metrics.py

```
This will start the Metric API, allowing you to interact with it.

## Repo structure
```

├── Jenkinsfile
├── Makefile
├── chat_api
│   ├── Dockerfile
│   ├── chat_api
│   ├── poetry.lock
│   └── pyproject.toml
├── deployment
│   ├── diabetes_core
│   ├── instrument
│   ├── jenkins_ops
│   └── monitoring
├── diabetes
│   ├── README.md
│   ├── diabetes
│   ├── example
│   ├── logs
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── tests
└── requirements.txt

```
