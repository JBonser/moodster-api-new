from setuptools import setup

setup(
    name="moodster-api",
    version=0.1,
    packages=["app"],
    install_requires=[
        "python-dateutil",
        "dataclasses",
        "fastapi",
        "pkg-resources",
        "pydantic",
        "starlette",
        "SQLAlchemy",
        "alembic",
        "requests",
        "uvicorn",
        "bcrypt",
        "passlib[bscrypt]",
        "pytest",
        "pytest-cov",
        "python-multipart",
        "PyJWT",
    ],
)
