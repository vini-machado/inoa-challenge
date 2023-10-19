# Inoa Challenge - Django 
This repository contains a python project using Django that visualizes stock prices and send email alerts as stock prices reach user input values.
## Installation
Create a new virtual environment
```bash
python -m venv env
```
Activate virtual environment

**Windows**
```bash
.\env\Scripts\activate
```
Install dependencies
```bash
pip install -r requirements.txt
```
## Configuration
**Email**
In order to be able to send email alerts, you need to create some credentials.
Duplicate "secrets-mock.json" file and rename it to "secrets.json" and insert correct credencials.

**Database**
To correct use built-in Django SQLite run the following command with python virtual enviroment activated
```bash
python manage.py migrate
```
## Usage

Finally, the application can be started running
```bash
python manage.py runserver --noreload
``` 
