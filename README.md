# ci-project5
Code Institute Diploma in Full Stack Software Development - Project 5

## Contents
- [Technology Stack](#technology-stack)
- [Setup](#setup)
- [Functionality](#functionality)
- [Deployment](#deployment)
- [Testing](#testing)
- [Bugs](#bugs)

## Technology Stack
See [requirements.txt](https://github.com/ivankrauseza/ci-project5/blob/main/requirements.txt) for an overview of the development environment.  
- Python (Django)
- HTML & CSS (Bootstrap @ 5.3.2)
- JavaScript (jQuery @3.7.1 and jQueryUI @ 1.13.2)
- Database (AWS - RDS)
- Media (AWS - S3)
- Icons FontAwesome @latest
- Markdown (ReadMe)

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



## Testing
### Manual Testing
Manual testing was performed to validate that the Authentication and the E-commerce system function correctly.

## Core Functionality
### Shop
- Can all products be viewed in list format - Yes = Pass
- Can a user filter products by collection - Yes = Pass
- Can a user sort the product list by price (asc and desc) - Yes = Pass
- Can a product be viewed in detail format - Yes = Pass
- Can a logged out user add to basket - No = Pass
- Can a logged in user add to basket - Yes = Pass
- Can a user exceed the available quantity when adding to basket from Product detail page - No = Pass
- Can a user exceed the available quantity when adding to basket from Basket page - No = Fail
- Can a user delete a basket item from Basket page - Yes = Pass
- Can a user Pay for an order without a delivery address - No = Pass
- Can a user Pay for an order with a valid delivery address - Yes = Pass
- Basket
- Checkout
- Can I Search products - No = Fail

### Account
- Update Account information
- View order history and detail
- Delete Account

### Admin Dashboard
- CRUD Products
- View All orders

### General Pages
- About us
- Terms and Conditions
- Contact Us
- Privacy Policy

### Validator Testing 
#### W3C HTML
To do...

#### W3C CSS
To do...

#### PEP8
I have tested my code using https://www.pythonchecker.com/ and there are some issues where the errors refer to spacing around operators. Example: ('/') where it has recommended that I put a space around the operator like (' / ') which obviously breaks the path. I also received errors where the indentation should be 4 spaces but VS Code is tabbing the indentations but the code works fine according to the VSCode linter.  

#### Lighthouse
Overall, the Lighthouse test performed reasonably ok, across all pages.


## Bugs

## Deployment
### Deployment to Heroku
- Create Procfile (web: gunicorn cadence.wsgi)
- Freeze requirements (pip freeze > requirements.txt)
- Create New Project
- Region: Europe 
- Setup Config Vars
- Deployment Method: GitHub > 'ci-project5'
- Choose a branch to deploy 'main'
- Deploy Manually

## Credits and Resources
### Walkthroughs for inspiration
- Code Institute Walkthroughs: (Hello Django, I think therefore I blog, Boutique Ado)
- [Learning Django](https://www.linkedin.com/learning/learning-django-2/rapidly-create-web-applications)
- [MDN - Local Library](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Tutorial_local_library_website)
- [AWS S3](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html)
- [AWS S3 - Static Files](https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/)
- https://learndjango.com/tutorials/add-robotstxt-django-website#:~:text=To%20implement%20a%20robots.,a%20new%20app%20called%20pages%20.&text=Immediately%20add%20it%20to%20your%20INSTALLED_APPS%20setting.&text=Then%20create%20a%20custom%20view,on%20the%20built%2Din%20TemplateView%20.