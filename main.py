from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# :pathはいかなるパスにもマッチする
# curl http://127.0.0.1:8000/files//home/johndoe/myfile.txt
# → {"file_path":"/home/johndoe/myfile.txt"}%  
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# クエリパラメータ
# curl "http://127.0.0.1:8000/items/?skip=0&limit=10"
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

