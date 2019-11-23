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
------------

Added the following to connectingkerala/settings.py

ALLOWED_HOSTS = ['139.59.37.100']


For running in server use the following commands:

python manage.py runserver 139.59.37.100:8000

=============================================


For actuall hosting in digitalocean please refer the link :

https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-16-04

THe final /etc/apache2/sites-available/000-default.conf in the dyfiapi digitlocean server looks like:



<VirtualHost *:80>

        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

    <Directory /root/dyfiapi/connectingkerala>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess dyfiapi python-home=/root/virtualenv_dyfi_api python-path=/root/dyfiapi
    WSGIProcessGroup dyfiapi
    WSGIScriptAlias / /root/dyfiapi/connectingkerala/wsgi.py
</VirtualHost>


ADI-DOC

Groups
1.	Login
Request URL: http://localhost:8000/login
Method: POST
Request Payload: {“dob”: “01/01/1990”, “mobile_no”: “00”}

Response: {“token”: <jwt_token with first_name and mobile_no>}


For every other request you have to pass this jwt token in the header as “Authorization”

2.	Get Levels
Request URL: http://localhost:8000/levels
Method : GET

3.	Create Group
Request URL: http://localhost:8000/groups
Method : POST
Request Payload: 
	{
		"title": "K1",
		"level_id": "5d87203f41dc466648dbd83d",
		"parent_group_id": “5d87423241dc465e74ea74f9”
	}
4.	List Groups
Request URL: http://localhost:8000/groups
Method : GET
5.	Get Group Details
Request URL: http://localhost:8000/groups/<group_id>
Method : GET

6.	Update Group
Request URL: http://localhost:8000/groups/<group_id>
Method : PUT
Request Payload: { “Title”: “K2”}

7.	Delete Group
Request URL: http://localhost:8000/groups/<group_id>
Method : DELETE

8.	Add Member

Request URL: http://localhost:8000/members
Method : POST
Request Payload: 
	{
		"first_name": "Sachin",
		“middle_name”: “Ramesh”
		"last_name": "Tendulkar",
		“mobile_no”: “98038402348”,
		“dob”: “01/01/1990”,
		“gender”: “male”,
“level_id”: “5d87423241dc465e74ea74f9”
		"group_ids": [“5d87423241dc465e74ea74f9”, “5d87423241dc465e74ea4545”]
	}
9.	List Members
Request URL: http://localhost:8000/members
Method : GET
10.	Get Group Details
Request URL: http://localhost:8000/members/<member_id>
Method : GET

11.	Update Group
Request URL: http://localhost:8000/members/<member_id>
Method : PUT
Request Payload: { “middle_name”: “middlename”}

12.	Delete Group
Request URL: http://localhost:8000/members/<member_id>
Method : DELETE


13.	Image Upload
Request URL: http://localhost:8000/config/banner_image
Method : POST
Request Payload: { “banner_image”: <bas64image data>}
	
14.	Get Image
Request URL: http://localhost:8000/config/banner_image
Method : Get
	
15.	Replace Image
Request URL: http://localhost:8000/config/banner_image
Method : PUT
Request Payload: { “banner_image”: <bas64image data>}
	
16.	Search Members using mobile_no
Request URL: http://localhost:8000/members
Method : GET
Request Query Params: { “mobile_no”: "87987923423"}

17.	Get all members excel data
Request URL: http://localhost:8000/members/export_data
Method : GET
Request Query Params: { “mobile_no”: "87987923423"}

18.	Get excel data of members in group with group id "90902938023434"-
Request URL: http://localhost:8000/members/export_data
Method : GET
Request Query Params: { “group_id”: "90902938023434"}

19.	Get My Profile -details of logged in member(Me)
Request URL: http://localhost:8000/members/me
Method : GET

20.	Update My Profile
Request URL: http://localhost:8000/members/me
Method : PUT
Request Payload: { “middle_name”: “middlename”}

21. Update My Profile Image
Request URL: http://localhost:8000/members/me
Method : PUT
Request Payload: { “image”: "base64image" }

22. Update Member Image
Request URL: http://localhost:8000/members/<member_id>
Method : PUT
Request Payload: { “image”: "base64image" }


APIs to set Group Admin
======================

23.Set Group Admin
Request URL: http://localhost:8000/groups/<group_id>/add_admin
Method : PUT
Request Payload: { “member_id”: <member_id> }

24.Set Group Admin
Request URL: http://localhost:8000/groups/<group_id>/remove_admin
Method : PUT
Request Payload: { “member_id”: <member_id> }


