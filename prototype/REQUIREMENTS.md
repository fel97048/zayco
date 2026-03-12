# 家庭用在庫管理システム - 要件定義書

## 1. プロジェクト概要

### 1.1 目的
家庭内の食料品や日用品の在庫を効率的に管理するWebアプリケーションを開発する。

### 1.2 対象ユーザー
- 家族全員（複数ユーザー対応）
- 主な利用場所：自宅内ネットワーク

### 1.3 想定される商品規模
- 管理商品数：約100種類

## 2. 技術要件

### 2.1 技術スタック

#### バックエンド
- 言語：Python 3.11
- フレームワーク：FastAPI
- ORM：SQLAlchemy
- データベース：SQLite
- 認証：JWT (python-jose)
- パスワードハッシュ化：bcrypt (passlib)

#### フロントエンド
- 言語：TypeScript
- フレームワーク：Vue 3 (Composition API)
- 状態管理：Pinia
- ルーティング：Vue Router
- ビルドツール：Vite
- HTTPクライアント：Axios

#### インフラ
- コンテナ化：Docker + Docker Compose
- ポート設定：
  - フロントエンド：3000
  - バックエンド：8000

### 2.2 アクセス要件
- ブラウザ経由でアクセス可能
- レスポンシブデザイン（スマホ・タブレット・PC対応）
- 自宅内ネットワークのみでアクセス可能

## 3. 機能要件

### 3.1 認証・ユーザー管理

#### 3.1.1 ユーザー登録
- 機能：新規ユーザーアカウントの作成
- 入力項目：
  - ユーザー名（必須、一意）
  - パスワード（必須）
- バリデーション：
  - ユーザー名の重複チェック
  - パスワードのハッシュ化

#### 3.1.2 ログイン
- 機能：認証とJWTトークンの発行
- 入力項目：
  - ユーザー名
  - パスワード
- セッション管理：
  - トークンの有効期限：30分
  - ローカルストレージにトークンを保存

#### 3.1.3 ログアウト
- 機能：トークンの削除とログイン画面への遷移

### 3.2 カテゴリ管理

#### 3.2.1 カテゴリ一覧表示
- 機能：登録されているすべてのカテゴリを表示

#### 3.2.2 カテゴリ登録
- 機能：新しいカテゴリを追加
- 入力項目：
  - カテゴリ名（必須、一意）
- 例：調味料、飲料、洗剤、日用品、冷凍食品、缶詰

### 3.3 商品マスタ管理

#### 3.3.1 商品一覧表示
- 機能：登録されているすべての商品を一覧表示
- 表示項目：
  - 商品名
  - カテゴリ名
  - バーコード
  - 単位
  - 操作ボタン（編集・削除）

#### 3.3.2 商品登録
- 機能：新しい商品をマスタに追加
- 入力項目：
  - 商品名（必須）
  - カテゴリ（必須、セレクトボックス）
  - バーコード（任意）
  - 単位（必須、セレクトボックス）
- 単位の選択肢：個、本、袋、ml、g、kg、L
- 処理：商品登録時に在庫レコードも自動生成（初期在庫数：0）

#### 3.3.3 商品編集
- 機能：既存商品の情報を更新
- 編集可能項目：商品名、カテゴリ、バーコード、単位

#### 3.3.4 商品削除
- 機能：商品を削除（関連する在庫データも削除）
- 確認ダイアログ表示

### 3.4 在庫管理

#### 3.4.1 在庫一覧表示
- 機能：全商品の現在在庫を一覧表示
- 表示項目：
  - 商品名
  - カテゴリ名
  - 現在在庫数
  - 単位
  - 操作ボタン（購入・使用）
- 在庫数の色分け：
  - 0個：赤色（在庫切れ）
  - 1-5個：オレンジ色（在庫少）
  - 6個以上：緑色（在庫あり）

#### 3.4.2 検索機能
- 機能：商品名またはカテゴリ名で絞り込み検索

#### 3.4.3 購入（在庫追加）
- 機能：購入した商品の在庫を増やす
- 入力項目：
  - 数量（必須、0.1以上の数値）
- 処理：
  - 現在在庫数に加算
  - 履歴に記録（取引タイプ：購入）

#### 3.4.4 使用（在庫減算）
- 機能：使用した商品の在庫を減らす
- 入力項目：
  - 数量（必須、0.1以上の数値）
- バリデーション：
  - 在庫数が不足している場合はエラー
- 処理：
  - 現在在庫数から減算
  - 履歴に記録（取引タイプ：使用）

