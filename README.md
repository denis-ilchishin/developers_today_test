# Developers Today Test Assessment

[Assessment link](https://www.notion.so/Python-test-assessment-by-DevelopsToday-901e35b8314d4ddc962bebf5041871d6)
[Postman docs](https://documenter.getpostman.com/view/14225558/TVzVjGrL#8a64df16-dc10-4c95-8c39-9e75a5112cf7)
## How to run

Clone source code
```
git clone git@github.com:denis-ilchishin/developers_today_test.git
cd developers_today_test
```

Setup env variables
```
cp .env.example .env
```

Run migration
```
docker-compose -f docker-compose.dev.yml run --rm api python manage.py migrate
```

Run tests
```
docker-compose -f docker-compose.dev.yml run --rm api python manage.py test
```

Run dev server on [http://localhost:8000](http://localhost:8000)
```
docker-compose -f docker-compose.dev.yml run --rm api python manage.py runserver 0.0.0.0:8000
```
---
Or run for local development inside container (with VSCode, for example)
```
docker-compose -f docker-compose.dev.yml up -d
```
Inside container
```
./manage.py runserver 0.0.0.0:8000
```
