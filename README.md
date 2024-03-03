# ci-project5 - Cadence Tools
For my Project 5 at the Code Institute I have created an e-commerce platform for a brand called Cadence Tools which sells high quality hand and power tools. The platform is integrated with Stripe Checkout, and using AWS for database and file storage. The main aim of this project was to make the most of the default styles and functions offered by bootstrap.

![https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/responsive.jpg](https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/responsive.jpg)

## Contents
- [Technology Stack](#technology-stack)
- [User Experience](#user-experience)
- [Database Schema](#database-schema)
- [User Stories](#user-stories)
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
- Stripe Checkout
- Icons FontAwesome @latest
- Markdown (ReadMe)

## User Experience (MVP)
 Taking inspiration from a previous role. I wanted to develop an updated, simple and cleaner e-commerce experience. I have also taken inspiration from IKEA to simplify the display and draw attention to the products right away and reduce distraction. Overall it is a standard e-commerce website that contains traditional user flow of Product List / Product Detail / Basket / Checkout but the User needs to register their account in order to add products to the basket. Users also have the basic tools to view previous orders and manage their account.

 ### Wireframes and Mockups
 ![https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/figma_wireframes.jpg](https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/figma_wireframes.jpg)  
 ![https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/figma_mockups.jpg](https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/figma_mockups.jpg)

 ### Customers: Logged in users VS logged out users
- I have allowed anyone to view the products, however a logged out user CANNOT add any product to the basket.
- To add a product to the basket the user needs to sign up (also needed for stripe id to be created).
- Logged in user can order, pay and view previous orders.

 ### Checkout
 I have used Stripe Checkout and Webhook to manage the Checkout process so there was no need to create a custom checkout view. When the user creates there Cadence account, they are assigned a stripe id so that their account and stripe id are already linked. This means that any purchases they make are linked via the stripe id.

### Staff: Logged in
- Staff are able to login and view the website as a regular customer, but they also have additional tools.
- They can Manage Products and Orders.
- Shortcut to edit all products from the product list page.
- Shortcut links to edit a product while viewing the product detail.

## Database Schema
Using experience gained working in MS365 Dynamics NAV, I tried to replicate the database schema in it's simplest form to also structure the project in such a way that if it needed to be integrated into an ERP system that it would follow a similar approach.
![https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/database_shema.jpg](https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/database_shema.jpg)

## User Stories
User Stories managed through ASANA as I am more comfortable using it over GitHub Issues.
![https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/user_stories.jpg](https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/user_stories.jpg)

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

### Core Functionality
#### Shop
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
- Can I Search products - No = Fail

### Accounts (General users / Staff / Superusers)
- Can a any user other than a superuser access the backened - No = Pass
- Can a general user create an account - Yes = Pass
- Can a general user edit an account - Yes = Pass
- Can a general user delete an account - Yes = Pass
- Can a general user see previous orders if existing - Yes = Pass
- Can a general user see admin/dashboard areas - No = Pass
- Can a general user make themselves a staff member - No = Pass
- Can a staff member see admin/dashboard areas - Yes = Pass
- Can a staff member manage products and orders if existing - Yes = Pass

### Admin Backened
- CRUD Products and Collections - Yes = Pass
- CRUD Users - Yes = Pass
- View All orders - Yes = Pass

### General Pages
- About us
- Terms and Conditions
- Contact Us
- Privacy Policy

### Validator Testing 
#### W3C HTML
Several pages were test and passed the validation without errors:
![https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/html_validation.jpg](https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/html_validation.jpg)

#### W3C CSS
Core Stylesheet test and no errors:
![https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/css_validation.jpg](https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/css_validation.jpg)

#### PEP8
I have tested my code using https://www.pythonchecker.com/ and there are some issues where the errors refer to spacing around operators. Example: ('/') where it has recommended that I put a space around the operator like (' / ') which obviously breaks the path. I also received errors where the indentation should be 4 spaces but VS Code is tabbing the indentations but the code works fine according to the VSCode linter. Generally the checker is repeating the same errors and nothing stands out after testing several views, form, models blocks of python code. Maybe I am doing something wrong. 
![https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/pep8_validation.jpg](https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/pep8_validation.jpg)

#### Lighthouse
Overall, the Lighthouse test performed reasonably ok, across all pages.  
![https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/lighthouse.jpg](https://bmie23a.s3.eu-west-1.amazonaws.com/uploads/readme/lighthouse.jpg)


## Bugs
### Sitemap
I do not understand the built in Sitemap generator yet so I used an external generator.  

### Stripe Webhook
I am not sure the Webhook url configuration is 100% reliable and if my config is correct but payments seem to process.

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
- [My Previous CI Project 4](https://github.com/ivankrauseza/ci-project4)
- Code Institute Walkthroughs: (Hello Django, I think therefore I blog, Boutique Ado)
- [Learning Django](https://www.linkedin.com/learning/learning-django-2/rapidly-create-web-applications)
- [MDN - Local Library](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Tutorial_local_library_website)
- [AWS S3](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html)
- [AWS S3 - Static Files](https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/)
- [Django Stripe Integration](https://testdriven.io/blog/django-stripe-tutorial/)
- [robots.txt](https://learndjango.com/tutorials/add-robotstxt-django-website#:~:text=To%20implement%20a%20robots.,a%20new%20app%20called%20pages%20.&text=Immediately%20add%20it%20to%20your%20INSTALLED_APPS%20setting.&text=Then%20create%20a%20custom%20view,on%20the%20built%2Din%20TemplateView%20.)
- [404 and 500 error pages](https://learndjango.com/tutorials/customizing-django-404-and-500-error-pages)
- [Sitemap Generator](https://www.xml-sitemaps.com/)