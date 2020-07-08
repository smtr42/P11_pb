<h1 align="center">
  [WIP] Project 8 - Pur Beurre
</h1>

<p align="center">
  <a href="">
    <img src="https://upload.wikimedia.org/wikipedia/fr/0/0d/Logo_OpenClassrooms.png" alt="Logo" width="100" height="100">
  </a>
</p>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.7-green.svg">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg">
  </a>
  <a href="https://www.linkedin.com/in/teiva-s/">
    <img src="https://img.shields.io/badge/linkedin-Simonnet-blue.svg">
  </a>
</p>



  <h3 align="center">Replace unhealthy food by better ones</h3>

 <p align="center">
    A Openclassrooms practical case where you use OpenFoodFacts to find alternatives to lesser nutritious food.
    <br />
  </p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [Functionality](#functionality)
- [Getting Started](#getting-started)
  - [Live version](#live-version)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Tests](#tests)
    - [Requirements](#requirements)
- [Author](#author)

<!-- ABOUT THE PROJECT -->
## About The Project

<p align="center">
  <a href="https://fr.openfoodfacts.org/">
    <img src="https://static.openfoodfacts.org/images/misc/openfoodfacts-logo-fr-178x150.png">
  </a>
</p>

OpenFoodFacts is a database fed by volunteers in order to map the food and its ingredients. It's available under the Open Database License.

The goal is to create an application so the user can find an healthier alternative to a specific food using OpenFoodFacts.

This project is the 8th assignment for the Python developer diploma from OpenClassrooms.
The goal is to learn about:
* Django,
* Deployement,
* Agile development,
* Common good practices.


### Functionality

* Ability to find a reference in a clone of the OpenFoodFacts Database
* The user can create and connect to his personnal account
* The user ask for a product in the search bar and get a substitute he can save
 
<!-- GETTING STARTED -->
## Getting Started

### Live version
The website is hosted on heroku  [on this link](http://smtr42p8.herokuapp.com/) `http://smtr42p8.herokuapp.com/`

### Installation
I used Python 3.7.7

*  Clone the repo
```bash
$ git clone https://github.com/smtr42/p8_purb
```
*  Install required dependencies
```bash
$ pip install -r requirements.txt
```
*  Create database
```bash
$ python manage.py migrate
```
*  Use a custom django command to populate database, may take a while
```bash
$ python manage.py build
```
*  (Optional) Create dist files in `static/`
```bash
$ npm install
$ npm run build
```


<!-- USAGE EXAMPLES -->
### Usage
*  Launch local server
```bash
$ python manage.py runserver
```
### Tests
#### Requirements
 [Geckodriver](https://github.com/mozilla/geckodriver/releases/) must be installed before attempting to use [selenium](https://www.selenium.dev/) tests.

* To test the project I use unittest 
```bash
$ python manage.py test
```

## Author
[Project Link](https://github.com/smtr42/P5_openfoodfact)

* **Simonnet T** - *Initial work* - [smtr42](https://github.com/smtr42)
   
  <a href="https://www.linkedin.com/in/teiva-s/">
   <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Logo.svg.original.svg" alt="linkedin" width="200" height="54">
 </a>
<br>