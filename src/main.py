from fastapi import FastAPI
from api.events.routing import router as event_router
from contextlib import asynccontextmanager
from api.db.session import init_db
from fastapi.middleware.cors import CORSMiddleware
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(event_router, prefix="/api/events")


@app.get("/")
def home():
    return {"message": "API is running"}


@app.get("/healthz")
def read_api_health():
    return {"status": "healthy"}
