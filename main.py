from typing import Union
from typing import List

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field


app = FastAPI()

# 起動するコマンド: $ uvicorn main:app --reload

# :pathはいかなるパスにもマッチする
# curl http://127.0.0.1:8000/files//home/johndoe/myfile.txt
# → {"file_path":"/home/johndoe/myfile.txt"}%  
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# クエリパラメータ
# curl "http://127.0.0.1:8000/items/?skip=0&limit=10"
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]

# モデルの使用
# curl "http://127.0.0.1:8000/items/?name=foo&price=4.2"
class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.post("/items/")
async def create_item(item: Item):
    return item

# リクエストボディ + パスパラメータ
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# より多くのメタデータを宣言する
# curl -X 'GET' 'http://127.0.0.1:8000/items/' -H 'accept: application/json'
@app.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# updateメソッド、複数のbodyパラメータ
# curl -X 'PUT' 'http://127.0.0.1:8000/items/1' -H 'accept: application/json'
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results
