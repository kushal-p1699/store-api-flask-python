# Flask Project Setup

1. Creating python virtual enviornment

   ```linux
   python -m venv .venv
   ```

2. Once .venv is created, terminate the current terminal and open new terminal.
3. Install flask

   ```linux
   pip install flask
   ```

4. Create python file with name `app.py` and add below code.

   ```python
   from flask import Flask

   # NOTE: variable name should be same as filename
   app = Flask(__name__)
   ```

5. Running flask app

   ```linux
   flask run
   ```

## Running flask app in Docker

1. Make sure you have docker installed in your system.
2. Create a `Dockerfile` without any extension.

   ```Dockerfile
   FROM python:3.10
   EXPOSE 5000
   WORKDIR /app
   RUN pip install flask
   COPY . . # COPY current-directory current-workdir
   CMD [ "flask", "run", "--host", "0.0.0.0" ]
   ```

3. Building docker image

   ```linux
   docker run -t store-api-flask-python .
   ```

4. Running docker image

   ```linux
   docker run -p 5000:5000 store-api-flask-python
   ```
