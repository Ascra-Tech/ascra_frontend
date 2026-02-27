# Employee Self Service (ESS) — Custom Frontend
## Requirements & Developer Guidelines

> **Stack Target:** Custom Frontend (React / Vue / Angular / Vanilla JS) → Frappe/ERPNext HRMS Backend
> **Version:** 1.0
> **Last Updated:** February 2026

---

## 1. Project Overview

This document outlines the requirements and development guidelines for building a custom Employee Self Service (ESS) frontend that integrates with **Frappe HRMS / ERPNext** as the backend. The frontend communicates entirely via the **Frappe REST API** and must respect ERPNext's permission model, workflow states, and DocType schema.

---

## 2. Architecture Overview

```
┌─────────────────────────────────┐
│        Custom ESS Frontend      │
│   (React / Vue / Angular etc.)  │
└────────────────┬────────────────┘
                 │ HTTPS REST API
┌────────────────▼────────────────┐
│       Frappe / ERPNext Backend  │
│   - REST API (/api/resource)    │
│   - Whitelisted Methods         │
│   - Role-based Permissions      │
│   - Workflow Engine             │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│         MariaDB Database        │
│   (DocType-based schema)        │
└─────────────────────────────────┘
```

### Key API Patterns

| Action | Endpoint |
|---|---|
| List records | `GET /api/resource/{DocType}` |
| Get single record | `GET /api/resource/{DocType}/{name}` |
| Create record | `POST /api/resource/{DocType}` |
| Update record | `PUT /api/resource/{DocType}/{name}` |
| Delete record | `DELETE /api/resource/{DocType}/{name}` |
| Custom method | `GET/POST /api/method/{dotted.path}` |
| File upload | `POST /api/method/upload_file` |
| Login | `POST /api/method/login` |
| Logout | `GET /api/method/logout` |
| Logged-in user | `GET /api/method/frappe.auth.get_logged_user` |

---

## 3. Authentication

### 3.1 Options

| Method | Use Case |
|---|---|
| **Session Cookie** | Browser-based SPA (recommended) |
| **API Key + Secret** | Server-to-server or mobile apps |
| **OAuth2** | Third-party integrations |

### 3.2 Session Login Flow

```http
POST /api/method/login
Content-Type: application/json

{ "usr": "employee@company.com", "pwd": "password" }
```

Store the session cookie and send it with every subsequent request.

### 3.3 API Key Authentication

```http
GET /api/resource/Employee
Authorization: token {api_key}:{api_secret}
```

### 3.4 Employee Resolution (Critical First Step)

After login, immediately resolve the logged-in user to their Employee record:

```js
// Step 1: Get logged-in user
GET /api/method/frappe.auth.get_logged_user

// Step 2: Resolve to Employee record
GET /api/method/frappe.client.get_value
  ?doctype=Employee
  &filters={"user_id":"user@company.com"}
  &fieldname=["name","employee_name","department","designation","image","company"]
```

**Store the `Employee.name` (e.g., `EMP-00123`) in global state — it is required for almost every subsequent API call.**

---

## 4. DocType Reference by Module

### Phase 1 — Core (Must Have)

#### 4.1 Employee Profile
- **Primary DocType:** `Employee`
- **Supporting:** `Employee Bank Account`

Key fields: `name`, `employee_name`, `user_id`, `department`, `designation`, `date_of_joining`, `image`, `cell_number`, `personal_email`, `company`, `holiday_list`

```js
GET /api/resource/Employee/EMP-00123
```

#### 4.2 Leave Management
- **Primary DocTypes:** `Leave Application`, `Leave Type`, `Leave Allocation`
- **Supporting:** `Holiday List`

**Get leave balance:**
```js
GET /api/method/hrms.hr.doctype.leave_application.leave_application.get_leave_details
  ?employee=EMP-00123&date=2024-01-01
```

**Submit leave application:**
```js
POST /api/resource/Leave Application
{
  "employee": "EMP-00123",
  "leave_type": "Casual Leave",
  "from_date": "2024-02-01",
  "to_date": "2024-02-02",
  "half_day": 0,
  "reason": "Personal work",
  "docstatus": 1
}
```

**docstatus values:** `0` = Draft, `1` = Submitted, `2` = Cancelled

