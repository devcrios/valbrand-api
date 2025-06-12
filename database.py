import os
import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


def get_database_url():
    """Construye la URL de la base de datos usando variables de entorno"""
    # Primero intenta usar DATABASE_URL directamente
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url
    
    # Si no existe, construye usando variables separadas
    host = os.getenv("MYSQLHOST")
    user = os.getenv("MYSQLUSER")
    password = os.getenv("MYSQLPASSWORD")
    database = os.getenv("MYSQLDATABASE")
    port = os.getenv("MYSQLPORT", "3306")
    
    if not all([host, user, password, database]):
        raise ValueError("Database environment variables are not set")
    
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

# Crear el engine usando la URL construida
engine = create_engine(get_database_url())

# Configurar la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

def get_db():
    """Función para obtener una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()