import frappe
from frappe import _
from frappe.utils import validate_email_address, today, now_datetime, getdate
import re
import json

@frappe.whitelist(allow_guest=True)
def create_user_account(email, first_name, last_name, password, company=None):
    """
    Create a new user account
    """
    try:
        # Validate email
        if not email or not validate_email_address(email):
            frappe.throw(_("Please enter a valid email address"))
        
        # Check if user already exists
        if frappe.db.exists("User", email):
            frappe.throw(_("User with this email already exists"))
        
        # Validate names
        if not first_name or not last_name:
            frappe.throw(_("First name and last name are required"))
        
        # Validate password
        if not password or len(password.strip()) < 8:
            frappe.throw(_("Password must be at least 8 characters long"))
        
        # Create full name
        full_name = f"{first_name.strip()} {last_name.strip()}"
        
        # Create new user with minimal required fields
        user_doc = {
            "doctype": "User",
            "email": email.strip(),
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "full_name": full_name,
            "enabled": 1,
            "user_type": "Website User",
            "send_welcome_email": 0
        }
        
        # Add company if provided
        if company and company.strip():
            user_doc["company"] = company.strip()
        
        # Create and insert the user
        user = frappe.get_doc(user_doc)
        user.flags.ignore_permissions = True
        user.flags.ignore_mandatory = True
        
        # Add necessary roles for Website Users
        user.append("roles", {"role": "Guest"})
        
        user.insert()
        
        # Set password properly using Frappe's password utilities
        from frappe.utils.password import update_password
        update_password(user.name, password.strip())
        
        # Send welcome email (optional)
        try:
            user.send_welcome_mail_to_user()
        except Exception as email_error:
            frappe.log_error(f"Welcome email sending failed: {str(email_error)}")
            # Continue even if email fails
        
        return {
            "success": True,
            "message": _("Account created successfully! You can now login with your email and password."),
            "user_id": user.name
        }
        
    except frappe.DuplicateEntryError:
        frappe.throw(_("User with this email already exists"))
    except frappe.ValidationError as e:
        frappe.log_error(f"User validation error: {str(e)}")
        frappe.throw(str(e))
    except Exception as e:
        frappe.log_error(f"User creation error: {str(e)}")
        frappe.throw(f"An error occurred while creating your account: {str(e)}")

@frappe.whitelist(allow_guest=True)
def login_user(email, password):
    """
    Custom login API for Website Users
    """
    try:
        # Validate input
        if not email or not password:
            frappe.throw(_("Email and password are required"))
        
        # Validate email format
        if not validate_email_address(email):
            frappe.throw(_("Please enter a valid email address"))
        
        # Check if user exists
        if not frappe.db.exists("User", email):
            frappe.throw(_("Invalid email or password"))
        
        # Get user document
        user = frappe.get_doc("User", email)
        
        # Check if user is enabled
        if not user.enabled:
            frappe.throw(_("Your account has been disabled. Please contact administrator."))
        
        # Verify password
        from frappe.utils.password import check_password
        try:
            check_password(email, password)
        except frappe.AuthenticationError:
            frappe.throw(_("Invalid email or password"))
        
        # Simple authentication - let the frontend handle session management
        # Just verify credentials and return user info
        
        # Get default route for Website Users
        default_route = "/dashboard"  # or get from user preferences
        
        return {
            "success": True,
            "message": _("Login successful"),
            "user": email,
            "full_name": user.full_name,
            "default_route": default_route
        }
        
    except Exception as e:
        frappe.log_error(f"Login error: {str(e)}")
        if isinstance(e, frappe.AuthenticationError):
            frappe.throw(_("Invalid email or password"))
        else:
            frappe.throw(str(e))

