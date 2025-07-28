# SmartCity – Citizen Services Platform (Backend)

This repository contains the Flask-based backend implementation for the **SmartCity Citizen Services Platform**. The platform enables citizens to submit service requests, and access issued documents, while allowing administrators to manage and update request statuses.

---

## Features

-  **Service Requests**
    - Citizens can submit service requests (e.g., street light repair, garbage pickup)
    - View request history per citizen
    - Admins can update request statuses (e.g., approved, resolved)
-  **Document Management**
    - Citizens can submit requests for official documents (e.g., permits, certificates)
    - View all uploaded documents

---

##  Tech Stack

- **Language:** Python 3.x
- **Framework:** Flask
- **Database:** SQLite (via SQLAlchemy ORM)
- **API Format:** RESTful JSON

---

## Project Structure

    smartcity-backend/
    │
    ├── app.py # Main Flask app with models and API routes
    ├── instance
    |      ├── smartcity.db # SQLite database (auto-generated)
    ├── README.md # Project documentation
    └── requirements.txt # Python dependencies
---

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/smartcity-backend.git
   cd smartcity-backend
2. Create a virtual environment
    ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
3. Install dependencies
    ```bash
   pip install -r requirements.txt

4. Run the backend server
    ```bash
   python app.py

Server will start at: http://localhost:5000

## API Endpoints
### Service Requests

| Endpoint                       | Method | Description                  |
|--------------------------------| ------ | ---------------------------- |
| `/requests`                    | POST   | Create a new service request |
| `/requests/<citizen-id>`       | GET    | View citizen's requests      |
| `/admin/requests/<request-id>` | PUT    | Admin updates request status 

#### Sample Service Request Creation Payload
    {
        "citizen_id": 1,
        "category": "street-light",
        "description": "Street light not working on 5th Avenue."
    }

#### Sample Update Request Status Payload (Admin)
    {
        "status": "resolved"
    }

### Document Requests

| Endpoint                  | Method | Description                     |
|---------------------------| ------ | ------------------------------- |
| `/documents`              | POST   | Upload citizen document         |
| `/documents/<citizen-id>` | GET    | Retrieve all documents for user |


### Sample Document Request Creation Payload
    {
        "citizen_id": 1,
        "document_type": "birth-certificate",
        "content": "File path or base64 encoded text"
    }