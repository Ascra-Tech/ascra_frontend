# Ascra Frontend - Production Deployment Guide

## Overview
The Ascra Frontend app follows the same deployment pattern as Frappe HRMS, where the frontend Vue.js application is built and served as static assets within the Frappe app structure.

## Deployment Architecture

### Development vs Production
- **Development**: Frontend runs on `http://localhost:8080/frontend/` via Vite dev server
- **Production**: Frontend is built and served as static assets at `/assets/ascra_frontend/frontend/`

### File Structure
```
ascra_frontend/
├── frontend/                          # Vue.js source code
│   ├── src/                          # Vue components, pages, router
│   ├── package.json                  # Build scripts and dependencies
│   ├── vite.config.js               # Build configuration
│   └── ...
├── ascra_frontend/
│   ├── public/frontend/             # Built frontend assets (generated)
│   │   ├── assets/                  # JS, CSS, fonts
│   │   └── index.html              # Built HTML
│   ├── www/frontend.html           # Jinja template entry point
│   ├── hooks.py                    # Route rules and app config
│   └── api.py                      # Backend APIs
└── build_frontend.sh              # Production build script
```

## Production Build Process

### 1. Build Command
```bash
cd apps/ascra_frontend
./build_frontend.sh
```

Or manually:
```bash
cd frontend
yarn install
yarn build
```

### 2. Build Output
- **Static Assets**: `ascra_frontend/public/frontend/assets/`
- **Entry HTML**: `ascra_frontend/www/frontend.html` (copied from built index.html)
- **Base Path**: `/assets/ascra_frontend/frontend/` for all assets

### 3. Deployment Steps
```bash
# 1. Build the frontend
cd apps/ascra_frontend
./build_frontend.sh

# 2. Install/Update the app on your site
bench --site your-site.com install-app ascra_frontend
# OR for updates:
bench --site your-site.com migrate

# 3. Clear cache and restart
bench --site your-site.com clear-cache
bench restart
```

## Route Configuration

### Website Route Rules (hooks.py)
```python
website_route_rules = [
    {"from_route": "/frontend/<path:app_path>", "to_route": "frontend"},
]
```

### Access URLs
- **Production**: `https://your-site.com/frontend`
- **Development**: `http://localhost:8080/frontend/`

## Key Features Deployed

### 1. Advanced Contact Form
- Creates **Lead** and **Contact** records in ERPNext
- Comprehensive form fields (company info, location, industry)
- Integrated with ERPNext CRM module

### 2. Employee Dashboard (for Employee role users)
- **Attendance Management**: Mark daily attendance
- **Leave Applications**: Apply for and track leaves
- **Salary Slips**: View historical salary information
- **Leave Balance**: Check available leave days

### 3. Authentication System
- **Standard Frappe Login**: Uses `/api/method/login`
- **User Registration**: Creates Website Users with Guest role
- **Role Detection**: Automatically shows Employee Dashboard for Employee role users

### 4. Navigation Structure
- **Public Users**: Home page with Services, Portfolio, About, Contact sections
- **Logged-in Users**: Dashboard with personalized content
- **Employee Users**: Additional Employee Dashboard access

## Backend APIs Available

### Public APIs (Guest Access)
- `create_user_account()` - User registration
- `create_lead_and_contact()` - Contact form submission

### Authenticated APIs (Employee Role Required)
- `get_user_roles()` - Role detection
- `get_employee_info()` - Employee details
- `mark_attendance()` - Attendance marking
- `get_attendance_records()` - Attendance history
- `get_salary_slips()` - Salary slip access
- `apply_leave()` - Leave application
- `get_leave_applications()` - Leave history
- `get_leave_balance()` - Available leave days

## Production Considerations

### 1. Asset Serving
- All frontend assets served via Frappe's static file serving
- Proper caching headers applied by Frappe
- CDN-ready asset structure

### 2. Security
- CSRF token integration
- Role-based access control
- Frappe session management

### 3. Performance
- Code splitting with manual chunks
- Optimized bundle sizes
- Source maps for debugging

### 4. SEO & PWA
- Meta tags for social sharing
- PWA manifest support
- Proper HTML structure

## Troubleshooting

### Build Issues
```bash
# Clear node_modules and rebuild
cd frontend
rm -rf node_modules yarn.lock
yarn install
yarn build
```

### Cache Issues
```bash
bench --site your-site.com clear-cache
bench restart
```

### Permission Issues
- Ensure Employee role is assigned to users who need Employee Dashboard
- Check API permissions in `api.py`

## Comparison with HRMS
Your `ascra_frontend` now follows the exact same pattern as Frappe HRMS:
- ✅ Frontend builds to `public/frontend/` directory
- ✅ Website route rules for `/frontend/<path>`
- ✅ HTML template in `www/frontend.html`
- ✅ Base path configuration for assets
- ✅ Frappe context injection
- ✅ Production-ready build process

The app will deploy automatically with the Frappe app installation, just like HRMS does.