@frappe.whitelist(allow_guest=True)
def check_email_availability(email):
    """
    Check if email is available for registration
    """
    try:
        if not email or not validate_email_address(email):
            return {"available": False, "message": "Invalid email format"}
        
        exists = frappe.db.exists("User", email)
        return {
            "available": not exists,
            "message": "Email already registered" if exists else "Email available"
        }
    except Exception as e:
        frappe.log_error(f"Email check error: {str(e)}")
        return {"available": False, "message": "Error checking email availability"}

@frappe.whitelist(allow_guest=True)
def create_lead_and_contact(data):
    """
    Advanced contact form that creates Lead and Contact records
    """
    try:
        # Parse data if it's a string
        if isinstance(data, str):
            data = json.loads(data)
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'company_name', 'message']
        for field in required_fields:
            if not data.get(field):
                frappe.throw(_(f"{field.replace('_', ' ').title()} is required"))
        
        # Validate email
        if not validate_email_address(data['email']):
            frappe.throw(_("Please enter a valid email address"))
        
        # Create Lead
        lead_doc = {
            "doctype": "Lead",
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email_id": data['email'],
            "mobile_no": data['phone'],
            "company_name": data['company_name'],
            "source": "Website",
            "status": "Lead",
            "request_type": data.get('request_type', 'Product Enquiry'),
            "industry": data.get('industry'),
            "job_title": data.get('job_title'),
            "website": data.get('website'),
            "city": data.get('city'),
            "state": data.get('state'),
            "country": data.get('country'),
            "annual_revenue": data.get('annual_revenue'),
            "no_of_employees": data.get('no_of_employees'),
            "territory": data.get('territory', 'All Territories'),
            "company": frappe.defaults.get_user_default("Company") or frappe.db.get_single_value("Global Defaults", "default_company")
        }
        
        lead = frappe.get_doc(lead_doc)
        lead.flags.ignore_permissions = True
        lead.insert()
        
        # Create Contact
        contact_doc = {
            "doctype": "Contact",
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email_id": data['email'],
            "phone": data['phone'],
            "mobile_no": data['phone'],
            "designation": data.get('job_title'),
            "company_name": data['company_name'],
            "status": "Open"
        }
        
        contact = frappe.get_doc(contact_doc)
        contact.flags.ignore_permissions = True
        contact.insert()
        
        # Link Contact to Lead
        contact.append("links", {
            "link_doctype": "Lead",
            "link_name": lead.name
        })
        contact.save()
        
        # Create Communication record for the message
        if data.get('message'):
            comm_doc = {
                "doctype": "Communication",
                "communication_type": "Communication",
                "communication_medium": "Email",
                "sent_or_received": "Received",
                "subject": f"Contact Form Inquiry from {data['first_name']} {data['last_name']}",
                "content": data['message'],
                "status": "Open",
                "reference_doctype": "Lead",
                "reference_name": lead.name,
                "sender": data['email'],
                "sender_full_name": f"{data['first_name']} {data['last_name']}"
            }
            
            comm = frappe.get_doc(comm_doc)
            comm.flags.ignore_permissions = True
            comm.insert()
        
        return {
            "success": True,
            "message": _("Thank you for your inquiry! We will get back to you soon."),
            "lead_id": lead.name,
            "contact_id": contact.name
        }
        
    except Exception as e:
        frappe.log_error(f"Lead/Contact creation error: {str(e)}")
        frappe.throw(f"An error occurred while processing your request: {str(e)}")

