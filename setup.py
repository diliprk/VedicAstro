from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="vedicastro",
    version="0.1.5",
    author="Dilip Rajkumar",
    author_email="diliprajkumar@gmail.com",
    description="A python package for Vedic Astrology, with a particular focus on the Krishnamurthi Paddhati system",
    license="MIT",
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
    dependency_links=["git+https://github.com/flatangle/flatlib.git@sidereal#egg=flatlib"]
)

print("IMPORTANT NOTE: PyPI no longer supports specifying external packages in `install_requires`")
print("Packages specified in `dependency_links` will also not get automatically installed")
print("To install the required package 'flatlib' from the 'sidereal' branch, run the following command \
      after completion of `pip install vedicastro` process:")
print("pip install git+https://github.com/flatangle/flatlib.git@sidereal#egg=flatlib")
