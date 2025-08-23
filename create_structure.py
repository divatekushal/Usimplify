import os

# Define the project root
project_root = "vsimplify_backend"

# Define the full structure as a list of paths
structure = [
    "app/__init__.py",
    "app/main.py",
    "app/config.py",
    "app/database.py",
    
    # Models
    "app/models/__init__.py",
    "app/models/user.py",
    "app/models/company.py",
    "app/models/document.py",
    "app/models/invoice.py",
    "app/models/supplier.py",
    "app/models/payment.py",
    
    # Schemas
    "app/schemas/__init__.py",
    "app/schemas/user.py",
    "app/schemas/company.py",
    "app/schemas/document.py",
    "app/schemas/invoice.py",
    "app/schemas/supplier.py",
    "app/schemas/payment.py",
    
    # Routers
    "app/routers/__init__.py",
    "app/routers/auth.py",
    "app/routers/users.py",
    "app/routers/companies.py",
    "app/routers/documents.py",
    "app/routers/invoices.py",
    "app/routers/suppliers.py",
    "app/routers/payments.py",
    
    # Utils
    "app/utils/__init__.py",
    "app/utils/auth.py",
    "app/utils/dependencies.py",
    
    # Root files
    "requirements.txt",
    ".env"
]

def create_structure(root, file_list):
    """Creates the directory and file structure."""
    for path in file_list:
        full_path = os.path.join(root, path)
        dir_name = os.path.dirname(full_path)
        
        # Create directory if it doesn't exist
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"Created directory: {dir_name}")
        
        # Create the file (even if empty)
        if not os.path.exists(full_path):
            with open(full_path, 'w') as f:
                pass  # Just create an empty file
            print(f"Created file: {full_path}")
        else:
            print(f"File already exists: {full_path}")

if __name__ == "__main__":
    create_structure(project_root, structure)
    print("\n✅ Project structure created successfully!")