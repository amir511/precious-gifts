# Precious Gifts
Precious gifts is a preconfigured CMS that comes with a built in e-commerce basic system that suits the needs of small to medium businesses.

Precious gifts is a free open source web application based on Django and Django CMS.

## Features:
* Works out of the box, minimal or no coding is required.
* CMS preconfigured with bootstrap and font awesome.
* Built in E-commerce.
* Product searching and filtering functionality.
* Email notifications.
* Seller manages whole website from the enhanced admin panel.
* Built in bootstrap themes based on bootswatch themes.
* Ability to add forms (e.g. contact us form) from the admin panel.

## Installation:
* Clone the project
* Create a virtual environment beside the project directory:
```
python3 -m venv venv
```
* activate the virtual environment:
```
source venv/bin/activate
```
* Change to the project directory and install requirements:
```
cd precious-gifts
pip install -r requirements.txt
```
* Setup your database, **Postgresql** is manadatory for the searching feature to work.

switch to postgres user and create new user and database:
```
sudo su postgres
createuser --createdb --pwprompt preciousdev
createdb -U preciousdev -W -h localhost precious
```
off course in production you have to change the database name and password
* Migrate the database:
```
python manage.py migrate
```
* Load the fixture data of email templates, these are default html templates that are used for emails, they can be customized later from the admin panel:
```
python manage.py loaddata mail_templates.json
```
* Create a super user account:
```
python manage.py createsuperuser
```
* (Optional) Now you can start customizing the project's settings to suit your needs, if you are happy with the defaults, skip to running the server step:

    Open the settings file located at `precious_gifts/settings.py`:

    * Change the `TIME_ZONE` to suit your time zone.
    * Change the `LANGUAGES` to suite your preferred set of languages.
    * Head to `# Email Settings` and change to your email server that will be used in sending emails to buyers and admins.
    * The `ADMINS` option holds the admin email that will recieve emails upon new orders, order cancellations, and when a server error occurs.
    * `DISABLE_EMAIL_TEMPLATES_EDIT` This option if set to True, will not allow the content editor to make changes to the email templates, this is a safety procedure because the email templates has variables that gets replaced in the backend with user info, order details ..etc., Only set this option to `False` if your content editor is aware that the variables in `{}` should not be removed or modified.
    * Change `WEBSITE_NAME` from Precious Gifts to your desired project name, this name will appear in the navbar and in the email templates.
    * Set the desired `BOOTSTRAP_THEME` from the available themes, this will automatically change the theme of the application.

* Now you are ready to **Run the server**:
```
python manage.py runserver
```
* Production settings:

    Off course in case of production, other steps should be made, Please refer to the Django Documentation.
    
    But I will list here some important points:
    * Change the database name, password, and User.
    * Change the `SECRET_KEY` option.
    * Change `DEBUG` to `False`.
    * Add your domain name in the `ALLOWED_HOSTS`.
    * Run: `python manage.py collectstatic`.



## Usage Guide:
### Website Initial setup:
* Log in with your admin credentials.
* Start adding pages, e.g. the home page.
* Bootstrap 4 components and font awesome are both available to the content editor from django cms.
* Add a footer that will automatically appear in all the pages.
* The accounts app is already there, with *Log In*, *Sign up* and *Log Out* links in the navbar.
* Start a new page, name it e.g. **shop**.
* After saving it, head to the advanced settings, choose *Store Menu* in **Attached Menu**, and choose *store* in **Application**.
* Your shop is now ready and appears in the navbar menu.
* Add a *Contact us* page.
* Attach the *Form* application in the **Application** menu.
* Now head to the structure of the page.
* Add a Form, configure your form and add its fields.
* Make sure to adjust the form appearance in the page by the means of bootstrap container.
* The following CSS classes are available for you to add to your components to customize its appearance directly from the django cms panel:
    * `card-shadow`: adds shadow to cards.
    * `text-shadow`: adds shadow to text.
    
    Feel free to add more custom classes if you wish in `precious_gifts/static/css/base.css`
* Head to **Sites** in the Administration panel, change the site name to your domain name.
* **You are done!**
### Managing the website:
* Managing the website is pretty easy and self explanatory, I will just explain some points to make it more clear.
* Head to the **Administration** panel.
* The **ACCOUNTS>Buyers** menu, displays a list of the users that have registered to your website, no action required from you here.
* The **FORMS>Form submissions** menu shows the submissions of the forms you create in the website (e.g. Contact Us form).
* Head to the **MAIL>Mail templates** menu, to change existing email templates that are used when mailing users and administrators, You can edit these templates using the built in rich text editor, don't change the variables inside `{}` because they are used and replaced from the backend.

    If the email templates are not editable, the developer should change the `DISABLE_EMAIL_TEMPLATES_EDIT` to `False` in the project settings file.
* Use the `SNIPPETS>snippets` menu to add small reusable html snippets, that can be used later as a component in your pages, e.g. add font awesome snippets.

* In the `STORE>Products` menu, start adding your products you wish to sell on your website.
* In the `STORE>Shipping Fees` menu, add a single record of the amount of the shipping fees you wish to add to the orders.
* In the `STORE>Orders` menu, check regulary for orders set by website users, change the order status when relevant for the user to know the status of his/her order.
* Enjoy !

## Contact me:
You are welcomed to add feature requests or bug reports here on Github.

If you want to cantact me directly please use : **amir.anwar.said@gmail.com**

