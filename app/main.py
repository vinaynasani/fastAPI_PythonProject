from fastapi import FastAPI
from . import models
from .database import engine, get_db
from .routers import post, user, auth, vote
from .config import settings

#import for CORS
from fastapi.middleware.cors import CORSMiddleware

# not more needed as alembic will take care of table creation and all, versioning and stuff
# models.Base.metadata.create_all(bind=engine)


# cross origin resourse sharing (CORS)to enable browsers to talk from different domain like from google.com to our local host etc

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {'message':'hello world'}




