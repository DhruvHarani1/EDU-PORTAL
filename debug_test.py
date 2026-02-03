
import traceback
import sys
import os

sys.path.append(os.getcwd())

try:
    from tests.test_view_consistency import app, test_attendance_view_consistency, db

    print("Running test wrapper...")
    with app.test_client() as c:
        with app.app_context():
            db.create_all()
            try:
                test_attendance_view_consistency(c)
            finally:
                # db.drop_all() 
                pass

except Exception:
    with open("traceback.log", "w") as f:
        traceback.print_exc(file=f)
    print("Exception captured to traceback.log")
