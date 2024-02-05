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

### Environment Variables and Gitignore
Create .gitignore, and add 'env.py' to the list. 

### Connect to AWS RDS
Setup aws rds database and connection to run initial migrations. Then remove default sqlite file.

### Create Superuser
```
python manage.py createsuperuser
```

### Create initial templates
Setup templates/base.html, and shop/templates/shop_index.html with basic info to test.


### Include 3rd-Party Packages
- Bootstrap
- Font Awesome
- Jquery & JqueryUI
- PopperJS