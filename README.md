## Запуск проекта

1. Установите Docker и Docker Compose.
2. В терминале перейдите в директорию проекта.
3. Запустите команду:

```
    docker-compose up --build
```
## Проверка работоспособности

- **Бэкенд**: Откройте браузер и перейдите по адресу `http://localhost:8000`.
- **PostgreSQL**: Подключитесь к базе данных через pgAdmin или другой клиент.
- **Redis**: Используйте `redis-cli` для проверки подключения.
- **Celery** и **Celery Beat**: Проверьте логи в терминале, чтобы убедиться, что задачи выполняются без ошибок.

## Настройка удаленного сервера

1. Откройте терминал и выполните команду для обновления списка пакетов:
`sudo apt update`
2. Выполните команду для обновления всех установленных пакетов до их последних версий:
`sudo apt upgrade`
3. Настройте файрвол.
4. В репозитории храните .env с переменными, или используйте Docker secrets.
Обязательные переменные:
DEBUG=false
SECRET_KEY=<секретный_ключ>
POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

5. В файле Dockerfile в корне проекта создайте образ приложения:
```
FROM python:3.13

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --no-input && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --timeout 120"]
```
6. Создайте nginx.conf и dockerfile для nginx в корне проекта.
7. Сохраните изменения в удаленный репозиторий, затем перейдите на удаленный сервер при помощи SSH.
8. Склонируйте удаленный репозиторий на сервер при помощи SSH ли git clone <путь к проекту>.
9. Перейдите в проект командой cd, создайте в нем env-файл:
``` nano .env ```
10. Сохраните из проекта переменные окружения в созданный файл.
11. Запустите контейнеры при помощи `docker compose up`.
12. После запуска контейнеров перейдите в адресной строке на свой домен или IP сервера.
13. При деплое с помощью GitHub Actions создайте в корне проекта директорию .github/workflows,
в ней создайте файл ci.yml.
```
name: Django CI

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Check out code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'

      - name: Install flake8
        run: |
          python -m pip install --upgrade pip
          pip install flake8

      - name: Run Flake8
        run: flake8 .

  test:
    needs: lint
    runs-on: ubuntu-latest

    steps:
      - name: Check out code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        env:
          SECRET_KEY: ${{ secrets.SECRET_KEY }}

        run: |
          python manage.py test

  build:
    needs: test
    runs-on: ubuntu-latest

    steps:
      - name: Check out code
        uses: actions/checkout@v3

      - name: Log in to Docker Hub
        run: echo ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }} | docker login -u ${{ secrets.DOCKER_HUB_USERNAME }} --password-stdin

      - name: Build Docker image
        run: docker build -t ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:${{ github.sha }} .

      - name: Push Docker image in Docker Hub
        run: docker push ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest

    steps:
      - name: Set up SSH
        uses: webfactory/ssh-agent@v0.9.0
        with:
          ssh-private-key: ${{ secrets.SSH_KEY }}

      - name: Deploy to Server
        run: |
          ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} << 'EOF'
          docker pull ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:${{ github.sha }}
          docker stop myapp || true
          docker rm myapp || true
          docker run -d --name myapp -p 80:8000 ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:${{ github.sha }}
          EOF
```