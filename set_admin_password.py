import sys
from models.database import Database

if len(sys.argv) != 2:
    print('Usage: python set_admin_password.py <new_password>')
    sys.exit(1)

new_password = sys.argv[1]
db = Database()
db.init_admin(new_password)
print('Admin password updated successfully.')
