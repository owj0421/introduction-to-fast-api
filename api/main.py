from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import task, done

app = FastAPI()
app.include_router(task.router)
app.include_router(done.router)

# CORS 설정
# TODO: 나중에 공부할 것. CORS가 뭔지, 왜 필요한지, 어떻게 동작하는지
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}