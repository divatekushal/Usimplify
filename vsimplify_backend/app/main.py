from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.routers import auth, companies, users, documents, invoices, suppliers, payments
from app.database import engine, Base, get_db
from app.models.user import User
from app.utils.auth import verify_password, create_access_token
from app.config import settings
from datetime import timedelta

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VSimplify Clone API",
    description="Backend API for VSimplify clone application",
    version="1.0.0"
)

# Template configuration
templates = Jinja2Templates(directory="templates")

# Static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Web routes for templates
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Authenticate user
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request, 
                "error": "Invalid email or password"
            }
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Redirect to dashboard with token (you can store in session/cookie)
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.access_token_expire_minutes * 60,
        secure=False  # Set to True in production with HTTPS
    )
    
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # You can add authentication check here
    return templates.TemplateResponse("accountant-dashboard.html", {"request": request})

# Include API routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(companies.router)
app.include_router(documents.router)
app.include_router(invoices.router)
app.include_router(suppliers.router)
app.include_router(payments.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
