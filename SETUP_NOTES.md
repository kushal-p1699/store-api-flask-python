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

6. Installing dependencies using `requirement.txt` file.

   ```linux
   pip install -r requirement.txt
   ```

7. Setting flask env to activate a debugger in dev mode.

   ```text
   FLASK_APP=app
   FLASK_DEBUG=1
   ```

   Note: `pip install python-dotenv` is required to use .flaskenv file.

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

   if ur using `requirments.txt`.

   ```Dockerfile
   FROM python:3.10
   EXPOSE 5000
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD [ "flask", "run", "--host", "0.0.0.0" ]
   ```

3. Building docker image

   ```linux
   docker build -t store-api-flask-python .
   ```

4. Running docker image

   ```linux
   docker run -p 5000:5000 store-api-flask-python
   ```

   If your changes needs to be reflected immediately then you need to volume mount your current working dir.

   ```linux
   docker run -p 5000:5000 -w /app -v "E:\Python Projects\Flask Projects\Store-api" store-api-flask-python
   ```

### Adding Schemas

Creating a schema by defining a class with variables mapping attribute names to Field objects.

```python
from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(required=True)
```

- `dump_only` is used when the property is used only when returning a response.
- `required` will validate if a property present in the payload or not.

#### Decorating routes with schemas

```python

from schemas import ItemSchema

@blp.route('/item/<string:item_id')
class Item(MethodView):
   @blp.response(200, ItemSchema(many=True)):
   def get(self, item_id):
      ....
      return items[item_id]

   @blp.arguments(ItemSchema)
   @blp.response(200, ItemSchema)
   def post(self, item_data):
      .....

```

- `@blp.arguments` is used to plugin the schema into the method.
- `@blp.response` is used to decorate the response in the format of schema. `many=True` specifies that response will be list of schema's
