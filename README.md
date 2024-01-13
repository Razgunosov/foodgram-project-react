## Foodgram

1. Перейти в папку, где находится docker-compose:
```bash
cd infra
```
2. Развернуть docker-compose:
```bash
docker-compose up -d --no-deps --build
```
3. Выполнить служебные команды Django:
```bash
docker exec -it infra_backend_1 python manage.py migrate
docker exec -it infra_backend_1 python manage.py collectstatic --no-input
docker exec -it infra_backend_1 python manage.py createsuperuser
docker exec -it infra_backend_1 python manage.py load_ingredients
```