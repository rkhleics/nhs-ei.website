# NHSEI Website

This is the repo for the NHS England & Imporvement website https://england.nhs.uk

## How to install
---

Clone this repo to your local development machine

```
git clone https://github.com/rkhleics/nhs-ei.website [your folder name:optional]
```

### 1. Install with Docker

You will need 'docker' installed on your development machine 

Get Docker: https://docs.docker.com/get-docker/

cd into the root of the project e.g.
```
cd nhs-ei.website
```

copy .env.example to .env
```
cp .env.example .env
```
after you have installed docker...
```
docker-compose up
```

This will take a while to complete and will set up an environment which you can develop on.

It mirrors all the services and packages needed to run in production.

### 2. Install with virtual environment [recommended for development work]

You will need a package on your machine to be able to setup a virual environment such as python -m venv, virtualenv or Pipenv. This example will use Pipenv

Create your virtual environment.
the python version should be >=3.8
```
Pipenv shell
```
or to set the python version...
```
Pipenv --python 3.8
```
#### Your virtual environment should now be activated

Install the requirements by running
```
pip install -r requirements.txt
```
---
here we need to make some changes so this runs with sqlite3 and so on

---