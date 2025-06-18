from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import asyncio
from contextlib import asynccontextmanager
from routes.design_routes import router as design_router
from database.connection import connect_to_mongo, close_mongo_connection

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="AI House Design Generator",
    description="Generate house designs using AI",
    version="1.0.0",
    lifespan=lifespan
)    

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_header=["*"], 
)

# Include routers
app.include_router(design_router, prefix="/api", tags=["designs"])

@app.get("/")
async def root():
    return {"message": "AI House Design Generator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

