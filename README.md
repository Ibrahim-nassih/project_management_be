# project management Backend

web application for project management and bug tracking implemented with Django for the backend and Angular for the frontend.

## Getting Started

To get started with LeadSync, follow these steps:

- Clone the backend repository:
git clone https://github.com/Ibrahim-nassih/project_management_be.git

- Clone the frontend repository:
git clone https://github.com/Ibrahim-nassih/project_management_fe.git

- Navigate to the backend directory:
cd leadSync_Backend

- Install Django dependencies:
pip install -r requirements.txt

## Add Your Files

If you're adding an existing Git repository to your project, use the following commands:

```bash
cd existing_repo
git remote add origin https://github.com/Ibrahim-nassih/project_management_be.git
git branch -M main
git push -uf origin main
```
## API Endpoints
this app provides the following API endpoints:
```
POST /register: Register a new user.
GET /space: Retrieve information about a space.
GET /workflow: Retrieve workflows.
GET /step: Retrieve workflow steps.
GET /steps/{id}: Retrieve details of a specific workflow step.
POST /transaction: Create a new transaction.
GET /team: Retrieve team information.
GET /users: Retrieve user information.
POST /member: Add a new member to the team.
POST /ticket: Create a new ticket.
GET /tasks: Retrieve tasks.
POST /sprint: Create a new sprint.
GET /sprint/tickets: Retrieve tickets associated with a sprint.
```

## Visuals
Watch a demo of project management:
[![Video Demo](https://img.youtube.com/vi/PZOanoZQVbM/0.jpg)](https://youtu.be/_oMaxKaIThA)

## Author
project management backend is authored by Ibrahim Nassih.