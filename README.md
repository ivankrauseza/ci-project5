# ci-project5
Code Institute Diploma in Full Stack Software Development - Project 5

## Contents
- [Setup](#setup)

## Setup
### Clone Github Repo
```
git clone https://github.com/ivankrauseza/ci-project5.git
```
### Start Django Project and App
```
django-admin startproject cadence .  
python manage.py startapp shop
```
#### Update settings.py
Add the 'shop' app to INSTALLED_APPS in 'settings.py'
```
INSTALLED_APPS = [
    ...
    'shop',
]
```