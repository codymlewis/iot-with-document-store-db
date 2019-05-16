# IoT with Document Store DB
A simulation of an Internet of things network using a centralized document store database.

## Requirements
- CouchDB
- python
- NodeJS

## Setup
Run
```
cd www && npm install && cd ..
```

## Running
Start the simulation with
```
cd src && python3 Network.py
```
then start the web server with
```
cd ../www && npm start
```
and visit http://localhost:3000/
