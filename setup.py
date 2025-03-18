from setuptools import setup, find_packages

setup(
    name="meeting-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-multipart",
        "jinja2",
        "pytest",
        "python-dotenv",
        "aiofiles",
    ],
) 