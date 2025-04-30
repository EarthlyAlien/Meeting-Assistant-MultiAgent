from setuptools import find_packages, setup

setup(
    name="meeting-assistant",
    version="0.1.0",
    description="A multi-agent system for processing meeting recordings",
    author="Chaitanya K.K. Vankadaru",
    author_email="chaitanya.vankadaru@gmail.com",
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
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
)