### 3.5 在庫履歴

#### 3.5.1 履歴一覧表示
- 機能：過去の在庫増減履歴を表示
- 表示項目：
  - 日時（年月日 時分）
  - 商品名
  - 取引タイプ（購入/使用）
  - 数量
- ソート：最新の履歴が上に表示
- 件数制限：最新100件

### 3.6 ダッシュボード

#### 3.6.1 統計情報表示
- 表示項目（カード形式）：
  - カテゴリ数
  - 商品数
  - 総在庫数
  - 在庫少商品数（5個以下）

#### 3.6.2 在庫アラート
- 機能：在庫が5個以下の商品を一覧表示
- 表示項目：
  - 商品名
  - カテゴリ
  - 在庫数（赤字で強調）
  - 単位

## 4. データベース設計

### 4.1 テーブル定義

#### 4.1.1 usersテーブル
```
カラム名           型          制約
----------------------------------------
id                INTEGER     PRIMARY KEY
username          VARCHAR     UNIQUE, NOT NULL
hashed_password   VARCHAR     NOT NULL
created_at        DATETIME    DEFAULT CURRENT_TIMESTAMP
```

#### 4.1.2 categoriesテーブル
```
カラム名      型          制約
----------------------------------------
id           INTEGER     PRIMARY KEY
name         VARCHAR     UNIQUE, NOT NULL
created_at   DATETIME    DEFAULT CURRENT_TIMESTAMP
```

#### 4.1.3 productsテーブル
```
カラム名       型          制約
----------------------------------------
id            INTEGER     PRIMARY KEY
name          VARCHAR     NOT NULL
category_id   INTEGER     FOREIGN KEY (categories.id), NOT NULL
barcode       VARCHAR     UNIQUE, NULL
unit          VARCHAR     NOT NULL, DEFAULT '個'
created_at    DATETIME    DEFAULT CURRENT_TIMESTAMP
```

#### 4.1.4 inventoryテーブル
```
カラム名       型          制約
----------------------------------------
id            INTEGER     PRIMARY KEY
product_id    INTEGER     FOREIGN KEY (products.id), UNIQUE, NOT NULL
quantity      FLOAT       NOT NULL, DEFAULT 0
expiry_date   DATETIME    NULL (将来実装)
updated_at    DATETIME    DEFAULT CURRENT_TIMESTAMP
```

#### 4.1.5 inventory_historyテーブル
```
カラム名           型          制約
----------------------------------------
id                INTEGER     PRIMARY KEY
product_id        INTEGER     FOREIGN KEY (products.id), NOT NULL
user_id           INTEGER     FOREIGN KEY (users.id), NOT NULL
transaction_type  VARCHAR     NOT NULL ('購入' or '使用')
quantity          FLOAT       NOT NULL
created_at        DATETIME    DEFAULT CURRENT_TIMESTAMP
```

### 4.2 リレーション
- categories 1 : N products
- products 1 : 1 inventory
- products 1 : N inventory_history
- users 1 : N inventory_history

## 5. API仕様

### 5.1 エンドポイント一覧

#### 認証API

```
POST /api/users/register
説明：新規ユーザー登録
リクエストボディ：
{
  "username": "string",
  "password": "string"
}
レスポンス：
{
  "id": 1,
  "username": "string",
  "created_at": "2024-01-01T00:00:00"
}
```

```
POST /api/users/login
説明：ログイン
リクエストボディ：
{
  "username": "string",
  "password": "string"
}
レスポンス：
{
  "access_token": "string",
  "token_type": "bearer"
}
```

```
GET /api/users/me
説明：現在のユーザー情報取得
認証：必要
レスポンス：
{
  "id": 1,
  "username": "string",
  "created_at": "2024-01-01T00:00:00"
}
```

#### カテゴリAPI

