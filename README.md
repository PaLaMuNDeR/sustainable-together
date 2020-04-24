# sustainable-together
EarthxHack Hackaton - Fill in the missing gap of global collaboration on sustainibility issues

# Installation
1. Install Docker (https://docs.docker.com/install/), for Windows install Docker Tools (https://docs.docker.com/toolbox/overview/#ready-to-get-started)
2. Run Docker 
3. Clone the project
4. Run `docker build` - it will start building the project - might take 5-10 minutes with good connection
5. Run `docker-compose up` - if everything went well it will run the server with all the modules
To run it daemonized (as a background task) - run `docker-compose up -d`
6. Open the browser at `http://localhost:3000` and create new user.
7. Open the terminal and turn this user to superuser with the following set of commands below. 
Two options for creating Admin:
7.1 Open the terminal and run
```
docker-compose exec back-end /bin/bash
cd st/back-end
python manage.py createsuperuser
```
7.2 The superuser is the equivalent of the Admin as of the scope of the project: 
```
docker-compose exec back-end /bin/bash
cd st/back-end
python manage.py shell
>>> from api.models import Client
>>> u = Client.objects.last().user
>>> u.is_staff = True
>>> u.is_superuser = True
>>> u.save()
```

8. Now you could navigate in your browser to `localhost:8000/admin` and enter as an admin 

9. To run tests enter the container and execute the tests with the following set of commands:
```
docker-compose exec back-end /bin/bash
cd calories/back-end
python manage.py test
```

10. Documentation is available at `http://localhost:8000/admin/doc/`