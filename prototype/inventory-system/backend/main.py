from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from database import init_db, get_db
from models import User, Category, Product, Inventory, InventoryHistory
from schemas import (
    UserCreate, UserResponse, Token, LoginRequest,
    CategoryCreate, CategoryResponse,
    ProductCreate, ProductUpdate, ProductResponse,
    InventoryResponse, InventoryHistoryCreate, InventoryHistoryResponse
)
from auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI(title="家庭用在庫管理システム")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データベース初期化
@app.on_event("startup")
def on_startup():
    init_db()

# ヘルスチェック
@app.get("/")
def read_root():
    return {"message": "在庫管理システムAPI"}

# ユーザー登録
@app.post("/api/users/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="ユーザー名は既に使用されています")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ログイン
@app.post("/api/users/login", response_model=Token)
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_req.username).first()
    if not user or not verify_password(login_req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 現在のユーザー情報取得
@app.get("/api/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# カテゴリ一覧取得
@app.get("/api/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    categories = db.query(Category).all()
    return categories

# カテゴリ作成
@app.post("/api/categories", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# 商品一覧取得
@app.get("/api/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    products = db.query(Product).all()
    return products

# 商品作成
@app.post("/api/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # 在庫レコードも同時に作成
    inventory = Inventory(product_id=db_product.id, quantity=0)
    db.add(inventory)
    db.commit()
    
    return db_product

# 商品更新
@app.put("/api/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    
    update_data = product.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

# 商品削除
@app.delete("/api/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    
    # 関連する在庫と履歴も削除
    db.query(Inventory).filter(Inventory.product_id == product_id).delete()
    db.query(InventoryHistory).filter(InventoryHistory.product_id == product_id).delete()
    db.delete(db_product)
    db.commit()
    return {"message": "商品を削除しました"}

# 在庫一覧取得
@app.get("/api/inventory", response_model=List[InventoryResponse])
def get_inventory(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    inventory = db.query(Inventory).all()
    return inventory

# 在庫更新（購入・使用）
@app.post("/api/inventory/transaction", response_model=InventoryHistoryResponse)
def create_inventory_transaction(
    transaction: InventoryHistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 在庫レコードを取得
    inventory = db.query(Inventory).filter(Inventory.product_id == transaction.product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="在庫が見つかりません")
    
    # 在庫数を更新
    if transaction.transaction_type == "購入":
        inventory.quantity += transaction.quantity
    elif transaction.transaction_type == "使用":
        if inventory.quantity < transaction.quantity:
            raise HTTPException(status_code=400, detail="在庫が不足しています")
        inventory.quantity -= transaction.quantity
    else:
        raise HTTPException(status_code=400, detail="不正な取引タイプです")
    
    # 履歴を作成
    history = InventoryHistory(
        product_id=transaction.product_id,
        user_id=current_user.id,
        transaction_type=transaction.transaction_type,
        quantity=transaction.quantity
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    
    return history

# 在庫履歴取得
@app.get("/api/inventory/history", response_model=List[InventoryHistoryResponse])
def get_inventory_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history = db.query(InventoryHistory).order_by(InventoryHistory.created_at.desc()).limit(100).all()
    return history
