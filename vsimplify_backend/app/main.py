from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, companies, users, documents, invoices, suppliers, payments
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VSimplify Clone API",
    description="Backend API for VSimplify clone application",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(companies.router)
app.include_router(documents.router)
app.include_router(invoices.router)
app.include_router(suppliers.router)
app.include_router(payments.router)

@app.get("/")
def read_root():
    return {"message": "VSimplify Clone API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
