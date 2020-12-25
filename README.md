# Bloodbank Database

A model database of a blood bank. Supports all relevant queries.
- Database design and functionalities: [database_design.pdf](Schema/database_design.pdf) 
- Entity Relationship diagram: [ER_diagram.png](Schema/ER_diagram.png)
- Relational Schema diagram: [relational_schema.png](Schema/relational_schema.png)


## Database Purpose

This project presents a <strong>Blood Bank Database Management System (BBDBMS)</strong>. The system keeps track of data 
in all stages of blood donation from donor participation to providing blood to patients in hospitals. The system keeps 
a record of donor information, details of donation, properties of blood donated, results of blood testing, processed 
blood components, stock of blood in blood inventory/storage and data about orders placed by hospitals.

## Intended Audience

This database is meant to be used by blood donation centers for the overall management of data pertaining to different 
stages in the blood donation process. Functions of the database are described in the functional requirements section of 
[database_design.pdf](Schema/database_design.pdf).

## How to Run the CLI

- Run ```pip3 install pymysql prettytable```.
- Run ```mysql -u <username> -p < SQL/schema.sql``` to create the database.
- Run ```python3 pyscripts/main.py``` to start the CLI. You will be prompted to enter username and password before the 
  CLI starts.
  
## General Instructions

- The username and password entered to start the CLI must be the same as those used to create the database.
- The fields in the CLI marked with ```*``` are optional. These can be skipped by pressing ```ENTER```.