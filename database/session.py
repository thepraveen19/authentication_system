from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from configparser import ConfigParser

# Directly access the path to the database configuration file
DATABASE_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "database.ini")
# Read database configuration from the ini file
config_parser = ConfigParser()
config_parser.read(DATABASE_CONFIG_PATH)

# Construct the DATABASE_URL using the configuration from database.ini
DATABASE_URL = (
    f"postgresql://{config_parser['postgresql']['user']}:{config_parser['postgresql']['password']}"
    f"@{config_parser['postgresql']['host']}:{config_parser['postgresql']['port']}"
    f"/{config_parser['postgresql']['database']}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


