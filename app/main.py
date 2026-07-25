from fastapi import FastAPI

app = FastAPI(title="F1 Analytics Pipeline")


@app.get("/")
def root():
    return {"status": "green"}