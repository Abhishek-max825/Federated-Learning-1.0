from app import create_app, db
from app.models import User, Role

app = create_app()

with app.app_context():
    users = User.query.all()
    print(f"{'Username':<15} {'Role':<15} {'Hospital ID'}")
    print("-" * 45)
    for u in users:
        role_name = u.role.name if u.role else 'None'
        print(f"{u.username:<15} {role_name:<15} {u.hospital_id}")
