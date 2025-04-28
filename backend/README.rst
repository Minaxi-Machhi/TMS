===================================
Task Management System
===================================

### APPS
----------
core
project_management
task_management

### .env
----------
```
DEBUG=True

DOMAIN="localhost"

DOMAIN_IP="127.0.0.1"

FRONT_END_DOMAIN="http://localhost:3000"

DB_NAME="dbname"

DB_USER="dbuser"

DB_PASSWORD="password"

DB_HOST="localhost"

TIME_ZONE="Asia/Muscat"

```

### Initial Migrations
------------------------------
```bash
python manage.py makemigrations
python manage.py migrate
```
