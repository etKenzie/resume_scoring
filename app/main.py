from fastapi import FastAPI
from router import router as process_router

app = FastAPI()
app.include_router(process_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
