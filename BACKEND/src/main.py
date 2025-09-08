from fastapi import FastAPI


app = FastAPI()

@app.get('/')
def hello():
    return {"MESSAGE": "HELLO WORLD"}