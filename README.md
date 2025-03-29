# Audio Storage API 📦

API для загрузки и хранения аудиофайлов. Поддерживает авторизацию через OAuth Yandex и дальнейшую аутентификацию с использованием внутренних JWT токенов.

## 🔧 Стек технологий

- **FastAPI – веб-фреймворк для создания API.**
- &#x20;SQLAlchemy, Alembic – работа с базой данных.
- **Docker, Docker Compose – контейнеризация.**
- **OAuth Yandex – авторизация пользователей.**
- **JWT – аутентификация после входа через OAuth Yandex.**

## 🚀 Шаги по разворачиванию с Docker

1. **Создание директории приложения и переход в неё**:

   ```bash
   mkdir Audio_Storage_API && cd Audio_Storage_API
   ```

2. **Создание локальных папок для volume**:

   ```bash
   mkdir uploads logs
   ```

3. **Копирование `docker-compose.yml` из репозитория**:

   ```bash
   wget https://raw.githubusercontent.com/burvelandrei/Audio_Storage_API/main/docker-compose.yml
   ```

4. **Получение Yandex ID и Yandex Secret Client**:

   - Перейдите в [Yandex OAuth](https://oauth.yandex.ru/client/new).
   - Создайте новое приложение.
   - Укажите `redirect_uri`: `http://your_server_host:8001/auth/yandex/callback/`.
   - Запросите права **только** на `login:info`.
   - Сохраните `Yandex Client ID` и `Yandex Client Secret`.

5. **Создание `.env` файла на основе `config`**:

   - Создайте файл `.env` и укажите в нём переменные окружения.
   - Важно: в качестве хоста БД укажите `db`.

6. **Создание базы данных**:

   ```bash
   create database your_database;
   ```

7. **Запуск проекта через Docker Compose**:

   ```bash
   docker-compose up -d
   ```
## 📌 Доработки и планы развития

1. Добавление роутеров для изменения и удаления файлов.
2. Переход с локального хранилища на S3.
3. Разработка фронтенда для удобного взаимодействия с API.
4. Подключение Grafana Loki для логирования.
5. Введение ограничений на количество файлов и реализация платных подписок для увеличенного хранилища.

---

📌 **Автор:** [burvelandrei](https://github.com/burvelandrei)