@frappe.whitelist()
def get_user_roles():
    """
    Get current user's roles
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            return {"roles": []}
        
        user_doc = frappe.get_doc("User", user)
        roles = [role.role for role in user_doc.roles]
        
        return {
            "success": True,
            "user": user,
            "roles": roles,
            "is_employee": "Employee" in roles
        }
        
    except Exception as e:
        frappe.log_error(f"Get user roles error: {str(e)}")
        return {"success": False, "message": str(e)}

@frappe.whitelist()
def get_employee_info():
    """
    Get employee information for logged-in user
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            frappe.throw(_("Please login to access employee information"))
        
        # Check if user has Employee role
        user_roles = frappe.get_roles(user)
        if "Employee" not in user_roles:
            frappe.throw(_("Access denied. Employee role required."))
        
        # Get employee record
        employee = frappe.db.get_value("Employee", {"user_id": user}, "*")
        if not employee:
            frappe.throw(_("Employee record not found for this user"))
        
        employee_doc = frappe.get_doc("Employee", employee.name)
        
        return {
            "success": True,
            "employee": {
                "name": employee_doc.name,
                "employee_name": employee_doc.employee_name,
                "designation": employee_doc.designation,
                "department": employee_doc.department,
                "company": employee_doc.company,
                "branch": employee_doc.branch,
                "employee_number": employee_doc.employee_number,
                "date_of_joining": employee_doc.date_of_joining,
                "status": employee_doc.status,
                "image": employee_doc.image
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Get employee info error: {str(e)}")
        frappe.throw(str(e))

@frappe.whitelist()
def mark_attendance(status="Present", attendance_date=None):
    """
    Mark attendance for current employee
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            frappe.throw(_("Please login to mark attendance"))
        
        # Check if user has Employee role
        user_roles = frappe.get_roles(user)
        if "Employee" not in user_roles:
            frappe.throw(_("Access denied. Employee role required."))
        
        # Get employee record
        employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not employee:
            frappe.throw(_("Employee record not found for this user"))
        
        # Use today's date if not provided
        if not attendance_date:
            attendance_date = today()
        
        # Check if attendance already exists for this date
        existing_attendance = frappe.db.exists("Attendance", {
            "employee": employee,
            "attendance_date": attendance_date,
            "docstatus": ["!=", 2]
        })
        
        if existing_attendance:
            frappe.throw(_("Attendance already marked for this date"))
        
        # Create attendance record
        attendance_doc = {
            "doctype": "Attendance",
            "employee": employee,
            "attendance_date": attendance_date,
            "status": status,
            "in_time": now_datetime() if status == "Present" else None
        }
        
        attendance = frappe.get_doc(attendance_doc)
        attendance.flags.ignore_permissions = True
        attendance.insert()
        attendance.submit()
        
        return {
            "success": True,
            "message": _("Attendance marked successfully"),
            "attendance_id": attendance.name
        }
        
    except Exception as e:
        frappe.log_error(f"Mark attendance error: {str(e)}")
        frappe.throw(str(e))

@frappe.whitelist()
def get_attendance_records(from_date=None, to_date=None):
    """
    Get attendance records for current employee
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            frappe.throw(_("Please login to view attendance"))
        
        # Check if user has Employee role
        user_roles = frappe.get_roles(user)
        if "Employee" not in user_roles:
            frappe.throw(_("Access denied. Employee role required."))
        
        # Get employee record
        employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not employee:
            frappe.throw(_("Employee record not found for this user"))
        
        # Set default date range if not provided
        if not from_date:
            from_date = frappe.utils.add_days(today(), -30)  # Last 30 days
        if not to_date:
            to_date = today()
        
        # Get attendance records
        attendance_records = frappe.get_all("Attendance", 
            filters={
                "employee": employee,
                "attendance_date": ["between", [from_date, to_date]],
                "docstatus": ["!=", 2]
            },
            fields=["name", "attendance_date", "status", "in_time", "out_time", "working_hours"],
            order_by="attendance_date desc"
        )
        
        return {
            "success": True,
            "attendance_records": attendance_records,
            "from_date": from_date,
            "to_date": to_date
        }
        
    except Exception as e:
        frappe.log_error(f"Get attendance records error: {str(e)}")
        frappe.throw(str(e))

@frappe.whitelist()
def get_salary_slips(from_date=None, to_date=None):
    """
    Get salary slips for current employee
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            frappe.throw(_("Please login to view salary slips"))
        
        # Check if user has Employee role
        user_roles = frappe.get_roles(user)
        if "Employee" not in user_roles:
            frappe.throw(_("Access denied. Employee role required."))
        
        # Get employee record
        employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not employee:
            frappe.throw(_("Employee record not found for this user"))
        
        # Set default date range if not provided (last 12 months)
        if not from_date:
            from_date = frappe.utils.add_months(today(), -12)
        if not to_date:
            to_date = today()
        
        # Get salary slips
        salary_slips = frappe.get_all("Salary Slip",
            filters={
                "employee": employee,
                "start_date": [">=", from_date],
                "end_date": ["<=", to_date],
                "docstatus": 1
            },
            fields=["name", "start_date", "end_date", "gross_pay", "total_deduction", "net_pay", "posting_date"],
            order_by="start_date desc"
        )
        
        return {
            "success": True,
            "salary_slips": salary_slips
        }
        
    except Exception as e:
        frappe.log_error(f"Get salary slips error: {str(e)}")
        frappe.throw(str(e))

@frappe.whitelist()
def apply_leave(leave_type, from_date, to_date, description, half_day=0, half_day_date=None):
    """
    Apply for leave
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            frappe.throw(_("Please login to apply for leave"))
        
        # Check if user has Employee role
        user_roles = frappe.get_roles(user)
        if "Employee" not in user_roles:
            frappe.throw(_("Access denied. Employee role required."))
        
        # Get employee record
        employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not employee:
            frappe.throw(_("Employee record not found for this user"))
        
        # Create leave application
        leave_app_doc = {
            "doctype": "Leave Application",
            "employee": employee,
            "leave_type": leave_type,
            "from_date": from_date,
            "to_date": to_date,
            "description": description,
            "half_day": int(half_day),
            "half_day_date": half_day_date if half_day else None,
            "status": "Open"
        }
        
        leave_app = frappe.get_doc(leave_app_doc)
        leave_app.flags.ignore_permissions = True
        leave_app.insert()
        
        return {
            "success": True,
            "message": _("Leave application submitted successfully"),
            "leave_application_id": leave_app.name
        }
        
    except Exception as e:
        frappe.log_error(f"Apply leave error: {str(e)}")
        frappe.throw(str(e))

@frappe.whitelist()
def get_leave_applications():
    """
    Get leave applications for current employee
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            frappe.throw(_("Please login to view leave applications"))
        
        # Check if user has Employee role
        user_roles = frappe.get_roles(user)
        if "Employee" not in user_roles:
            frappe.throw(_("Access denied. Employee role required."))
        
        # Get employee record
        employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not employee:
            frappe.throw(_("Employee record not found for this user"))
        
        # Get leave applications
        leave_applications = frappe.get_all("Leave Application",
            filters={"employee": employee},
            fields=["name", "leave_type", "from_date", "to_date", "total_leave_days", "description", "status", "posting_date"],
            order_by="posting_date desc"
        )
        
        return {
            "success": True,
            "leave_applications": leave_applications
        }
        
    except Exception as e:
        frappe.log_error(f"Get leave applications error: {str(e)}")
        frappe.throw(str(e))

@frappe.whitelist()
def get_leave_balance():
    """
    Get leave balance for current employee
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            frappe.throw(_("Please login to view leave balance"))
        
        # Check if user has Employee role
        user_roles = frappe.get_roles(user)
        if "Employee" not in user_roles:
            frappe.throw(_("Access denied. Employee role required."))
        
        # Get employee record
        employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not employee:
            frappe.throw(_("Employee record not found for this user"))
        
        # Get leave allocations
        leave_allocations = frappe.get_all("Leave Allocation",
            filters={
                "employee": employee,
                "docstatus": 1,
                "from_date": ["<=", today()],
                "to_date": [">=", today()]
            },
            fields=["leave_type", "new_leaves_allocated", "leaves_taken", "total_leaves_allocated"]
        )
        
        return {
            "success": True,
            "leave_balance": leave_allocations
        }
        
    except Exception as e:
        frappe.log_error(f"Get leave balance error: {str(e)}")
        frappe.throw(str(e))
