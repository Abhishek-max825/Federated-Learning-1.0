from app import create_app, db
from app.models import Role, User

app = create_app()

def seed_data():
    with app.app_context():
        # Create Roles
        roles = ['Admin', 'Doctor', 'Hospital Node']
        for r_name in roles:
            role = Role.query.filter_by(name=r_name).first()
            if role is None:
                role = Role(name=r_name)
                db.session.add(role)
        db.session.commit()
        print("Roles seeded.")

        # Create Admin User
        admin_role = Role.query.filter_by(name='Admin').first()
        admin = User.query.filter_by(username='admin').first()
        if admin is None:
            admin = User(username='admin', email='admin@example.com', role=admin_role)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user seeded.")
        else:
            print("Admin user already exists.")

        # Create Doctor User
        doctor_role = Role.query.filter_by(name='Doctor').first()
        doctor = User.query.filter_by(username='doctor').first()
        if doctor is None:
            doctor = User(username='doctor', email='doctor@example.com', role=doctor_role)
            doctor.set_password('doctor123')
            db.session.add(doctor)
            db.session.commit()
            print("Doctor user seeded.")
        else:
            print("Doctor user already exists.")

        # Create Hospital User
        hospital_role = Role.query.filter_by(name='Hospital Node').first()
        hospital = User.query.filter_by(username='hospital').first()
        if hospital is None:
            hospital = User(username='hospital', email='hospital@example.com', role=hospital_role)
            hospital.set_password('hospital123')
            db.session.add(hospital)
            db.session.commit()
            print("Hospital user seeded.")
        else:
            print("Hospital user already exists.")

if __name__ == '__main__':
    seed_data()
