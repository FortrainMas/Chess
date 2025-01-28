from fastapi import FastAPI
from api.v1.game_endpoints import router as game_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_router, prefix="/api/v1", tags=["Games"])

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI app"}
