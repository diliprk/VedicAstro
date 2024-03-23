<p align="center">
    <img src="https://raw.githubusercontent.com/diliprk/VedicAstro/main/VedicAstroLogo.png?raw=True" alt="Logo">
    <p align="center">
    <img src="https://img.shields.io/pypi/v/VedicAstro" alt="PyPi Latest Release"> <img src="https://img.shields.io/badge/python-3.11-limegreen" alt="Python Version"> <img src="https://img.shields.io/badge/License-MIT-blue" alt="License">
    </p> 
</p>

<b>`VedicAstro`</b> is a python library built for the study, practise, research and application of traditional Vedic Astrology. The goal of this package is to generate chart and planetary position data for Vedic Astrology systems , particularly `Krishnamurthi Paddhati` (KP) system. This package, primarily uses the `sidereal` branch of the [flatlib](https://github.com/flatangle/flatlib/tree/sidereal) library to obtain data from the swiss ephemeris (`pyswisseph`)

## Installation
Create a virtual environment in this project directory and install the required packages:

### From `PyPi`
```bash
pip install vedicastro
```
**NOTE**: `PyPI` no longer supports specifying external packages (eg:git repo URLs) in `install_requires` in the `setup.py` file. ([Read this](https://github.com/pypi/warehouse/issues/9404)) Packages specified in `dependency_links` will also not get automatically installed([Read this](https://setuptools.pypa.io/en/latest/deprecated/dependency_links.html)). To install the required package `flatlib` from the `sidereal` branch, run the following command, after completion of above `pip install VedicAstro` command:
```bash
pip install git+https://github.com/flatangle/flatlib.git@sidereal#egg=flatlib
```

### From local clone of Git Repo
Clone the repo: 
```bash
https://github.com/diliprk/VedicAstro.git
```

Create a python virtual environment using `venv`
```bash
python -m venv astrovenv
source astrovenv/bin/activate
pip install --upgrade  pip
pip install -r requirements.txt
```
In `Windows`: `source astrovenv/bin/activate` does not work, so you have to do `cd astrovenv\Scripts && activate` in command prompt, 

Alternatively, you can also use `miniconda` as your virtual environment manager:

```bash
conda create -n astrovenv python=3.11
conda activate astrovenv
pip install -r requirements.txt
```

## Study and Reference
The main class in this package is the `VedicHoroscopeData` class, which has the following methods:

 1. `generate_chart` - Generates a `flatlib.Chart` object for the given time and location data
 2. `get_planets_data_from_chart` - Generate the planets data table from a `flatlib.Chart` object
 3. `get_houses_data_from_chart` -  Generates the houses data table from a `flatlib.Chart` object
 4. `get_planet_wise_significators` - Generate the ABCD significators table for each planet
 5. `get_house_wise_significators` - Generate the ABCD significators table for each house
 6. `compute_vimshottari_dasa` - Computes the Vimshottari Dasa for the chart
 7. `get_planetary_aspects` - Computes aspects (like `Trine`, `Sextile` , `Square` , `Conjunction` etc.) between planets. This method is more popular in Western Astrology systems

You can run the  below notebook, to get a handle of the above basic operations.<br>[![ipynb file](https://img.shields.io/badge/VedicAstroStudy-notebook-brightgreen?logo=jupyter)](https://github.com/diliprk/VedicAstro/blob/main/VedicAstroStudy.ipynb)

### Horary (Prasna)
A seperate functionality has been added for computing KP Horary (`Prasna`) Chart, as it requires a completely different set of datetime objects for the ascendant computation.
You can invoke these functions `get_horary_ascendant_degree` and `find_exact_ascendant_time` in the `horary_chart.py` for preparing chart and tables for a KP Horary Question

## API Development
You can deploy this `VedicAstro` package using `FastAPI` on your local machine or remote server. Just run the below command from this directory where you have this `VedicAstroAPI.py` file

```bash
uvicorn VedicAstroAPI:app --reload --port 8088
```

Thereafter, you can test the API service at `http://127.0.0.1:8088/docs` in your browser

## Front-End Companion Project
If you are looking a front end project to visualize the results of the `VedicAstroAPI` call, please check out https://github.com/diliprk/AstroVue

## Dedicatations
This package is a dedication to the following great personalities, following in their footsteps:
- [Parasara MahaRishi](https://en.wikipedia.org/wiki/Parashara)
- [K.S. Krishnamurti](http://kpastrologys.net/about-us/)
- numerous great souls and teachers, who have shared this divine knowledge for free


## Glossary
| Term             | Definition                                                                                            |
|------------------|-------------------------------------------------------------------------------------------------------|
| Rasi             | Means one of the 12 signs of the zodiac, where each sign spans 30°, in the 360° sky                   |
| Nakshatra        | Lunar mansion which typically spans 13.32° (or about 800` degree-mins).                               |
| SubLord          | One of the 249 subdivisions of the KP Astrology system.                                               |
| SubSubLord       | Further divisions of the sublord.                                                                     |
| Vimshottari Dasha| [Vimshottari Dasha](https://en.wikipedia.org/wiki/Dasha_(astrology)) - A system of planetary periods. |


## Contributions
This project is always on the lookout for aspiring students of astrology with programming skills to take this open source contribution further.
