from fastapi import FastAPI
app = FastAPI()
@app.get("/hello/")


def world(name:str,price:float):
    return {"message": f"Hello,{name}!,your actual price is {price}"}

def home(name:str,price:float):
    return {"message": f"Hello,{name}!,your price is {price}"}