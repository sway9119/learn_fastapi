from typing import Union
from typing import List

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel


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
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

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

