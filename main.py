from fastapi import FastAPI

app = FastAPI()


# :pathはいかなるパスにもマッチする
# curl http://127.0.0.1:8000/files//home/johndoe/myfile.txt
# → {"file_path":"/home/johndoe/myfile.txt"}%  
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
