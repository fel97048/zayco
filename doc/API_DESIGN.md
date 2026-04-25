# API設計書

## 改訂履歴

| 版 | 日付 | 変更内容 |
|---|------|---------|
| 1.0 | 2025-03-11 | 初版作成 |

## 1. 概要

### 1.1 フレームワーク

**バックエンド:** Django 4.2 + Django REST Framework

### 1.2 ベースURL

```
開発環境: http://localhost:8000
本番環境: https://inventory.example.com
```

### 1.3 認証方式

- **方式:** JWT (JSON Web Token)
- **ライブラリ:** djangorestframework-simplejwt
- **ヘッダー:** `Authorization: Bearer {access_token}`
- **トークン種別:**
  - Access Token: 有効期限30分
  - Refresh Token: 有効期限7日（将来実装）

### 1.4 共通レスポンス形式

**成功時:**
```json
{
  "data": { ... },
  "message": "成功メッセージ（任意）"
}
```

**エラー時:**
```json
{
  "detail": "エラーメッセージ"
}
```

### 1.5 HTTPステータスコード

| コード | 意味 | 使用例 |
|--------|------|--------|
| 200 | OK | 成功（取得、更新、削除） |
| 201 | Created | 新規作成成功 |
| 400 | Bad Request | バリデーションエラー |
| 401 | Unauthorized | 認証エラー |
| 403 | Forbidden | 権限エラー |
| 404 | Not Found | リソースが見つからない |
| 409 | Conflict | 重複エラー |
| 500 | Internal Server Error | サーバーエラー |

---

## 2. エンドポイント一覧

### 2.1 認証

| メソッド | エンドポイント | 説明 | 認証 |
|---------|---------------|------|------|
| POST | /api/users/register | ユーザー登録 | 不要 |
| POST | /api/users/login | ログイン | 不要 |
| GET | /api/users/me | 現在のユーザー情報取得 | 必要 |

### 2.2 カテゴリ

| メソッド | エンドポイント | 説明 | 認証 |
|---------|---------------|------|------|
| GET | /api/categories | カテゴリ一覧取得 | 必要 |
| POST | /api/categories | カテゴリ作成 | 必要 |
| DELETE | /api/categories/:id | カテゴリ削除 | 必要 |

### 2.3 保管場所

| メソッド | エンドポイント | 説明 | 認証 |
|---------|---------------|------|------|
| GET | /api/storage-locations | 保管場所一覧取得 | 必要 |
| POST | /api/storage-locations | 保管場所作成 | 必要 |
| DELETE | /api/storage-locations/:id | 保管場所削除 | 必要 |

### 2.4 商品マスタ

| メソッド | エンドポイント | 説明 | 認証 |
|---------|---------------|------|------|
| GET | /api/products | 商品一覧取得 | 必要 |
| GET | /api/products/:id | 商品詳細取得 | 必要 |
| POST | /api/products | 商品作成 | 必要 |
| PUT | /api/products/:id | 商品更新 | 必要 |
| DELETE | /api/products/:id | 商品削除（論理削除） | 必要 |

### 2.5 在庫ロット

| メソッド | エンドポイント | 説明 | 認証 |
|---------|---------------|------|------|
| GET | /api/inventory/lots | 在庫ロット一覧取得 | 必要 |
| GET | /api/inventory/lots/:id | ロット詳細取得 | 必要 |
| POST | /api/inventory/purchase | 購入登録 | 必要 |
| POST | /api/inventory/lots/:id/use | 使用登録 | 必要 |
| GET | /api/inventory/summary | 商品別在庫サマリー | 必要 |

### 2.6 在庫履歴

| メソッド | エンドポイント | 説明 | 認証 |
|---------|---------------|------|------|
| GET | /api/inventory/history | 在庫履歴取得 | 必要 |

### 2.7 買い物リスト

| メソッド | エンドポイント | 説明 | 認証 |
|---------|---------------|------|------|
| GET | /api/shopping-list | 買い物リスト一覧取得 | 必要 |
| POST | /api/shopping-list | リストに追加 | 必要 |
| PATCH | /api/shopping-list/:id | 購入済みに更新 | 必要 |
| DELETE | /api/shopping-list/:id | リストから削除 | 必要 |

---

## 3. 詳細仕様

---

### 3.1 認証API

#### POST /api/users/register

**説明:** 新規ユーザー登録

