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
pipenv install --dev --three
```

> *This will install all the dependencies required from this project to run properly.*

### Using Docker

Make sure you have `Docker` installed on your machine and the `Dockerd` service is up & running.  
Once done, navigate to your project folder and type the following command:

```sh
docker-compose build
```

> *This will build the `Docker` image which will later be used to run the project.*

## Configuration

Before starting the server, you need to configure it.

### `.env` file

To do so, you need to create a `.env` file in the project folder like the following:
```
SECRET_KEY=<32_chars_random_string>
```

> *This `SECRET_KEY` value will be the secret you need to use to generate your `JWT token` used for the user authentication.*

### `JWT token`

As just mentioned, the `JWT token` is used to authenticate the user.  
For this reason, you need to create your own `JWT token` if you want to use this service.

Visit the following URL: **[jwt.io](https://jwt.io/)**  
We will work on the right side of the page, the "**Decoded**" section.

Paste the same `SECRET_KEY` you just wrote inside the `.env`
into the input box that shows "`your-256-bit-secret`".  
Next, edit the "**PAYLOAD**" section by replacing the content with the following:

```json
{ "username": "<choose-the-username-you-want-to-use>" }
```

> *Choose your favourite username or change it with some others if you want to try the multi-user experience.*

Now you can save the newly generated `JWT token`, shown on the left side of the screen, under the "**Encoded**" section.  
It should look almost like...

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

## Starting the server

### Using your local Python

Type the following command:

```sh
pipenv shell

cd src/

mkdir -p .volume/collections \
         .volume/logs

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

### Authentication

All you have to do now is to append to your requests the `Authorization` header
valued with the `JWT token` you previously generated using the `SECRET_KET`.

### Requests

The web server provide the following endpoints:

- **`/`**
    - **GET**: returns the entire collection of hashmaps of the authenticated user.
- **`/<name>`**
    - **GET**: returns the `<name>` hashmap with all the stored key-value pairs.
    - **POST**: creates the `<name>` hashmap if it doesn't exist yet.  
    Ignores the request payload.
    - **PUT**: renames the `<name>` hashmap using the value present in the request payload.
    - **DELETE**: removes the `<name>` hashmap if it already exists.  
    Ignores the request payload.
- **`/<name>/<key>`**
    - **GET**: returns the value for `<key>` stored within the `<name>` hashmap.
    - **POST**: creates and sets the value for `<key>` stored within the
    `<name>` hashmap using the value present in the request payload.  
    It fails if `<key>` already exists.
    - **PUT**: replaces the value for `<key>` stored within the
    `<name>` hashmap using the value present in the request payload.  
    It fails if `<key>` doesn't exist yet.
    - **DELETE**: removes the value for `<key>` stored within the `<name>` hashmap.  
    Ignores the request payload.
