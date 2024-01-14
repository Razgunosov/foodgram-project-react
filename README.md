### Foodgram - продуктовый помощник с базой кулинарных рецептов. Позволяет публиковать рецепты, сохранять избранные, а также формировать список покупок для выбранных рецептов. Можно подписываться на любимых авторов.

Проект доступен по [razgunosfoodgram.ddns.net](razgunosfoodgram.ddns.net)

### Запуск проекта
1. Склонировать репозиторий:
```bash
git clone https://github.com/Razgunosov/foodgram-project-react.git
```

2. Перейти в папку проекта и зайти в папку, где находится docker-compose:
```bash
cd infra
```
3. Создать в папке infra файл .env и прописать туда Ваши данные для подключения к Postgres. Пример:
```
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
4. Установить на сервере Docker, Docker Compose:

```
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
```

5. Развернуть docker-compose:
```bash
docker-compose up -d --no-deps --build
```
6. Выполнить служебные команды Django и следовать инструкциям в консоли:
```bash
docker exec -it infra_backend_1 python manage.py migrate
docker exec -it infra_backend_1 python manage.py collectstatic --no-input
docker exec -it infra_backend_1 python manage.py createsuperuser
docker exec -it infra_backend_1 python manage.py load_ingredients
```

- После запуска проект будут доступен по адресу: [http://localhost/](http://localhost/)
- Документация будет доступна по адресу: [http://localhost/api/docs/](http://localhost/api/docs/)
