## About

ToDo list REST API built with Python FastAPI.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

```bash
make serve
```

## API Endpoints

| HTTP Method | URI                 | Action                  |
| ----------- | ------------------- | ----------------------- |
| GET         | /api/v1.0/tasks     | Retrieve list of tasks  |
| GET         | /api/v1.0/tasks/:id | Retrieve a task         |
| POST        | /api/v1.0/tasks     | Create a new task       |
| PUT         | /api/v1.0/tasks/:id | Update an existing task |
| DELETE      | /api/v1.0/tasks/:id | Delete a task           |
