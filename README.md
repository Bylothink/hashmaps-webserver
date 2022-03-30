# HashMaps web server 🗺

A simple web server that provides a RESTful API to store and
retrieve data from hashmap data structures made from scratch.

It provides a collection of different hashmaps for each authenticated user.  
Authentication is done by using the **[JSON Web Token](https://jwt.io/)** standard.

It stores the data in files on the disk and persists it across restarts.

It also keeps track via a simple log file of all the requests made by users,
allowing subsequent analysis and statistical processing of the use.

## Requirements

- **[`Python`](https://www.python.org/downloads/)**
- **[`pip`](https://pypi.org/project/pip/)**
- **[`Pipenv`](https://pipenv.pypa.io/en/latest/)**

*... or...*

- **[`Docker`](https://www.docker.com/)**
- **[`Docker Compose`](https://docs.docker.com/compose/)**

## Installation / Build

### Using your local Python

Make sure you have `Python`, `pip`, and `Pipenv` installed on your machine.  
Once done, navigate to your project folder and type the following command:

```sh
pipenv install
```

> *This will install all the dependencies required from this project to run properly.*

### Using Docker

Make sure you have `Docker` installed on your machine and the `Dockerd` service is up & running.  
Once done, navigate to your project folder and type the following command:

```sh
docker-compose build
```

> *This will build the `Docker` image which will later be used to run the project.*

## Starting the server

### Using your local Python

Type the following command:

```sh
pipenv shell

cd src/
python3 run.py
```

> *This will also run the project in `DEBUG` mode, by default.*

### Using Docker

Type the following command:

```sh
docker-compose up
```

> *This will also run the project in `PRODUCTION` mode, by default.*

## That's it!

Now the web server is running and you can access it at the following URL:

- **[localhost:8000](http://localhost:8000/)**
