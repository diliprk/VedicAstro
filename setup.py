from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="VedicAstro",
    version="0.1.2",
    author="Dilip Rajkumar",
    author_email="diliprajkumar@gmail.com",
    description="A python package for Vedic Astrology, with a particular focus on the Krishnamurthi Paddhati system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diliprk/VedicAstro",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=["polars","fastapi","uvicorn","prettytable","ipykernel"],
    dependency_links=["git+https://github.com/flatangle/flatlib.git#egg=flatlib-sidereal"]
)