```
GET /api/categories
説明：カテゴリ一覧取得
認証：必要
レスポンス：
[
  {
    "id": 1,
    "name": "string",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

```
POST /api/categories
説明：カテゴリ作成
認証：必要
リクエストボディ：
{
  "name": "string"
}
レスポンス：
{
  "id": 1,
  "name": "string",
  "created_at": "2024-01-01T00:00:00"
}
```

#### 商品API

```
GET /api/products
説明：商品一覧取得
認証：必要
レスポンス：
[
  {
    "id": 1,
    "name": "string",
    "category_id": 1,
    "category": {
      "id": 1,
      "name": "string",
      "created_at": "2024-01-01T00:00:00"
    },
    "barcode": "string",
    "unit": "個",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

```
POST /api/products
説明：商品作成
認証：必要
リクエストボディ：
{
  "name": "string",
  "category_id": 1,
  "barcode": "string",
  "unit": "個"
}
レスポンス：商品オブジェクト
```

```
PUT /api/products/{product_id}
説明：商品更新
認証：必要
リクエストボディ：
{
  "name": "string",
  "category_id": 1,
  "barcode": "string",
  "unit": "個"
}
レスポンス：更新された商品オブジェクト
```

```
DELETE /api/products/{product_id}
説明：商品削除
認証：必要
レスポンス：
{
  "message": "商品を削除しました"
}
```

#### 在庫API

```
GET /api/inventory
説明：在庫一覧取得
認証：必要
レスポンス：
[
  {
    "id": 1,
    "product_id": 1,
    "product": { 商品オブジェクト },
    "quantity": 10,
    "expiry_date": null,
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

```
POST /api/inventory/transaction
説明：在庫増減取引
認証：必要
リクエストボディ：
{
  "product_id": 1,
  "transaction_type": "購入",  // or "使用"
  "quantity": 5
}
レスポンス：
{
  "id": 1,
  "product_id": 1,
  "user_id": 1,
  "transaction_type": "購入",
  "quantity": 5,
  "created_at": "2024-01-01T00:00:00"
}
```

```
GET /api/inventory/history
説明：在庫履歴取得
認証：必要
レスポンス：履歴オブジェクトの配列（最新100件）
```

### 5.2 認証方式
- JWT (JSON Web Token)
- Authorizationヘッダーに `Bearer {token}` 形式で送信
- トークン有効期限：30分

### 5.3 CORS設定
- 許可オリジン：http://localhost:3000
- 許可メソッド：すべて
- 認証情報の送信：許可

## 6. UI/UX要件

### 6.1 画面一覧

#### 6.1.1 ログイン/登録画面
- レイアウト：中央配置のカード形式
- 背景：グラデーション
- ログイン/登録の切り替え可能
- エラーメッセージ表示領域

#### 6.1.2 ダッシュボード
- 統計カード（4枚）をグリッド配置
- 在庫少商品テーブル
- レスポンシブ：モバイルでは2列表示

#### 6.1.3 商品管理画面
- アクションボタン：カテゴリ追加、商品追加
- 商品一覧テーブル
- モーダル：商品追加/編集フォーム
- モーダル：カテゴリ追加フォーム

#### 6.1.4 在庫管理画面
- 検索ボックス
- 在庫一覧テーブル
- アクションボタン：購入、使用
- モーダル：数量入力フォーム

#### 6.1.5 履歴画面
- 履歴テーブル（日時降順）
- 取引タイプの色分け

### 6.2 ナビゲーション
- 上部に固定ナビゲーションバー
- メニュー項目：
  - ダッシュボード
  - 商品管理
  - 在庫管理
  - 履歴
- 右端：ユーザー名とログアウトボタン
- アクティブメニューのハイライト

### 6.3 デザインガイドライン

#### カラーパレット
- プライマリ：#4CAF50（緑）
- セカンダリ：#2196F3（青）
- 危険：#f44336（赤）
- 警告：#ff9800（オレンジ）
- 背景：#f5f5f5
- カード背景：白

#### タイポグラフィ
- フォントファミリー：システムフォント
- 見出し：太字
- 本文：14px

#### ボタンスタイル
- プライマリボタン：緑背景、白文字
- セカンダリボタン：青背景、白文字
- 危険ボタン：赤背景、白文字
- ホバー時：明度変更
- パディング：10px 20px
- ボーダー半径：4px

#### レスポンシブ
- ブレークポイント：768px
- モバイル時：
  - ナビゲーション：縦並び
  - テーブル：フォントサイズ縮小
  - ボタン：フル幅

## 7. ファイル構成

### 7.1 プロジェクト構造

```
inventory-system/
├── docker-compose.yml
├── .gitignore
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   └── data/           # SQLiteデータベース保存先
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── tsconfig.json
    ├── tsconfig.node.json
    ├── vite.config.ts
    ├── index.html
    └── src/
        ├── main.ts
        ├── App.vue
        ├── env.d.ts
        ├── api/
        │   └── index.ts
        ├── components/
        │   └── Layout.vue
        ├── views/
        │   ├── LoginView.vue
        │   ├── DashboardView.vue
        │   ├── ProductsView.vue
        │   ├── InventoryView.vue
        │   └── HistoryView.vue
        ├── stores/
        │   ├── auth.ts
        │   └── inventory.ts
        ├── router/
        │   └── index.ts
        └── types/
            └── index.ts
```

### 7.2 ファイルの役割

#### バックエンド
- `main.py`：FastAPIアプリケーション、エンドポイント定義
- `models.py`：SQLAlchemyモデル定義
- `schemas.py`：Pydanticスキーマ定義
- `database.py`：データベース接続設定
- `auth.py`：認証関連ユーティリティ
- `requirements.txt`：Python依存パッケージ

#### フロントエンド
- `main.ts`：アプリケーションエントリーポイント
- `App.vue`：ルートコンポーネント
- `api/index.ts`：API通信ロジック
- `components/Layout.vue`：共通レイアウトコンポーネント
- `views/*.vue`：各ページコンポーネント
- `stores/*.ts`：Piniaストア（状態管理）
- `router/index.ts`：Vue Routerルート定義
- `types/index.ts`：TypeScript型定義

## 8. Docker設定

### 8.1 docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: inventory-backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - inventory-data:/app/data
    environment:
      - DATABASE_URL=sqlite:///data/inventory.db
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    container_name: inventory-frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000
    command: npm run dev -- --host 0.0.0.0

volumes:
  inventory-data:
```

### 8.2 バックエンドDockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### 8.3 フロントエンドDockerfile

```dockerfile
FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

## 9. セットアップ手順

### 9.1 前提条件
- Docker Desktop インストール済み
- Docker Compose インストール済み

### 9.2 起動手順

1. プロジェクトディレクトリに移動
```bash
cd inventory-system
```

2. コンテナのビルドと起動
```bash
docker-compose up -d
```

3. アクセス確認
- フロントエンド：http://localhost:3000
- バックエンドAPI：http://localhost:8000
- APIドキュメント：http://localhost:8000/docs

### 9.3 初期データ作成

1. ユーザー登録
   - ブラウザで http://localhost:3000 にアクセス
   - 「新規登録はこちら」から最初のユーザーを作成

2. 初期カテゴリ作成例
   - 調味料
   - 飲料
   - 日用品
   - 冷凍食品
   - 缶詰

3. サンプル商品登録例
   - 醤油（調味料、500ml）
   - コーラ（飲料、1.5L）
   - トイレットペーパー（日用品、ロール）

## 10. 将来実装予定の機能（プロトタイプでは未実装）

### 10.1 賞味期限管理
- inventory テーブルの expiry_date を使用
- 期限切れアラート表示
- 期限順ソート機能

### 10.2 バーコード読み取り
- スマホカメラでバーコードスキャン
- 商品情報の自動入力

### 10.3 通知機能
- 在庫少ない商品の通知
- 賞味期限が近い商品の通知

### 10.4 その他
- 買い物リスト自動生成
- レポート・分析機能
- データエクスポート/インポート

## 11. 非機能要件

### 11.1 パフォーマンス
- ページ読み込み：3秒以内
- API応答時間：500ms以内（通常時）

### 11.2 セキュリティ
- パスワードのbcryptハッシュ化
- JWT認証
- CORS設定による不正アクセス防止
- SQLインジェクション対策（SQLAlchemy使用）

### 11.3 可用性
- Dockerによる環境の一貫性確保
- データベースファイルのボリュームマウント

### 11.4 保守性
- TypeScriptによる型安全性
- コンポーネント指向設計
- RESTful API設計

## 12. 制約事項

- 外部ネットワークからのアクセス不可（自宅内限定）
- 商品画像のアップロード機能なし
- 賞味期限管理は将来実装
- バーコード読み取りは将来実装
- プッシュ通知なし

## 13. 開発上の注意事項

### 13.1 環境変数
- `VITE_API_URL`：フロントエンドからバックエンドへの接続URL
- `DATABASE_URL`：データベース接続文字列

### 13.2 データの永続化
- SQLiteデータベースファイルはDockerボリュームに保存
- コンテナ再起動してもデータは保持される
- データリセット時は `docker-compose down -v` でボリュームも削除

### 13.3 開発時のホットリロード
- バックエンド：`--reload` オプションでコード変更時に自動再起動
- フロントエンド：Viteの開発サーバーで自動リロード

### 13.4 APIドキュメント
- FastAPIの自動生成ドキュメント：http://localhost:8000/docs
- テスト時に活用可能

---

この要件定義書に基づいてシステムを実装すること。
