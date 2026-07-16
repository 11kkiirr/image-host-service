# API документация — image-host-service

Документация предназначена для фронтенд-разработчика: описывает эндпоинты, форматы запросов/ответов, требования по аутентификации и примеры запросов.

Base URL: зависит от окружения (например `https://api.example.com` или `http://localhost:8000`).

## Аутентификация
- Метод: cookie-based auth.
- При успешном `POST /auth/login` сервер устанавливает httpOnly cookie `access_token` со значением `Bearer <token>`.
- Для всех защищённых запросов фронтенду нужно отправлять запросы с `credentials: 'include'` (в fetch/axios) или передавать cookie в curl/постман.
- Cookie флаги (dev): `httponly`, `samesite='lax'`, `secure=False`. На продакшене `secure=True` и HTTPS обязательно.

> Важно: фронтенд не должен пытаться читать / модифицировать `access_token` (httponly).

## Основные Pydantic-схемы (кратко)
- `UserCreateSchema`: `{ username: str, email: str, password: str }` (validation: username 3-50, password 8-50)
- `UserLoginSchema`: `{ email: str, password: str }`
- `UserProfileReadSchema`: `{ id: int, username?: str, email?: str, is_email_confirmed?: bool, is_banned?: bool, is_moderator?: bool, is_admin?: bool }`
- `ItemCreateSchema`: `{ link_hash?: str, title?: str, description?: str, is_global: bool }` (сервер сам ставит `owner_id`, поэтому клиенту не нужно отправлять его)
- `ItemUpdateSchema`: `{ title?: str, description?: str, is_global?: bool }`
- `ItemReadSchema`: `{ uuid: UUID, owner_id: int, link_hash: str, title?: str, description?: str, is_global: bool, views: int, likes: int, deleted_at?: str }`
- `FileReadSchema`: `{ uuid: UUID, creator_id: int, item_id?: UUID, filename: str, content_type: str, size: int, storage_path: str, is_deleted?: bool }`

## Конкретные эндпоинты

1) GET /
   - Описание: отдаёт `static/index.html` (UI).
   - Auth: нет

2) POST /auth/register
   - Auth: нет
   - Body (JSON): `UserCreateSchema`
   - Успех: `200` {
       "message": "User registered successfully",
       "user_id": <int>
     }
   - Ошибки: 400 / валидация

3) POST /auth/login
   - Auth: нет
   - Body (JSON): `UserLoginSchema`
   - Успех: `200` { "message": "Успешный вход" } + cookie `access_token` устанавливается
   - Ошибки: `401` при неверных данных

4) GET /profile/me
   - Auth: требуется (cookie)
   - Response: `UserProfileReadSchema`
   - Ошибки: `404` если пользователь не найден

5) POST /file/upload
   - Auth: требуется
   - Body: `multipart/form-data` — поля `uploaded_files` (или `files`) как массив файлов
   - Response: `200` {
       "message": "Files uploaded successfully.",
       "files": [ FileReadSchema, ... ]
     }
   - Ошибки: `400` если файлы отсутствуют

6) GET /file/{content_uuid}
   - Auth: по коду не требуется (зависит от сервиса)
   - Path param: `content_uuid` (UUID/str)
   - Response: бинарный файл (FileResponse) с заголовком для скачивания

7) GET /p/u/{item_uuid}
   - Auth: нет
   - Path param: `item_uuid` (UUID)
   - Response: `ItemReadSchema`

8) GET /p/h/{link_hash}
   - Auth: нет
   - Path param: `link_hash`
   - Response: `ItemReadSchema`

9) GET /p/my_posts
   - Auth: требуется
   - Response: список `ItemReadSchema`

10) POST /post/create_new
    - Auth: требуется
    - Body (JSON): `ItemCreateSchema` (лучше не отправлять `owner_id` с клиента)
    - Response: созданный объект (предположительно `ItemReadSchema`)

11) POST /post/update
    - Auth: требуется
    - Query param: `item_uuid` (пример: `/post/update?item_uuid=<UUID>`) — в коде параметр объявлен как обычный аргумент, поэтому FastAPI ожидает query parameter
    - Body (JSON): `ItemUpdateSchema`
    - Response: обновлённый объект

12) POST /post/create_link
    - Auth: требуется
    - Query param: `item_uuid`
    - Body: пустой
    - Response: объект с заполненным `link_hash`

## Примеры запросов (frontend)

Login (fetch):

```javascript
fetch('/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'ivan@example.com', password: 'securepass' }),
  credentials: 'include'
})
```

Get profile:

```javascript
fetch('/profile/me', { method: 'GET', credentials: 'include' })
  .then(r => r.json())
  .then(data => console.log(data));
```

Upload files (fetch):

```javascript
const fd = new FormData();
fd.append('uploaded_files', fileInput.files[0]);
fd.append('uploaded_files', fileInput.files[1]);
fetch('/file/upload', { method: 'POST', body: fd, credentials: 'include' })
  .then(r => r.json())
  .then(data => console.log(data));
```

Create post:

```javascript
fetch('/post/create_new', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'Привет', description: 'Описание', is_global: false }),
  credentials: 'include'
})
```

Update post (query param):

```javascript
fetch('/post/update?item_uuid=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title: 'Новый заголовок' }),
  credentials: 'include'
})
```

Download file (browser):

```javascript
fetch('/file/CONTENT_UUID')
  .then(res => res.blob())
  .then(blob => {
    // показать или сохранить
  })
```

Curl example (upload, using cookie file):

```bash
curl -v -X POST "https://api.example.com/file/upload" -b cookies.txt \
  -F "uploaded_files=@/path/to/img1.jpg" -F "uploaded_files=@/path/to/img2.png"
```

## Замечания и рекомендации
- Все защищённые запросы: `credentials: 'include'`.
- Не читать httponly cookie с клиента.
- `item_uuid` в некоторых `POST`-маршрутах передаётся как query-параметр.
- При создании поста лучше не передавать `owner_id` — сервер использует `user_id` из сессии.
- Проверять размер/тип файлов на клиенте перед отправкой (сервер принимает `UploadFile`).

## Где смотреть исходники
- Роуты: `apps/backend/src/presentation/api/routes/` (auth_route.py, profile_route.py, content_route.py, item_get_route.py, item_post_route.py, main_route.py)
- Схемы: `apps/backend/src/database/schemas/` (users.py, items.py, files.py)

---
Если нужно, могу дополнительно сгенерировать Postman-коллекцию или готовые React-хуки для каждого эндпоинта.
