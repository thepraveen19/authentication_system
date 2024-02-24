from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from env_variables import DATABASE_CONFIG_PATH
from configparser import ConfigParser

# Read database configuration from the ini file
config_parser = ConfigParser()
config_parser.read(DATABASE_CONFIG_PATH)

DATABASE_URL = (
    f"postgresql://{config_parser['postgresql']['user']}:{config_parser['postgresql']['password']}"
    f"@{config_parser['postgresql']['host']}:{config_parser['postgresql']['port']}"
    f"/{config_parser['postgresql']['database']}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