#### 4.3 Attendance
- **Primary DocTypes:** `Attendance`, `Employee Checkin`
- **Supporting:** `Attendance Request`

**Get monthly attendance:**
```js
GET /api/resource/Attendance
  ?filters=[["employee","=","EMP-00123"],["attendance_date","between",["2024-01-01","2024-01-31"]]]
  &fields=["attendance_date","status","in_time","out_time","shift"]
```

**Mark check-in:**
```js
POST /api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field
{
  "employee_field_value": "EMP-00123",
  "log_type": "IN",
  "timestamp": "2024-01-15 09:00:00"
}
```

#### 4.4 Payslips
- **Primary DocType:** `Salary Slip`

```js
GET /api/resource/Salary Slip
  ?filters=[["employee","=","EMP-00123"]]
  &fields=["name","posting_date","net_pay","gross_pay","start_date","end_date"]
  &order_by=posting_date desc
```

#### 4.5 Expense Claims
- **Primary DocTypes:** `Expense Claim`, `Expense Claim Type`

```js
POST /api/resource/Expense Claim
{
  "employee": "EMP-00123",
  "expense_approver": "manager@company.com",
  "posting_date": "2024-01-15",
  "expenses": [{
    "expense_date": "2024-01-10",
    "expense_type": "Travel",
    "amount": 500,
    "description": "Client visit cab fare"
  }]
}
```

---

### Phase 2 — Should Have

| Feature | DocType |
|---|---|
| Attendance regularization | `Attendance Request` |
| Comp-off requests | `Compensatory Leave Request` |
| Shift view | `Shift Assignment` |
| Bank account update | `Employee Bank Account` |
| Travel request | `Travel Request` |
| Tax declaration | `Employee Tax Exemption Declaration` |
| Loan application | `Loan Application` |

---

### Phase 3 — Nice to Have

| Feature | DocType |
|---|---|
| Appraisal | `Appraisal`, `Appraisal Cycle` |
| Performance feedback | `Employee Performance Feedback` |
| Training | `Training Event`, `Training Result` |
| Grievances | `Employee Grievance` |
| Exit/offboarding | `Exit Interview`, `Employee Separation` |
| Leave encashment | `Leave Encashment` |

---

## 5. Permissions & Role Model

### 5.1 Required Roles

| Role | Who Gets It | Access Level |
|---|---|---|
| `Employee` | All employees | Own records only |
| `Leave Approver` | Team managers | Own team's leave applications |
| `HR Manager` | HR staff | All employee records |
| `HR User` | HR assistants | Limited HR access |

### 5.2 Rules

- The `Employee` role scopes all data to the logged-in user's own records automatically.
- Never expose HR Manager-level APIs to regular employees on the frontend.
- For manager features (team leave approval, attendance overview), check the user's role before rendering those UI sections:

```js
GET /api/method/frappe.client.get_value
  ?doctype=Has Role
  &filters={"parent":"user@company.com","role":"Leave Approver"}
```

### 5.3 Data Scoping Rule

Always pass `employee` as a filter in every API call — never rely solely on the backend to scope records. This is a defense-in-depth practice.

---

## 6. File Uploads

For expense claim receipts, profile photos, or document attachments:

```js
POST /api/method/upload_file
Content-Type: multipart/form-data

{
  file: <binary>,
  doctype: "Expense Claim",
  docname: "EXP-00123",
  is_private: 1
}
```

Response returns a `file_url` — store this and attach it to the parent document.

---

## 7. Workflow & Document States

ERPNext uses `docstatus` to control document lifecycle:

| docstatus | State | Meaning |
|---|---|---|
| `0` | Draft | Saved but not submitted |
| `1` | Submitted | Submitted, triggers workflow |
| `2` | Cancelled | Cancelled, no further edits |

For documents with **approval workflows** (Leave Application, Expense Claim):

- `status` field tracks approval: `Open`, `Approved`, `Rejected`
- Employee submits → Manager approves/rejects → Employee sees updated status
- **Poll or use webhooks** to reflect status changes in the frontend

---

## 8. Error Handling

All Frappe API errors follow this structure:

```json
{
  "exc_type": "ValidationError",
  "exception": "frappe.exceptions.ValidationError",
  "exc": "...",
  "_server_messages": "[{\"message\": \"Leave balance not sufficient\"}]"
}
```

### Recommended Handling

