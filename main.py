from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import datetime
import os

# Create FastAPI instance
app = FastAPI(
    title="FinanceFlow Owner Dashboard",
    description="Professional Financial Management Dashboard",
    version="1.0.0"
)

# Mount static files (CSS, JS, Images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Custom template filters and globals
def format_currency(amount):
    """Format number as Indian currency"""
    return f"₹{amount:,.0f}"

def format_number(number):
    """Format number with commas"""
    return f"{number:,}"

# Add custom functions to Jinja2 environment
templates.env.filters["currency"] = format_currency
templates.env.filters["number"] = format_number
templates.env.globals["now"] = datetime.now

# Sample data (in production, this would come from database)
SAMPLE_DATA = {
    "invoices": {
        "submitted_processing": 847,
        "ready_posting": 1245,
        "posted": 692,
        "exception": 63
    },
    "books": {
        "closed": 34,
        "pending": 6
    },
    "next_posting": {
        "sales": 2500000,
        "purchases": 1820000,
        "expenses": 850000,
        "others": 320000
    },
    "bank_statements": {
        "submitted": 156,
        "verified": 142,
        "exceptions": 8,
        "processed": 128,
        "posted": 115,
        "progress": 87.8
    },
    "recent_transactions": [
        {
            "date": "Aug 20",
            "id": "INV-1247",
            "type": "Invoice",
            "customer": "Acme Corporation",
            "amount": 1245000,
            "status": "processed"
        },
        {
            "date": "Aug 19",
            "id": "PO-892",
            "type": "Purchase",
            "customer": "Tech Suppliers",
            "amount": 875000,
            "status": "verified"
        },
        {
            "date": "Aug 18",
            "id": "EXP-421",
            "type": "Expense",
            "customer": "Office Maintenance",
            "amount": 45000,
            "status": "pending"
        },
        {
            "date": "Aug 17",
            "id": "INV-246",
            "type": "Invoice",
            "customer": "Beta Enterprises",
            "amount": 680000,
            "status": "exception"
        }
    ]
}

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Redirect to dashboard"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": SAMPLE_DATA
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "data": SAMPLE_DATA,
        "page_title": "Financial Dashboard",
        "page_subtitle": "Real-time financial operations overview"
    })
    
@app.get("/transactions", response_class=HTMLResponse)
async def transactions(request: Request):
    """Transactions management page"""
    return templates.TemplateResponse("transactions.html", {
        "request": request
    })


@app.get("/bank", response_class=HTMLResponse)
async def bank(request: Request):
    """Bank management page"""
    bank_data = {
        "banks": [
            {
                "id": "hdfc",
                "name": "HDFC Bank", 
                "accounts": 3, 
                "total_balance": 4520000,
                "logo_color": "blue"
            },
            {
                "id": "icici", 
                "name": "ICICI Bank", 
                "accounts": 2, 
                "total_balance": 2880000,
                "logo_color": "red"
            },
            {
                "id": "sbi", 
                "name": "SBI Bank", 
                "accounts": 1, 
                "total_balance": 1560000,
                "logo_color": "green"
            },
            {
                "id": "axis", 
                "name": "Axis Bank", 
                "accounts": 2, 
                "total_balance": 3240000,
                "logo_color": "orange"
            }
        ]
    }
    
    return templates.TemplateResponse("bank.html", {
        "request": request,
        "data": bank_data,
        "page_title": "Bank Management",
        "page_subtitle": "Manage your bank accounts and transactions"
    })

@app.get("/books", response_class=HTMLResponse)
async def books(request: Request):
    """Books management page with advanced filtering"""
    return templates.TemplateResponse("books.html", {
        "request": request,
        "page_title": "Books Management",
        "page_subtitle": "Manage your monthly accounting books and records"
    })



@app.get("/customers", response_class=HTMLResponse)
async def customers(request: Request):
    """Customer management page with data table"""
    return templates.TemplateResponse("customers.html", {
        "request": request,
        "page_title": "Customer Management",
        "page_subtitle": "Manage customer relationships and account details"
    })

