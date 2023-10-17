### Setup
**Run following commands**
* docker-compose up -d
* docker container exec -it hex_images__web python manage.py create_test_users

### Admin Url
* http://localhost:8000/admin/

### Available users to login to admin site
* username: **hex_basic** password: **hex_basic_2023**
* username: **hex_premium** password: **hex_premium_2023**
* username: **hex_enterprise** password: **hex_enterprise_2023**

### Available endpoints to use
**Please login to admin site before using these endpoints**
* http://localhost:8000/api/photos
* http://localhost:8000/api/photos/<pk>
* http://localhost:8000/api/expiring_link_view/<str:signed_link>/
* http://localhost:8000/api/expiring_links
* http://localhost:8000/api/expiring_links/<pk>
* http://localhost:8000/api/thumbnail_photos
* http://localhost:8000/media/<path>


### Testing command
* docker container exec -it hex_images__web python manage.py test --settings=hex_images.settings.testing

### Code Coverage
**93%**

### Time to finish
It took about 28 hours to finish the project