```js
async function apiCall(url, options) {
  const res = await fetch(url, options);
  const data = await res.json();

  if (!res.ok || data.exc) {
    const messages = JSON.parse(data._server_messages || "[]");
    const errorMsg = messages[0]?.message || "Something went wrong";
    throw new Error(errorMsg);
  }

  return data;
}
```

### Common Error Scenarios

| Error | Cause | Handling |
|---|---|---|
| `PermissionError` | User lacks access | Show "Not Authorized" message |
| `ValidationError` | Business rule violated | Show server message to user |
| `DoesNotExistError` | Record not found | Redirect or show 404 |
| `LinkValidationError` | Invalid linked value | Validate dropdowns from master data |

---

## 9. Frontend Development Guidelines

### 9.1 State Management

- Store `employee_id`, `employee_name`, `user_id`, `department`, `company` globally after login
- Cache master data (Leave Types, Expense Types, Departments) at app load — these rarely change
- Never hardcode DocType field values — always fetch from the API

### 9.2 API Call Best Practices

```js
// Always use field selection — never fetch all fields
GET /api/resource/Leave Application
  ?fields=["name","leave_type","from_date","to_date","status","total_leave_days"]
  &filters=[["employee","=","EMP-00123"]]
  &limit=20
  &order_by=from_date desc

// Use limit_start for pagination
  &limit_start=20&limit=20
```

### 9.3 Date Format

ERPNext uses `YYYY-MM-DD` for all dates. Always format dates before sending:

```js
const formatted = date.toISOString().split("T")[0]; // "2024-01-15"
```

### 9.4 Naming Convention

DocType record names (IDs) in ERPNext follow patterns like `EMP-00123`, `LEAVE-00456`, `SAL-SLIP-00789`. These are auto-generated — never assume or hardcode them.

### 9.5 Pagination

Default Frappe list API returns **20 records**. Always implement pagination:

```js
GET /api/resource/Attendance?limit=50&limit_start=0  // Page 1
GET /api/resource/Attendance?limit=50&limit_start=50 // Page 2
```

### 9.6 CORS Configuration

If your frontend is on a different domain, configure CORS in ERPNext:

`Site Settings → Allow CORS → add your frontend domain`

Or set in `site_config.json`:
```json
{ "allow_cors": "https://your-frontend-domain.com" }
```

---

## 10. Key Whitelisted API Methods

| Method | Purpose |
|---|---|
| `frappe.auth.get_logged_user` | Get current user |
| `frappe.client.get_value` | Get specific field values |
| `frappe.client.get_list` | Get filtered list |
| `frappe.client.set_value` | Update a single field |
| `hrms.hr.doctype.leave_application.leave_application.get_leave_details` | Leave balance |
| `hrms.hr.doctype.leave_application.leave_application.get_leave_balance_on` | Balance on date |
| `hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field` | Check-in/out |
| `frappe.desk.form.load.getdoc` | Full doc with metadata |

---

## 11. Build Priority Roadmap

```
Phase 1 (MVP — Weeks 1–4)
├── Auth & Employee Profile
├── Leave Application & Balance
├── Attendance View
└── Payslip View

Phase 2 (Weeks 5–8)
├── Expense Claims
├── Check-in / Check-out
├── Attendance Regularization
└── Bank Account Management

Phase 3 (Weeks 9–12)
├── Tax Declaration
├── Loan Application
├── Travel Request
└── Appraisal & Feedback
```

---

## 12. Security Checklist

- [ ] Never expose API Key/Secret in frontend JavaScript
- [ ] Always use HTTPS in production
- [ ] Validate all user inputs before sending to API
- [ ] Scope every query with `employee` filter
- [ ] Check user roles before rendering manager-level UI
- [ ] Use `is_private: 1` for all file uploads
- [ ] Implement session timeout handling
- [ ] Never cache sensitive data (payslips, salary) in localStorage

---

## 13. Useful ERPNext Resources

| Resource | URL |
|---|---|
| Frappe REST API Docs | `https://frappeframework.com/docs/user/en/api/rest` |
| HRMS GitHub | `https://github.com/frappe/hrms` |
| ERPNext Docs | `https://docs.erpnext.com` |
| Frappe Framework Docs | `https://frappeframework.com/docs` |

---

*This document should be treated as a living reference and updated as new modules are added to the ESS frontend.*
