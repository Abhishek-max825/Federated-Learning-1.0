# `app/templates/` — Jinja2 HTML Templates

All HTML templates rendered by Flask's `render_template()`. Uses **Bootstrap 5 dark mode** and **Toastify.js** for notifications.

## Structure

```
templates/
├── base.html               # Base layout: navbar, Bootstrap, Toastify, flash messages
├── index.html              # Home page — redirects based on role
├── auth/
│   ├── login.html          # Login form with animated design
│   └── register.html       # Registration form (Doctor / Hospital Node)
├── admin/
│   └── dashboard.html      # Admin panel: FL controls, user management, audit logs
├── doctor/
│   ├── dashboard.html      # Heart disease prediction form & results
│   └── report_pdf.html     # PDF report template for predictions
└── hospital/
    └── dashboard.html      # Local training: file upload + train button + analytics
```

## Template Inheritance

All pages extend `base.html` which provides:
- **Navbar** with role-based navigation (shows Dashboard link for the user's role)
- **User info** display (`username (role)`)
- **Flash messages** rendered as toast notifications
- Bootstrap 5 + Toastify.js script loading
