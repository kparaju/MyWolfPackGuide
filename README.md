#MyWolfpackGuide

Initially created for a Master's Software Engineering Course Project at NC State University, MyWolfpackGuide was developed with ease of adapatability to other brandings.

##Installation and Setup

_MyWolfpackGuide is application-driven website_

To begin, clone the repository into a directory of your choice. 

> $ git clone https://github.ncsu.edu/bynarron/MyWolfpackGuide.git

Enter the project directory and create a virtual environment to manage the project's dependencies:

> $ cd MyWolfpackGuide/ <br />
> $ virtualenv [your_virtual_environment_name] <br />
> $ source [your_virtual_environment_name]/bin/activate <br />
  
Now install the requirements:

> $ pip install -r requirements.pip

The project settings, by default, declare a Sqlite3 database. If you wish to develop locally, this is a good option. To instantiate the Database, simply sync the database and the file will be created. __Do not create a superuser quite yet:__

> $ python manage.py syncdb

Now, you will need to run migrations for MWG_Site and other tracked apps:

> $ python manage.py migrate

You're all set!

Run your test server and check out the site!

> $ python manage.py runserver

Access the server at _localhost:8000_

...And most importantly, HAVE FUN!

##Depedencies

Contents of Requirements.pip:

- Django
- PIL or Pillow
- South
- argparse
- distribute
- django-admin-bootstrapped
- django-bootstrap-form
- django-bootstrap3-datetimepicker
- django-gravatar2
- django-localflavor
- django-social-auth
- feedparser
- httplib2
- oauth2
- python-openid
- wsgiref

Contributers to MyWolfpackGuide would like to <b>sincerely</b> thank all contributers to the dependent packages!
  



