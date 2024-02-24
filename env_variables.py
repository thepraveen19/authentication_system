import os
from configparser import ConfigParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

# Path to your database configuration file
DATABASE_CONFIG_PATH = os.path.join(BASE_DIR, "config", "database.ini")

# Other paths, if needed...
