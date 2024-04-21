# Inventory Management (cag-assessment-be)
This project is the backend component for an inventory management system

## Set up
To set up the project, you would need an IDE that supports Python. This project was created with Python 3.9.2

Run the following command to install the required packages:
> python -m pip install -r requirements.txt

## DB Set up
Download MySQL workbench and set up MySQL server, for more information:
https://dev.mysql.com/doc/mysql-getting-started/en/

After setting up the server, you can run the sql script file in the db folder to create the schema and tables. Change the variables in the .env file under the environment folder to your DB connection details.