**リクエスト:**
```json
{
  "username": "tanaka",
  "password": "mypassword123"
}
```

**バリデーション:**
- username: 必須、3-50文字、一意
- password: 必須、4文字以上

**レスポンス (201 Created):**
```json
{
  "id": 1,
  "username": "tanaka",
  "created_at": "2025-03-11T10:00:00Z"
}
```

**エラー:**
- 400: バリデーションエラー
- 409: ユーザー名が既に使用されている

---

#### POST /api/users/login

**説明:** ログイン

**リクエスト:**
```json
{
  "username": "tanaka",
  "password": "mypassword123"
}
```

**レスポンス (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**エラー:**
- 401: ユーザー名またはパスワードが正しくありません

---

#### GET /api/users/me

**説明:** 現在のユーザー情報取得

**認証:** 必要

**レスポンス (200 OK):**
```json
{
  "id": 1,
  "username": "tanaka",
  "created_at": "2025-03-11T10:00:00Z"
}
```

**エラー:**
- 401: 認証エラー

---

### 3.2 カテゴリAPI

#### GET /api/categories

**説明:** カテゴリ一覧取得

**認証:** 必要

**レスポンス (200 OK):**
```json
[
  {
    "id": 1,
    "name": "調味料",
    "created_at": "2025-03-10T10:00:00Z"
  },
  {
    "id": 2,
    "name": "飲料",
    "created_at": "2025-03-10T10:00:00Z"
  }
]
```

---

#### POST /api/categories

**説明:** カテゴリ作成

**認証:** 必要

**リクエスト:**
```json
{
  "name": "冷凍食品"
}
```

**バリデーション:**
- name: 必須、最大50文字、一意

**レスポンス (201 Created):**
```json
{
  "id": 3,
  "name": "冷凍食品",
  "created_at": "2025-03-11T10:00:00Z"
}
```

**エラー:**
- 400: バリデーションエラー
- 409: カテゴリ名が既に存在

---

#### DELETE /api/categories/:id

**説明:** カテゴリ削除

**認証:** 必要

**レスポンス (200 OK):**
```json
{
  "message": "カテゴリを削除しました"
}
```

**エラー:**
- 404: カテゴリが見つかりません
- 409: このカテゴリは商品で使用されているため削除できません

---

### 3.3 保管場所API

#### GET /api/storage-locations

**説明:** 保管場所一覧取得

**認証:** 必要

**レスポンス (200 OK):**
```json
[
  {
    "id": 1,
    "name": "パントリー",
    "description": "常温保存可能な食品や調味料",
    "created_at": "2025-03-10T10:00:00Z"
  },
  {
    "id": 2,
    "name": "冷蔵庫",
    "description": null,
    "created_at": "2025-03-10T10:00:00Z"
  }
]
```

---

#### POST /api/storage-locations

**説明:** 保管場所作成

**認証:** 必要

**リクエスト:**
```json
{
  "name": "倉庫",
  "description": "ストック品"
}
```

**バリデーション:**
- name: 必須、最大50文字、一意
- description: 任意

**レスポンス (201 Created):**
```json
{
  "id": 5,
  "name": "倉庫",
  "description": "ストック品",
  "created_at": "2025-03-11T10:00:00Z"
}
```

**エラー:**
- 400: バリデーションエラー
- 409: 保管場所名が既に存在

---

#### DELETE /api/storage-locations/:id

**説明:** 保管場所削除

**認証:** 必要

**レスポンス (200 OK):**
```json
{
  "message": "保管場所を削除しました"
}
```

**エラー:**
- 404: 保管場所が見つかりません
- 409: この保管場所は商品または在庫で使用されているため削除できません

---

### 3.4 商品マスタAPI

#### GET /api/products

**説明:** 商品一覧取得

**認証:** 必要

**クエリパラメータ:**
| パラメータ | 型 | 説明 | デフォルト |
|-----------|---|------|-----------|
| search | string | 商品名で検索（部分一致） | - |
| category_id | integer | カテゴリでフィルタ | - |
| include_deleted | boolean | 削除済み商品を含む | false |
| page | integer | ページ番号 | 1 |
| limit | integer | 1ページあたりの件数 | 50 |

**リクエスト例:**
```
GET /api/products?search=醤油&category_id=1&page=1&limit=20
```

**レスポンス (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "name": "キッコーマン醤油 500ml",
      "category": {
        "id": 1,
        "name": "調味料"
      },
      "default_storage_location": {
        "id": 1,
        "name": "パントリー"
      },
      "barcode": "4901515001234",
      "unit": "ml",
      "description": "キッコーマン しょうゆ",
      "deleted_at": null,
      "created_at": "2025-03-10T10:00:00Z",
      "updated_at": "2025-03-10T10:00:00Z"
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8
}
```

---

#### GET /api/products/:id

**説明:** 商品詳細取得

**認証:** 必要

**レスポンス (200 OK):**
```json
{
  "id": 1,
  "name": "キッコーマン醤油 500ml",
  "category": {
    "id": 1,
    "name": "調味料"
  },
  "default_storage_location": {
    "id": 1,
    "name": "パントリー"
  },
  "barcode": "4901515001234",
  "unit": "ml",
  "description": "キッコーマン しょうゆ",
  "deleted_at": null,
  "created_at": "2025-03-10T10:00:00Z",
  "updated_at": "2025-03-10T10:00:00Z"
}
```

**エラー:**
- 404: 商品が見つかりません

---

#### POST /api/products

**説明:** 商品作成

**認証:** 必要

**リクエスト:**
```json
{
  "name": "キッコーマン醤油 1L",
  "category_id": 1,
  "default_storage_location_id": 1,
  "barcode": "4901515001241",
  "unit": "ml",
  "description": "キッコーマン しょうゆ 1L"
}
```

**バリデーション:**
- name: 必須、最大255文字
- category_id: 必須、存在するカテゴリID
- default_storage_location_id: 必須、存在する保管場所ID
- barcode: 任意、最大50文字、一意
- unit: 必須、最大20文字
- description: 任意

**レスポンス (201 Created):**
```json
{
  "id": 2,
  "name": "キッコーマン醤油 1L",
  "category": {
    "id": 1,
    "name": "調味料"
  },
  "default_storage_location": {
    "id": 1,
    "name": "パントリー"
  },
  "barcode": "4901515001241",
  "unit": "ml",
  "description": "キッコーマン しょうゆ 1L",
  "deleted_at": null,
  "created_at": "2025-03-11T10:00:00Z",
  "updated_at": "2025-03-11T10:00:00Z"
}
```

**エラー:**
- 400: バリデーションエラー
- 404: カテゴリまたは保管場所が見つかりません
- 409: バーコードが既に存在

---

#### PUT /api/products/:id

**説明:** 商品更新

**認証:** 必要

**リクエスト:**
```json
{
  "name": "キッコーマン醤油 1L（改）",
  "category_id": 1,
  "default_storage_location_id": 1,
  "barcode": "4901515001241",
  "unit": "ml",
  "description": "新しい説明"
}
```

**バリデーション:** POST と同じ

**レスポンス (200 OK):**
```json
{
  "id": 2,
  "name": "キッコーマン醤油 1L（改）",
  "category": {
    "id": 1,
    "name": "調味料"
  },
  "default_storage_location": {
    "id": 1,
    "name": "パントリー"
  },
  "barcode": "4901515001241",
  "unit": "ml",
  "description": "新しい説明",
  "deleted_at": null,
  "created_at": "2025-03-11T10:00:00Z",
  "updated_at": "2025-03-11T10:30:00Z"
}
```

**エラー:**
- 400: バリデーションエラー
- 404: 商品が見つかりません
- 409: バーコードが既に存在（他の商品で使用中）

---

#### DELETE /api/products/:id

**説明:** 商品削除（論理削除）

**認証:** 必要

**レスポンス (200 OK):**
```json
{
  "message": "商品を削除しました"
}
```

**エラー:**
- 404: 商品が見つかりません

**備考:**
- 物理削除ではなく論理削除（deleted_at に現在日時を設定）
- 在庫が残っていても削除可能（警告は UI 側で処理）

---

### 3.5 在庫ロットAPI

#### GET /api/inventory/lots

**説明:** 在庫ロット一覧取得

**認証:** 必要

**クエリパラメータ:**
| パラメータ | 型 | 説明 | デフォルト |
|-----------|---|------|-----------|
| search | string | 商品名で検索（部分一致） | - |
| category_id | integer | カテゴリでフィルタ | - |
| storage_location_id | integer | 保管場所でフィルタ | - |
| has_expiry | boolean | 賞味期限の有無 | - |
| expiry_within_days | integer | N日以内に期限切れ | - |
| sort_by | string | ソート項目（expiry_date/quantity/product_name） | expiry_date |
| sort_order | string | ソート順（asc/desc） | asc |
| page | integer | ページ番号 | 1 |
| limit | integer | 1ページあたりの件数 | 20 |

**リクエスト例:**
```
GET /api/inventory/lots?storage_location_id=2&expiry_within_days=30&sort_by=expiry_date&sort_order=asc
```

**レスポンス (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "product": {
        "id": 3,
        "name": "明治おいしい牛乳 1L",
        "unit": "L",
        "category": {
          "id": 6,
          "name": "生鮮食品"
        }
      },
      "storage_location": {
        "id": 2,
        "name": "冷蔵庫"
      },
      "quantity": 2.0,
      "expiry_date": "2025-03-20",
      "purchased_date": "2025-03-10",
      "created_by": {
        "id": 1,
        "username": "tanaka"
      },
      "created_at": "2025-03-10T10:00:00Z",
      "updated_at": "2025-03-10T10:00:00Z"
    },
    {
      "id": 2,
      "product": {
        "id": 3,
        "name": "明治おいしい牛乳 1L",
        "unit": "L",
        "category": {
          "id": 6,
          "name": "生鮮食品"
        }
      },
      "storage_location": {
        "id": 2,
        "name": "冷蔵庫"
      },
      "quantity": 1.0,
      "expiry_date": "2025-03-25",
      "purchased_date": "2025-03-11",
      "created_by": {
        "id": 1,
        "username": "tanaka"
      },
      "created_at": "2025-03-11T08:00:00Z",
      "updated_at": "2025-03-11T08:00:00Z"
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8
}
```

---

#### GET /api/inventory/lots/:id

**説明:** ロット詳細取得

**認証:** 必要

**レスポンス (200 OK):**
```json
{
  "id": 1,
  "product": {
    "id": 3,
    "name": "明治おいしい牛乳 1L",
    "unit": "L",
    "category": {
      "id": 6,
      "name": "生鮮食品"
    }
  },
  "storage_location": {
    "id": 2,
    "name": "冷蔵庫",
    "description": null
  },
  "quantity": 2.0,
  "expiry_date": "2025-03-20",
  "purchased_date": "2025-03-10",
  "created_by": {
    "id": 1,
    "username": "tanaka"
  },
  "created_at": "2025-03-10T10:00:00Z",
  "updated_at": "2025-03-10T10:00:00Z"
}
```

**エラー:**
- 404: ロットが見つかりません

---

#### POST /api/inventory/purchase

**説明:** 購入登録（ロットの作成または更新）

**認証:** 必要

**リクエスト:**
```json
{
  "product_id": 3,
  "quantity": 2.0,
  "storage_location_id": 2,
  "expiry_date": "2025-03-20",
  "purchased_date": "2025-03-11"
}
```

**バリデーション:**
- product_id: 必須、存在する商品ID（削除されていない）
- quantity: 必須、0より大きい
- storage_location_id: 必須、存在する保管場所ID
- expiry_date: 任意、purchased_date以降
- purchased_date: 任意、デフォルトは今日

**処理:**
1. 同一ロット検索（product_id, storage_location_id, expiry_date が一致）
2. 存在する場合：quantity を加算
3. 存在しない場合：新規ロット作成
4. inventory_transactions に履歴記録

**レスポンス (201 Created):**
```json
{
  "lot": {
    "id": 1,
    "product": {
      "id": 3,
      "name": "明治おいしい牛乳 1L",
      "unit": "L"
    },
    "storage_location": {
      "id": 2,
      "name": "冷蔵庫"
    },
    "quantity": 4.0,
    "expiry_date": "2025-03-20",
    "purchased_date": "2025-03-11",
    "created_at": "2025-03-10T10:00:00Z",
    "updated_at": "2025-03-11T10:00:00Z"
  },
  "transaction": {
    "id": 10,
    "transaction_type": "購入",
    "quantity": 2.0,
    "created_at": "2025-03-11T10:00:00Z"
  }
}
```

**エラー:**
- 400: バリデーションエラー
- 404: 商品または保管場所が見つかりません

---

#### POST /api/inventory/lots/:id/use

**説明:** 使用登録（ロットの減算）

**認証:** 必要

**リクエスト:**
```json
{
  "quantity": 1.0
}
```

**バリデーション:**
- quantity: 必須、0より大きい、現在在庫数以下

**処理:**
1. ロットの quantity から減算
2. inventory_transactions に履歴記録

**レスポンス (200 OK):**
```json
{
  "lot": {
    "id": 1,
    "product": {
      "id": 3,
      "name": "明治おいしい牛乳 1L",
      "unit": "L"
    },
    "storage_location": {
      "id": 2,
      "name": "冷蔵庫"
    },
    "quantity": 3.0,
    "expiry_date": "2025-03-20",
    "purchased_date": "2025-03-11",
    "created_at": "2025-03-10T10:00:00Z",
    "updated_at": "2025-03-11T11:00:00Z"
  },
  "transaction": {
    "id": 11,
    "transaction_type": "使用",
    "quantity": 1.0,
    "created_at": "2025-03-11T11:00:00Z"
  }
}
```

**エラー:**
- 400: 在庫が不足しています
- 404: ロットが見つかりません

---

#### GET /api/inventory/summary

**説明:** 商品別在庫サマリー（ダッシュボード用）

**認証:** 必要

**レスポンス (200 OK):**
```json
{
  "total_products": 150,
  "total_quantity": 480,
  "expiring_soon_count": 5,
  "low_stock_count": 12,
  "expiring_soon": [
    {
      "product_name": "明治おいしい牛乳 1L",
      "total_quantity": 2.0,
      "unit": "L",
      "earliest_expiry": "2025-03-20",
      "days_until_expiry": 9
    }
  ],
  "low_stock": [
    {
      "product_name": "キッコーマン醤油 500ml",
      "total_quantity": 2.0,
      "unit": "ml"
    }
  ]
}
```

**備考:**
- expiring_soon: 賞味期限が30日以内の商品
- low_stock: 総在庫数が5以下の商品

---

### 3.6 在庫履歴API

#### GET /api/inventory/history

**説明:** 在庫履歴取得

**認証:** 必要

**クエリパラメータ:**
| パラメータ | 型 | 説明 | デフォルト |
|-----------|---|------|-----------|
| product_id | integer | 商品でフィルタ | - |
| user_id | integer | ユーザーでフィルタ | - |
| transaction_type | string | 取引種別（購入/使用） | - |
| from_date | string | 開始日（YYYY-MM-DD） | - |
| to_date | string | 終了日（YYYY-MM-DD） | - |
| limit | integer | 件数 | 100 |

**リクエスト例:**
```
GET /api/inventory/history?product_id=3&limit=50
```

**レスポンス (200 OK):**
```json
{
  "items": [
    {
      "id": 11,
      "product_id": 3,
      "product_name": "明治おいしい牛乳 1L",
      "user": {
        "id": 1,
        "username": "tanaka"
      },
      "transaction_type": "使用",
      "quantity": 1.0,
      "storage_location_name": "冷蔵庫",
      "expiry_date": "2025-03-20",
      "created_at": "2025-03-11T11:00:00Z"
    },
    {
      "id": 10,
      "product_id": 3,
      "product_name": "明治おいしい牛乳 1L",
      "user": {
        "id": 1,
        "username": "tanaka"
      },
      "transaction_type": "購入",
      "quantity": 2.0,
      "storage_location_name": "冷蔵庫",
      "expiry_date": "2025-03-20",
      "created_at": "2025-03-11T10:00:00Z"
    }
  ],
  "total": 50
}
```

---

### 3.7 買い物リストAPI

#### GET /api/shopping-list

**説明:** 買い物リスト一覧取得

**認証:** 必要

**クエリパラメータ:**
| パラメータ | 型 | 説明 | デフォルト |
|-----------|---|------|-----------|
| is_purchased | boolean | 購入済みフラグ | false |

**リクエスト例:**
```
GET /api/shopping-list?is_purchased=false
```

**レスポンス (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "product_id": 1,
      "product_name": "キッコーマン醤油 500ml",
      "quantity": 2.0,
      "unit": "ml",
      "is_purchased": false,
      "added_by": {
        "id": 1,
        "username": "tanaka"
      },
      "purchased_at": null,
      "created_at": "2025-03-10T10:00:00Z"
    },
    {
      "id": 2,
      "product_id": null,
      "product_name": "トイレットペーパー",
      "quantity": 12.0,
      "unit": "ロール",
      "is_purchased": false,
      "added_by": {
        "id": 2,
        "username": "suzuki"
      },
      "purchased_at": null,
      "created_at": "2025-03-11T08:00:00Z"
    }
  ],
  "total": 5
}
```

---

#### POST /api/shopping-list

**説明:** 買い物リストに追加

**認証:** 必要

**リクエスト（商品マスタから追加）:**
```json
{
  "product_id": 1,
  "quantity": 2.0
}
```

**リクエスト（手動追加）:**
```json
{
  "product_name": "トイレットペーパー",
  "quantity": 12.0,
  "unit": "ロール"
}
```

**バリデーション:**
- product_id または product_name: いずれか必須
- quantity: 必須、0より大きい
- unit: product_id が null の場合は必須

**処理:**
- product_id がある場合：商品情報（名前、単位）を自動取得
- product_id が null の場合：手動入力された商品として登録

**レスポンス (201 Created):**
```json
{
  "id": 3,
  "product_id": 1,
  "product_name": "キッコーマン醤油 500ml",
  "quantity": 2.0,
  "unit": "ml",
  "is_purchased": false,
  "added_by": {
    "id": 1,
    "username": "tanaka"
  },
  "purchased_at": null,
  "created_at": "2025-03-11T12:00:00Z"
}
```

**エラー:**
- 400: バリデーションエラー
- 404: 商品が見つかりません（product_id 指定時）

---

#### PATCH /api/shopping-list/:id

**説明:** 購入済みに更新

**認証:** 必要

**リクエスト:**
```json
{
  "is_purchased": true
}
```

**レスポンス (200 OK):**
```json
{
  "id": 1,
  "product_id": 1,
  "product_name": "キッコーマン醤油 500ml",
  "quantity": 2.0,
  "unit": "ml",
  "is_purchased": true,
  "added_by": {
    "id": 1,
    "username": "tanaka"
  },
  "purchased_at": "2025-03-11T12:00:00Z",
  "created_at": "2025-03-10T10:00:00Z"
}
```

**エラー:**
- 404: アイテムが見つかりません

---

#### DELETE /api/shopping-list/:id

**説明:** 買い物リストから削除

**認証:** 必要

**レスポンス (200 OK):**
```json
{
  "message": "リストから削除しました"
}
```

**エラー:**
- 404: アイテムが見つかりません

---

## 4. エラーレスポンス詳細

### 4.1 バリデーションエラー (400)

```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "password"],
      "msg": "ensure this value has at least 4 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

