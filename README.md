### Run the Dev server 
```bash
python manage.py runserver
```

### Create new app or module 
```bash
python manage.py startapp exampleapp 
```

### Migrations and Migrate 
a) Migrations
For All apps 
```bash
python manage.py makemigrations
```
For specific app
```bash
python manage.py makemigrations app_name
```

b) Migrate 
For All apps 
```bash
python manage.py migrate
```
For specific app
```bash
python manage.py migrate app_name
```