@app.get("/customer/{customer_id}", response_class=HTMLResponse)
async def customer_detail(customer_id: int, request: Request):
    """Customer detail page"""
    
    # Sample customer data
    customer_data = {
        1: {
            "id": 1,
            "name": "Acme Corporation",
            "code": "ACM001",
            "ledger_name": "Acme Corp - Sales",
            "customer_since": "Jan 15, 2020",
            "primary_contact": "John Smith",
            "phone": "+91 98765 43210",
            "email": "accounts@acmecorp.com",
            "address": "123 Business Park, Mumbai, Maharashtra - 400001",
            "gst_number": "27AAACA1234B1Z5",
            "gst_type": "Regular",
            "state_code": "27 - Maharashtra",
            "gst_reg_date": "Jan 20, 2020",
            "total_receivable": 1250000,
            "receipts": 800000,
            "balance": 450000,
            "days_outstanding": 45,
            "credit_limit": 2000000,
            "payment_terms": 30,
            "last_payment_date": "Aug 15, 2025",
            "last_payment_amount": 125000,
            "status": "active",
            "pan_uploaded": True,
            "aadhar_uploaded": False,
            "recent_activities": [
                {"description": "Payment received ₹1,25,000", "date": "Aug 15, 2025"},
                {"description": "Invoice INV-1247 created", "date": "Aug 12, 2025"},
                {"description": "GST details updated", "date": "Aug 10, 2025"},
                {"description": "Credit limit increased", "date": "Aug 05, 2025"}
            ]
        }
    }
    
    customer = customer_data.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return templates.TemplateResponse("customer-detail.html", {
        "request": request,
        "customer": customer
    })


@app.get("/inventory", response_class=HTMLResponse)
async def inventory(request: Request):
    """Inventory management page"""
    inventory_data = {
        "total_items": 1240,
        "low_stock": 23,
        "out_of_stock": 5,
        "categories": [
            {"name": "Electronics", "items": 456, "value": 2500000},
            {"name": "Furniture", "items": 234, "value": 1200000},
            {"name": "Stationery", "items": 550, "value": 85000},
        ]
    }
    
    return templates.TemplateResponse("inventory.html", {
        "request": request,
        "data": inventory_data,
        "page_title": "Inventory Management",
        "page_subtitle": "Track and manage your inventory"
    })

@app.get("/suppliers", response_class=HTMLResponse)
async def suppliers(request: Request):
    """Supplier management page with data table"""
    return templates.TemplateResponse("suppliers.html", {
        "request": request,
        "page_title": "Supplier Management",
        "page_subtitle": "Manage supplier relationships and payment details"
    })

@app.get("/supplier/{supplier_id}", response_class=HTMLResponse)
async def supplier_detail(supplier_id: int, request: Request):
    """Supplier detail page"""
    
    # Sample supplier data (in production, fetch from database)
    supplier_data = {
        1: {
            "id": 1,
            "name": "Alpha Steel Industries",
            "code": "ASI001",
            "ledger": "Alpha Steel - Raw Materials",
            "payable": 1250000,
            "paid": 850000,
            "balance": 400000,
            "since": "March 15, 2020",
            "contact_person": "Rajesh Kumar",
            "phone": "+91 98765 43210",
            "email": "rajesh@alphasteel.com",
            "address": "123 Industrial Area, Sector 45, Gurugram, Haryana - 122003",
            "gst_number": "06AAACA1234B1Z5",
            "total_orders": 48
        }
        # Add more supplier data as needed
    }
    
    supplier = supplier_data.get(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    return templates.TemplateResponse("supplier-detail.html", {
        "request": request,
        "supplier": supplier
    })

@app.get("/accountant", response_class=HTMLResponse)
async def accountant_profile(request: Request):
    """Accountant profile and management page"""
    return templates.TemplateResponse("accountant.html", {
        "request": request,
        "page_title": "Accountant Management",
        "page_subtitle": "Comprehensive Accountant Profile & Activity Management"
    })


# API endpoints for AJAX requests
@app.get("/api/dashboard-data")
async def get_dashboard_data():
    """API endpoint to get dashboard data"""
    return SAMPLE_DATA

@app.get("/api/transactions")
async def get_transactions(limit: int = 10):
    """API endpoint to get recent transactions"""
    return {
        "transactions": SAMPLE_DATA["recent_transactions"][:limit],
        "total": len(SAMPLE_DATA["recent_transactions"])
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {
        "request": request,
        "page_title": "Page Not Found",
        "page_subtitle": "The requested page could not be found"
    }, status_code=404)



# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/accountant/dashboard", response_class=HTMLResponse)
async def accountant_dashboard(request: Request):
    """Accountant dashboard with document management"""
    return templates.TemplateResponse("accountant-dashboard.html", {
        "request": request
    })



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8080, 
        reload=True,
        log_level="info"
    )
