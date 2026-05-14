# zayco

Django + Django REST Framework で実装した家庭用在庫管理システムの API プロジェクトです。

## 使い方

1. Python 3.11 環境を用意します。
2. 依存関係をインストールします。

```bash
pip install -r requirements.txt
```

3. マイグレーションを実行します。

```bash
python manage.py migrate
```

4. サーバーを起動します。

```bash
python manage.py runserver
```

## API エンドポイント

- `POST /api/users/register`
- `POST /api/users/login`
- `GET /api/users/me`
- `GET /api/categories`
- `POST /api/categories`
- `DELETE /api/categories/:id`
- `GET /api/storage-locations`
- `POST /api/storage-locations`
- `DELETE /api/storage-locations/:id`
- `GET /api/products`
- `GET /api/products/:id`
- `POST /api/products`
- `PUT /api/products/:id`
- `DELETE /api/products/:id`
- `GET /api/inventory/lots`
- `GET /api/inventory/lots/:id`
- `POST /api/inventory/purchase`
- `POST /api/inventory/lots/:id/use`
- `GET /api/inventory/summary`
- `GET /api/inventory/history`
- `GET /api/shopping-list`
- `POST /api/shopping-list`
- `PATCH /api/shopping-list/:id`
- `DELETE /api/shopping-list/:id`
