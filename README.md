# Project: Tournament Results
###### Udacity Full Stack ND

#### About The Project
---
This project was created in part of Udacity's Full Stack Nanodegree curriculum. For easiest and fastest way to get started, please download [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/).  

The main goal of this project is to create a database schema to store player and game information using python and the PostgreSQL module, psycopg2. The code to create the database and tables are located in tournament.sql.
###### Database Schema Walkthrough
* `CREATE DATABASE tournament` - creates the database titled tournament which will the contain the tables listed below.
* `CREATE TABLE registered_players ...` - creates table of registered players. Each row lists the players' name and gives them an ID in the datatype of SERIAL.
* `CREATE TABLE matches ...` - creates table of all matches played. Each row lists the matches' loser and winner player and also gives each row an ID in the datatype of SERIAL.
* `CREATE MATERIALIZED VIEW wins AS ...` - creates materialized view listing all the winners so far from the matches and registered_players table.
* `CREATE MATERIALIZED VIEW total_matches AS ...` - creates materialized view listing the total amount of matches played for each player in the registered_players table. 

#### Getting Started
---
###### Requirements:
* Python (2.7 or higher)
* VirtualBox (5.1.10)
* Vagrant (1.8.5)

###### Installation:
1. Download repo
2. Create vagrant file for project and run 'vagrant up' command.
3. Log into the new virtual machine by running:
```
project_5_tournament_results $ vagrant ssh
```

###### Creating the Database
4. Once you are in the terminal of your virtual machine, you can create the database needed to run the test file using PostgreSQL:
```
project_5_tournament_results $ psql -f tournament.sql
```

###### Running the Test File
4. In order to run the tests written in tournament_test.py execute the following command in the terminal of the virtual machine:
```
project_5_tournament_results $ python tournament_test.py
```

#### Copyright
---
This project is free of any copyrights and open to the public.
