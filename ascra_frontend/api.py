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
            return {
                "success": False,
                "message": "Please enter a valid email address"
            }
        
        # Check if user already exists
        if frappe.db.exists("User", email):
            return {
                "success": False,
                "message": "User with this email already exists"
            }
        
        # Validate names
        if not first_name or not last_name:
            return {
                "success": False,
                "message": "First name and last name are required"
            }
        
        # Validate password
        if not password or len(password.strip()) < 8:
            return {
                "success": False,
                "message": "Password must be at least 8 characters long"
            }
        
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
        return {
            "success": False,
            "message": "User with this email already exists"
        }
    except frappe.ValidationError as e:
        print(f"User validation error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }
    except Exception as e:
        print(f"User creation error: {str(e)}")
        return {
            "success": False,
            "message": f"An error occurred while creating your account: {str(e)}"
        }

@frappe.whitelist(allow_guest=True)
def login_user(email, password):
    """
    Custom login API for Website Users
    """
    try:
        # Validate input
        if not email or not password:
            return {
                "success": False,
                "message": "Email and password are required"
            }
        
        # Validate email format
        if not validate_email_address(email):
            return {
                "success": False,
                "message": "Please enter a valid email address"
            }
        
        # Check if user exists
        if not frappe.db.exists("User", email):
            return {
                "success": False,
                "message": "Invalid email or password"
            }
        
        # Get user document
        user = frappe.get_doc("User", email)
        
        # Check if user is enabled
        if not user.enabled:
            return {
                "success": False,
                "message": "Your account has been disabled. Please contact administrator."
            }
        
        # Verify password
        from frappe.utils.password import check_password
        try:
            check_password(email, password)
        except frappe.AuthenticationError:
            return {
                "success": False,
                "message": "Invalid email or password"
            }
        
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
        print(f"Login error: {str(e)}")
        if isinstance(e, frappe.AuthenticationError):
            return {
                "success": False,
                "message": "Invalid email or password"
            }
        else:
            return {
                "success": False,
                "message": str(e)
            }

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
        # Debug: Log received data
        print(f"Received data type: {type(data)}")
        print(f"Received data: {data}")
        
        # Parse data if it's a string
        if isinstance(data, str):
            data = json.loads(data)
        
        print(f"Parsed data: {data}")
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'company_name', 'message']
        for field in required_fields:
            if not data.get(field):
                return {
                    "success": False,
                    "message": f"{field.replace('_', ' ').title()} is required"
                }
        
        # Validate email
        if not validate_email_address(data['email']):
            return {
                "success": False,
                "message": "Please enter a valid email address"
            }
        
        # Create Lead - only include simple fields to avoid Link field validation errors
        lead_doc = {
            "doctype": "Lead",
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email_id": data['email'],
            "mobile_no": data['phone'],
            "company_name": data['company_name'],
            "status": "Lead",
            "request_type": data.get('request_type', 'Product Enquiry'),
            "job_title": data.get('job_title'),
            "website": data.get('website'),
            "city": data.get('city'),
            "state": data.get('state'),
            "no_of_employees": data.get('no_of_employees'),
            "territory": "All Territories",
            "company": frappe.defaults.get_user_default("Company") or frappe.db.get_single_value("Global Defaults", "default_company")
        }
        
        # Try to add source if "Website" Lead Source exists
        if frappe.db.exists("Lead Source", "Website"):
            lead_doc['source'] = "Website"
        
        # Add country only if it's provided (Link field)
        if data.get('country'):
            lead_doc['country'] = data['country']
        
        # Add annual revenue only if provided
        if data.get('annual_revenue'):
            lead_doc['annual_revenue'] = data['annual_revenue']
        
        lead = frappe.get_doc(lead_doc)
        lead.flags.ignore_permissions = True
        lead.insert()
        
        print(f"Lead created successfully: {lead.name}")
        frappe.log_error(f"Lead created: {lead.name} for {data['email']}", "Contact Form - Lead Created")
        
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
        
        print(f"Contact created successfully: {contact.name}")
        
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
        
        print(f"Lead and Contact creation completed successfully")
        
        return {
            "success": True,
            "message": _("Thank you for your inquiry! We will get back to you soon."),
            "lead_id": lead.name,
            "contact_id": contact.name
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        frappe.log_error(f"Lead/Contact creation error: {error_details}", "Contact Form Submission Error")
        print(f"Lead/Contact creation error: {str(e)}")
        print(f"Full traceback: {error_details}")
        return {
            "success": False,
            "message": f"An error occurred while processing your request: {str(e)}"
        }

@frappe.whitelist()
def get_company_info():
    """
    Get company information including logo for frontend display
    """
    try:
        # Get user's default company or system default
        user_company = frappe.defaults.get_user_default("Company")
        if not user_company:
            user_company = frappe.db.get_single_value("Global Defaults", "default_company")
        
        if not user_company:
            # Get the first available company if no defaults are set
            companies = frappe.get_all("Company", limit=1, pluck="name")
            if companies:
                user_company = companies[0]
            else:
                return {
                    "success": False,
                    "message": "No company found in the system"
                }
        
        # Get comprehensive company information
        company_data = frappe.db.get_value("Company", user_company, [
            "name", "company_name", "abbr", "company_logo", "domain", 
            "country", "phone_no", "email", "website", "company_description"
        ], as_dict=True)
        
        if not company_data:
            return {
                "success": False,
                "message": f"Company '{user_company}' not found"
            }
        
        return {
            "success": True,
            "company": {
                "name": company_data.name,
                "company_name": company_data.company_name,
                "abbr": company_data.abbr,
                "logo": company_data.company_logo,
                "domain": company_data.domain,
                "country": company_data.country,
                "phone_no": company_data.phone_no,
                "email": company_data.email,
                "website": company_data.website,
                "description": company_data.company_description
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Get company info error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }

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
        
        # Get comprehensive employee record from database
        employee_data = frappe.db.get_value("Employee", {"user_id": user}, [
            "name", "employee_name", "first_name", "middle_name", "last_name", 
            "designation", "department", "company", "branch", "employee_number", 
            "date_of_joining", "date_of_birth", "status", "image", "gender",
            "cell_number", "personal_email", "company_email", "current_address",
            "permanent_address", "emergency_phone_number", "person_to_be_contacted",
            "relation", "marital_status", "blood_group", "reports_to", "salary_mode",
            "ctc", "salary_currency", "contract_end_date", "notice_number_of_days",
            "date_of_retirement", "holiday_list", "attendance_device_id"
        ], as_dict=True)
        
        if not employee_data:
            frappe.throw(_("Employee record not found for this user"))
        
        # If employee_number is None, use the employee name (HR-EMP-00001) as fallback
        employee_id = employee_data.employee_number or employee_data.name
        
        # Get reporting manager name if exists
        reports_to_name = None
        if employee_data.reports_to:
            reports_to_name = frappe.db.get_value("Employee", employee_data.reports_to, "employee_name")
        
        return {
            "success": True,
            "employee": {
                "name": employee_data.name,
                "employee_name": employee_data.employee_name,
                "first_name": employee_data.first_name,
                "middle_name": employee_data.middle_name,
                "last_name": employee_data.last_name,
                "designation": employee_data.designation or "Employee",
                "department": employee_data.department or "General",
                "company": employee_data.company,
                "branch": employee_data.branch,
                "employee_number": employee_id,
                "date_of_joining": employee_data.date_of_joining,
                "date_of_birth": employee_data.date_of_birth,
                "status": employee_data.status,
                "gender": employee_data.gender,
                "image": employee_data.image,
                "cell_number": employee_data.cell_number,
                "personal_email": employee_data.personal_email,
                "company_email": employee_data.company_email,
                "current_address": employee_data.current_address,
                "permanent_address": employee_data.permanent_address,
                "emergency_phone_number": employee_data.emergency_phone_number,
                "person_to_be_contacted": employee_data.person_to_be_contacted,
                "relation": employee_data.relation,
                "marital_status": employee_data.marital_status,
                "blood_group": employee_data.blood_group,
                "reports_to": employee_data.reports_to,
                "reports_to_name": reports_to_name,
                "salary_mode": employee_data.salary_mode,
                "ctc": employee_data.ctc,
                "salary_currency": employee_data.salary_currency,
                "contract_end_date": employee_data.contract_end_date,
                "notice_number_of_days": employee_data.notice_number_of_days,
                "date_of_retirement": employee_data.date_of_retirement,
                "holiday_list": employee_data.holiday_list,
                "attendance_device_id": employee_data.attendance_device_id
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Get employee info error: {str(e)}")
        frappe.throw(str(e))

@frappe.whitelist()
def mark_attendance(status="Present", attendance_date=None, in_time=None, out_time=None):
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
        
        # Get employee record with company information
        employee_data = frappe.db.get_value("Employee", {"user_id": user}, ["name", "company"], as_dict=True)
        if not employee_data:
            frappe.throw(_("Employee record not found for this user"))
        
        employee = employee_data.name
        company = employee_data.company
        
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
            # Get the existing attendance details
            existing_record = frappe.get_doc("Attendance", existing_attendance)
            return {
                "success": False,
                "message": _("Attendance already marked for {0} as {1}").format(
                    frappe.utils.formatdate(attendance_date), 
                    existing_record.status
                ),
                "attendance_id": existing_attendance,
                "already_exists": True
            }
        
        # Create attendance record with required fields
        attendance_doc = {
            "doctype": "Attendance",
            "employee": employee,
            "attendance_date": attendance_date,
            "company": company,
            "status": status
        }
        
        # Add time fields if provided
        if in_time:
            attendance_doc["in_time"] = in_time
        elif status == "Present":
            attendance_doc["in_time"] = now_datetime()
            
        if out_time:
            attendance_doc["out_time"] = out_time
        
        attendance = frappe.get_doc(attendance_doc)
        attendance.flags.ignore_permissions = True
        attendance.flags.ignore_mandatory = True
        
        # Insert the attendance record
        attendance.insert()
        
        # Submit the attendance record
        attendance.submit()
        
        return {
            "success": True,
            "message": _("Attendance marked successfully"),
            "attendance_id": attendance.name
        }
        
    except frappe.DuplicateEntryError:
        frappe.throw(_("Attendance already exists for this date"))
    except frappe.ValidationError as ve:
        frappe.log_error(f"Attendance validation error: {str(ve)}")
        frappe.throw(_("Validation error: {0}").format(str(ve)))
    except Exception as e:
        frappe.log_error(f"Mark attendance error: {str(e)}")
        frappe.throw(_("Failed to mark attendance: {0}").format(str(e)))

@frappe.whitelist()
def get_attendance_records(from_date=None, to_date=None):
    """
    Get attendance records for current employee
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            return {
                "success": False,
                "message": "Please login to view attendance",
                "attendance_records": []
            }
        
        # Check if user has Employee role
        user_roles = frappe.get_roles(user)
        if "Employee" not in user_roles:
            return {
                "success": False,
                "message": "Access denied. Employee role required.",
                "attendance_records": []
            }
        
        # Get employee record
        employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not employee:
            return {
                "success": False,
                "message": "Employee record not found for this user",
                "attendance_records": []
            }
        
        # Build filters for attendance records
        filters = {"employee": employee}
        
        # Only add date filtering if dates are provided
        if from_date and to_date:
            filters["attendance_date"] = ["between", [from_date, to_date]]
        elif from_date:
            filters["attendance_date"] = [">=", from_date]
        elif to_date:
            filters["attendance_date"] = ["<=", to_date]
        
        # Get attendance records with a reasonable limit to prevent data overflow
        attendance_records = frappe.get_all("Attendance", 
            filters=filters,
            fields=["name", "attendance_date", "status", "in_time", "out_time", "working_hours", "docstatus"],
            order_by="attendance_date desc",
            limit=100  # Limit to prevent CharacterLengthExceededError
        )
        
        # Add docstatus labels for frontend display
        for record in attendance_records:
            if record.docstatus == 0:
                record.docstatus_label = "Draft"
            elif record.docstatus == 1:
                record.docstatus_label = "Submitted"
            elif record.docstatus == 2:
                record.docstatus_label = "Cancelled"
        
        # Debug logging (simplified to avoid character length errors)
        print(f"Attendance API Debug - Employee: {employee}, Records found: {len(attendance_records)}")
        
        return {
            "success": True,
            "attendance_records": attendance_records,
            "from_date": from_date,
            "to_date": to_date,
            "debug_info": {
                "employee": employee,
                "total_records": len(attendance_records),
                "date_range": f"{from_date} to {to_date}"
            }
        }
        
    except Exception as e:
        print(f"Get attendance records error: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to load attendance records: {str(e)}",
            "attendance_records": []
        }

@frappe.whitelist()
def get_salary_slips(from_date=None, to_date=None):
    """
    Get salary slips for current employee
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            return {
                "success": False,
                "message": "Please login to view salary slips",
                "salary_slips": []
            }
        
        # Check if user has Employee role
        user_roles = frappe.get_roles(user)
        if "Employee" not in user_roles:
            return {
                "success": False,
                "message": "Access denied. Employee role required.",
                "salary_slips": []
            }
        
        # Get employee record
        employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not employee:
            return {
                "success": False,
                "message": "Employee record not found for this user",
                "salary_slips": []
            }
        
        # Build filters for salary slips
        filters = {"employee": employee}
        
        # Only add date filtering if dates are provided
        if from_date and to_date:
            filters["start_date"] = [">=", from_date]
            filters["end_date"] = ["<=", to_date]
        elif from_date:
            filters["start_date"] = [">=", from_date]
        elif to_date:
            filters["end_date"] = ["<=", to_date]
        
        # Get salary slips with a reasonable limit to prevent data overflow
        salary_slips = frappe.get_all("Salary Slip",
            filters=filters,
            fields=["name", "start_date", "end_date", "gross_pay", "total_deduction", "net_pay", "posting_date", "status", "docstatus"],
            order_by="start_date desc",
            limit=50  # Limit to prevent CharacterLengthExceededError
        )
        
        # Add docstatus labels for frontend display
        for record in salary_slips:
            if record.docstatus == 0:
                record.docstatus_label = "Draft"
            elif record.docstatus == 1:
                record.docstatus_label = "Submitted"
            elif record.docstatus == 2:
                record.docstatus_label = "Cancelled"
        
        return {
            "success": True,
            "salary_slips": salary_slips
        }
        
    except Exception as e:
        frappe.log_error(f"Get salary slips error: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to load salary slips: {str(e)}",
            "salary_slips": []
        }


@frappe.whitelist()
def download_salary_slip_pdf(salary_slip_name, print_format="Salary Slip Standard"):
    """
    Download salary slip as PDF with specified print format
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            frappe.throw(_("Please login to download salary slip"))
        
        # Get employee record
        employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not employee:
            frappe.throw(_("No employee record found for current user"))
        
        # Verify the salary slip belongs to the current employee
        salary_slip = frappe.get_doc("Salary Slip", salary_slip_name)
        if salary_slip.employee != employee:
            frappe.throw(_("You can only download your own salary slips"))
        
        # Validate print format exists and is for Salary Slip
        valid_formats = ["Salary Slip Standard", "Salary Slip with Year to Date", "Salary Slip based on Timesheet"]
        if print_format not in valid_formats:
            print_format = "Salary Slip Standard"  # Default fallback
        
        # Generate PDF using Frappe's built-in PDF generation
        from frappe.utils.pdf import get_pdf
        
        # Get the print format HTML
        html = frappe.get_print("Salary Slip", salary_slip_name, print_format=print_format)
        
        # Generate PDF
        pdf = get_pdf(html)
        
        # Set response headers for download
        frappe.local.response.filename = f"salary_slip_{salary_slip_name}_{print_format.replace(' ', '_')}.pdf"
        frappe.local.response.filecontent = pdf
        frappe.local.response.type = "download"
        
        return {
            "success": True,
            "message": "PDF generated successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Download salary slip PDF error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }

@frappe.whitelist()
def get_salary_slip_html(salary_slip_name, print_format="Salary Slip Standard"):
    """
    Get salary slip HTML for preview with specified print format
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            frappe.throw(_("Please login to view salary slip"))
        
        # Get employee record
        employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not employee:
            frappe.throw(_("No employee record found for current user"))
        
        # Verify the salary slip belongs to the current employee
        salary_slip = frappe.get_doc("Salary Slip", salary_slip_name)
        if salary_slip.employee != employee:
            frappe.throw(_("You can only view your own salary slips"))
        
        # Validate print format exists and is for Salary Slip
        valid_formats = ["Salary Slip Standard", "Salary Slip with Year to Date", "Salary Slip based on Timesheet"]
        if print_format not in valid_formats:
            print_format = "Salary Slip Standard"  # Default fallback
        
        # Get the print format HTML
        html = frappe.get_print("Salary Slip", salary_slip_name, print_format=print_format)
        
        return {
            "success": True,
            "html": html,
            "print_format": print_format
        }
        
    except Exception as e:
        frappe.log_error(f"Get salary slip HTML error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }

@frappe.whitelist()
def get_salary_slip_print_formats():
    """
    Get available print formats for salary slips
    """
    try:
        # Return the available salary slip print formats
        formats = [
            {"name": "Salary Slip Standard", "label": "Standard Format"},
            {"name": "Salary Slip with Year to Date", "label": "With Year to Date"},
            {"name": "Salary Slip based on Timesheet", "label": "Based on Timesheet"}
        ]
        
        return {
            "success": True,
            "print_formats": formats
        }
        
    except Exception as e:
        frappe.log_error(f"Get salary slip print formats error: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }

@frappe.whitelist()
def apply_leave(leave_type, from_date, to_date, description="", half_day=0, half_day_date=None):
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
        
        # Get employee record with company information
        employee_data = frappe.db.get_value("Employee", {"user_id": user}, ["name", "company"], as_dict=True)
        if not employee_data:
            frappe.throw(_("Employee record not found for this user"))
        
        employee = employee_data.name
        company = employee_data.company
        
        # Validate required fields
        if not leave_type:
            frappe.throw(_("Leave Type is required"))
        if not from_date:
            frappe.throw(_("From Date is required"))
        if not to_date:
            frappe.throw(_("To Date is required"))
        
        # Get employee name for leave application
        employee_name = frappe.db.get_value("Employee", employee, "employee_name")
        
        # Create leave application with all required fields
        leave_app_doc = {
            "doctype": "Leave Application",
            "employee": employee,
            "employee_name": employee_name,
            "leave_type": leave_type,
            "from_date": from_date,
            "to_date": to_date,
            "description": description or "",
            "company": company,
            "half_day": int(half_day) if half_day else 0,
            "half_day_date": half_day_date if half_day else None,
            "status": "Open",
            "posting_date": today(),
            "leave_approver": frappe.db.get_value("Employee", employee, "leave_approver")
        }
        
        # Remove None values
        leave_app_doc = {k: v for k, v in leave_app_doc.items() if v is not None}
        
        leave_app = frappe.get_doc(leave_app_doc)
        leave_app.flags.ignore_permissions = True
        leave_app.insert()
        
        return {
            "success": True,
            "message": _("Leave application submitted successfully"),
            "leave_application_id": leave_app.name
        }
        
    except frappe.ValidationError as ve:
        error_msg = str(ve)
        frappe.log_error(f"Leave application validation error: {error_msg}")
        return {
            "success": False,
            "message": f"Validation error: {error_msg}"
        }
    except Exception as e:
        error_msg = str(e)
        frappe.log_error(f"Apply leave error: {error_msg}")
        return {
            "success": False,
            "message": f"Failed to submit leave application: {error_msg}"
        }

@frappe.whitelist()
def get_leave_applications(from_date=None, to_date=None):
    """
    Get leave applications for current employee with optional date filtering
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            return {
                "success": False,
                "message": "Please login to view leave applications",
                "leave_applications": []
            }
        
        # Check if user has Employee role
        user_roles = frappe.get_roles(user)
        if "Employee" not in user_roles:
            return {
                "success": False,
                "message": "Access denied. Employee role required.",
                "leave_applications": []
            }
        
        # Get employee record
        employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
        if not employee:
            return {
                "success": False,
                "message": "Employee record not found for this user",
                "leave_applications": []
            }
        
        # Build filters for leave applications
        filters = {"employee": employee}
        
        # Only add date filtering if dates are provided
        if from_date and to_date:
            filters["from_date"] = [">=", from_date]
            filters["to_date"] = ["<=", to_date]
        elif from_date:
            filters["from_date"] = [">=", from_date]
        elif to_date:
            filters["to_date"] = ["<=", to_date]
        
        # Get leave applications with a reasonable limit to prevent data overflow
        leave_applications = frappe.get_all("Leave Application",
            filters=filters,
            fields=["name", "leave_type", "from_date", "to_date", "total_leave_days", "description", "status", "posting_date"],
            order_by="posting_date desc",
            limit=50  # Limit to prevent CharacterLengthExceededError
        )
        
        return {
            "success": True,
            "leave_applications": leave_applications
        }
        
    except Exception as e:
        frappe.log_error(f"Get leave applications error: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to load leave applications: {str(e)}",
            "leave_applications": []
        }

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
            fields=["leave_type", "new_leaves_allocated", "total_leaves_allocated"]
        )
        
        # Calculate leaves taken for each leave type
        leave_balance = []
        for allocation in leave_allocations:
            # Get approved leave applications for this leave type
            leaves_taken = frappe.db.sql("""
                SELECT COALESCE(SUM(total_leave_days), 0) as leaves_taken
                FROM `tabLeave Application`
                WHERE employee = %s 
                AND leave_type = %s 
                AND status = 'Approved'
                AND docstatus = 1
                AND from_date >= %s
                AND to_date <= %s
            """, (employee, allocation.leave_type, 
                  frappe.db.get_value("Leave Allocation", {"employee": employee, "leave_type": allocation.leave_type, "docstatus": 1}, "from_date"),
                  frappe.db.get_value("Leave Allocation", {"employee": employee, "leave_type": allocation.leave_type, "docstatus": 1}, "to_date")
                  ))[0][0] or 0
            
            leave_balance.append({
                "leave_type": allocation.leave_type,
                "total_leaves_allocated": allocation.total_leaves_allocated,
                "leaves_taken": leaves_taken,
                "leaves_remaining": allocation.total_leaves_allocated - leaves_taken
            })
        
        return {
            "success": True,
            "leave_balance": leave_balance
        }
        
    except Exception as e:
        print(f"Get leave balance error: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to load leave balance: {str(e)}",
            "leave_balance": []
        }

@frappe.whitelist()
def get_leave_types():
    """
    Get available leave types from the system
    """
    try:
        user = frappe.session.user
        if user == "Guest":
            return {
                "success": False,
                "message": "Please login to view leave types",
                "leave_types": []
            }
        
        # Check if user has Employee role
        user_roles = frappe.get_roles(user)
        if "Employee" not in user_roles:
            return {
                "success": False,
                "message": "Access denied. Employee role required.",
                "leave_types": []
            }
        
        # Get employee record to check company
        employee_data = frappe.db.get_value("Employee", {"user_id": user}, ["name", "company"], as_dict=True)
        if not employee_data:
            return {
                "success": False,
                "message": "Employee record not found for this user",
                "leave_types": []
            }
        
        # Get all leave types (no is_active field exists in Leave Type doctype)
        leave_types = frappe.get_all("Leave Type",
            fields=["name", "leave_type_name", "max_leaves_allowed", "is_carry_forward", "is_lwp", "include_holiday"],
            order_by="leave_type_name asc"
        )
        
        return {
            "success": True,
            "leave_types": leave_types
        }
        
    except Exception as e:
        print(f"Get leave types error: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to load leave types: {str(e)}",
            "leave_types": []
        }
