<<<<<<< HEAD
# flask_crud_CS# Flask CRUD API with MySQL

## Project Overview
This project is a Flask REST API connected to a MySQL database for managing company records.
It supports:
- CRUD operations (Create, Read, Update, Delete)
- JWT authentication for security
- Search functionality across company fields
- JSON and XML output formats

## Database
- MySQL database: `sales_db`
- Table: `company`
- Fields: `id`, `HONDA`, `YAMAHA`, `SUZUKI`, `RUSI`, `KAWASAKI`
- Sample data: 22 records

## Installation Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Daul7/flask_crud_CS.git
cd flask_crud_CS
=======
This project is a Flask REST API connected to a MySQL database (sales_db) that manages company records.
It supports full CRUD operations: 
- POST /company to create a new record
- GET /company to retrieve all records
- GET /company/<id> to retrieve a single record by ID
- PUT /company/<id> to update an existing record
- DELETE /company/<id> to delete a record
The API also includes:
- JWT authentication to secure endpoints
- Search functionality to filter companies by any field
- JSON and XML output formats for API responses
Test scripts are provided to demonstrate all CRUD operations in the terminal.
>>>>>>> cf3528209636d9a3cade0913c6ec2ca9b26dd37c
