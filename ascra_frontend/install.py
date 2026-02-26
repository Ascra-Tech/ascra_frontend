import os
import subprocess
import frappe
from frappe import _


def after_install():
    """Build frontend assets after app installation"""
    try:
        print("Building Ascra Frontend assets...")
        
        # Get the app path
        app_path = frappe.get_app_path("ascra_frontend")
        frontend_path = os.path.join(app_path, "..", "frontend")
        
        if os.path.exists(frontend_path):
            # Change to frontend directory
            os.chdir(frontend_path)
            
            # Install dependencies
            print("Installing frontend dependencies...")
            subprocess.run(["yarn", "install"], check=True)
            
            # Build the frontend
            print("Building frontend application...")
            subprocess.run(["yarn", "build"], check=True)
            
            print("✅ Frontend build completed successfully!")
            
        else:
            print("⚠️ Frontend directory not found, skipping build")
            
    except subprocess.CalledProcessError as e:
        frappe.log_error(f"Frontend build failed: {str(e)}")
        print(f"❌ Frontend build failed: {str(e)}")
        # Don't fail the installation if frontend build fails
        
    except Exception as e:
        frappe.log_error(f"Frontend installation error: {str(e)}")
        print(f"❌ Frontend installation error: {str(e)}")


def before_install():
    """Prepare for installation"""
    print("Preparing Ascra Frontend installation...")
