# Budgette
<img src="https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png"
     alt="Markdown Python icon"
     height="50px"
/>&nbsp;&nbsp;&nbsp;
<img src="https://cdn.worldvectorlogo.com/logos/fastapi.svg"
     alt="Markdown FastAPI icon"
     height="50px"
/>&nbsp;&nbsp;&nbsp;
<img src="https://wiki.postgresql.org/images/a/a4/PostgreSQL_logo.3colors.svg"
     alt="Markdown Postgre icon"
     height="50px"
/>&nbsp;&nbsp;&nbsp;
### Introduction
Purpose of this service is to manage user expenditures during a certain time period.
It holds data on users expenses with detailed information.

### Usage

Create the `.env` file which will hold environment variables:
```buildoutcfg
PROJECT_NAME=budgette

POSTGRES_USER=<PG_USER>
POSTGRES_PASSWORD=<PG_PASSWORD>
POSTGRES_SERVER=<PG_SERVER>
POSTGRES_PORT=<PG_PORT>
POSTGRES_DB=<PG_DATABASE>

LOCAL_ORIGIN=<SERVER_URL>

SECRET_KEY=<YOUR_SECRET_KEY>
```

It is advised to work in a virtual environment. Create one using the following command:
```
python3 -m venv venv
```

Activating **venv**:
- Windows OS: `./venv/Scripts/activate`
- Unix/Mac OS: `source venv/bin/activate`

Install the required packages into the newly created venv:
```
pip install -r requirements.txt
```

To start the server run:
```
python main.py
```

To start the tests:
```
pytest -v .
```