# ci-project5
Code Institute Diploma in Full Stack Software Development - Project 5

## Contents
- [Setup](#setup)
- [Functionality](#functionality)
- [Deployment](#deployment)
- [Testing](#testing)
- [Bugs](#bugs)

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


### Create the Shop Models
- Product
- Collection
- Files
- Basket
- Order
- Order Lines (Linked to Order)

## Functionality
### Shop
- View all products
- View products by collection
- Search products
- Product detail
- Basket
- Checkout

### Account
- Update Account information
- View order history and detail
- Delete Account

### Admin Dashboard
- CRUD Products
- View All orders

### Pages
- About us
- Terms and Conditions
- Contact Us
- Privacy Policy

## Deployment
### Deployment to Heroku
- Create Procfile (web: gunicorn lavoro.wsgi)
- Freeze requirements (pip freeze > requirements.txt)
- Create New Project
- Region: Europe 
- Setup Config Vars
- Deployment Method: GitHub > 'ci-project4'
- Choose a branch to deploy 'main'
- Deploy Manually

## Testing
### Validator Testing 
#### W3C HTML
To do...

#### W3C CSS
To do...

#### PEP8
To do...

#### Lighthouse
To do...


## Bugs

## Credits and Resources
- https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
- https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/
- https://fontawesome.com