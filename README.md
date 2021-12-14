### I2AMPARIS Project

## Install project locally

1. Clone the repository 
2. Go to project directory
3. Create virtual environment
4. Install all requirements:
```bash
pip install -r requirements.txt
```
5. Run server: 
```bash
python3 manage.py runserver 0.0.0.0:8000
```

6. Apply migrations:
```bash
python3 manage.py migrate
```

7. Use SQL files or pg_dump file to populate the database. (if you use the pg_dump file you will have to manually delete the tables created by the migrate command and re-initialise the tables' sequences)

 **The contact and evaluation services do not work in localhost.

Access Point: `http://localhost:8000`

## Install project using Docker (development)
1. Clone the repository 
2. Fill in the env variables in the files inside the directory .env/dev
3. Go to config_dev directory
4. Run: 
```bash
docker-compose up -d --build
```
5. The databse needs to be populated accordingly. !!! You may need to remove this command from the config_dev/run.sh file, as it completely deletes the database each time the container is re-created.
```bash
 python manage.py flush --no-input
 ```


## Install project using Docker (production)
1. Clone the repository 
2. Fill in the env variables in the files inside the directory .env/prod
3. Go to config_prod directory
4. Run: 
```bash
docker-compose up -d --build
```
5. The databse needs to be populated accordingly. !!! Under no circumstances should you delete the volume created by this container. ALL DATA WILL BE LOST.

