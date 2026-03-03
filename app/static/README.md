# `app/static/` — Static Assets

Contains static files served by Flask.

## Structure

```
static/
└── css/
    └── style.css    # Custom styles: dark theme overrides, gradient navbar, card styling
```

The main styling comes from **Bootstrap 5 dark mode** (loaded via CDN in `base.html`). The custom `style.css` provides:
- Dark-themed navbar with gradient accent
- Card styling for dashboard sections
- Custom form controls and button styles
- Responsive layout adjustments
