# IoT with Document Store DB
A simulation of an Internet of things network using a centralized document store database.

## Requirements
- CouchDB
- python
- flask

## Setup
Run
```
pip3 install -r requirements.txt
```

## Running
Start the simulation with
```
cd src && python3 Network.py
```
then start the web server with
```
cd ../www && export FLASK_APP=Server.py && flask run
```
and visit http://localhost:5000/
