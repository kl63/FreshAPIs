from setuptools import setup, find_packages

setup(
    name="freshly-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.6",
        "passlib>=1.7.4",
        "python-jose>=3.3.0",
        "python-multipart>=0.0.6",
        "email-validator>=2.0.0",
        "alembic>=1.11.1",
        "bcrypt>=4.0.1",
    ],
)
