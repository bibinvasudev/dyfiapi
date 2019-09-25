This project is for the backed operation of the dyfi membership campaign.

Tools used

1. mongodb - v4.0.12 abd above
2. Other main packages:
    django==1.11.17
    django-rest-framework-mongoengine==3.3.0
    djangorestframework==3.4.6
    mongoengine==0.9.0
    pymongo==2.8.1
    python-json-logger==0.1.2
    pytz==2019.2
3. Prefered os - Ubuntu 18.04 and above

4. For mongodb installation refer:
   https://tecadmin.net/install-mongodb-on-ubuntu/



**Issues and solution**
1. After installing the django and other packges from requirements.txt , if you are facing import issues like below:

"ImportError: Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?"

Then install the packages with the command "python3 -m pip install -r requirments.txt"

2. There are certain bug with python3 and django 1.11 so strictly use django1.11.17
  otherwise we will get error like :

  File "/home/bibin/connectingkerala-master/virtualenv/lib/python3.7/site-packages/django/contrib/admin/widgets.py", line 151
    '%s=%s' % (k, v) for k, v in params.items(),
    ^
SyntaxError: Generator expression must be parenthesized


Note- 

The branch naming standard

1. All user branch name should start with the username eg- for user bibin - bibin-<AnyIdetifier>, for user nikesh - nikesh-<AnyIdetifier>
   After each change raise pull request with metapipeline
2. The branch metapipeline is for testing the changes and once its verified we will merge to master.
   So please align your branch with metapipeline initially and create branch from metapipeline and and raise pull request to merge to metapipeline
