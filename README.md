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