### 4.2 認証エラー (401)

```json
{
  "detail": "Could not validate credentials"
}
```

### 4.3 Not Found (404)

```json
{
  "detail": "商品が見つかりません"
}
```

### 4.4 Conflict (409)

```json
{
  "detail": "ユーザー名は既に使用されています"
}
```

---

## 5. 認証フロー

### 5.1 ユーザー登録 → ログイン

```
1. POST /api/users/register
   → ユーザー作成

2. POST /api/users/login
   → トークン取得

3. 以降のリクエストでトークンを使用
   Authorization: Bearer {token}
```

### 5.2 トークンの使用

```http
GET /api/inventory/lots HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 5.3 トークンの有効期限切れ

```
トークン有効期限: 30分

期限切れの場合:
→ 401 Unauthorized
→ フロントエンドで /login にリダイレクト
```

---

## 6. CORS設定

**実装:** django-cors-headers パッケージ使用

**開発環境（settings.py）:**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True
```

**本番環境:**
```python
CORS_ALLOWED_ORIGINS = [
    "https://inventory.example.com",
]
```

---

## 7. レート制限

**現時点では実装しない**

将来的に検討：
- 認証API: 10リクエスト/分
- その他API: 100リクエスト/分

---

## 8. ページネーション

**採用方式:** オフセットベース

**クエリパラメータ:**
- `page`: ページ番号（1から開始）
- `limit`: 1ページあたりの件数

**レスポンス:**
```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8
}
```

---

## 9. 日付・時刻フォーマット

**すべての日時:** ISO 8601 形式（UTC）
```
2025-03-11T10:00:00Z
```

**日付のみ:** YYYY-MM-DD
```
2025-03-20
```

---

## 10. 実装の優先順位

### Phase 1: 必須機能
1. 認証API
2. 商品マスタAPI
3. 在庫ロットAPI（一覧、詳細、購入、使用）
4. カテゴリAPI
5. 保管場所API

### Phase 2: 拡張機能
6. 在庫履歴API
7. 買い物リストAPI
8. 在庫サマリーAPI

---

以上
