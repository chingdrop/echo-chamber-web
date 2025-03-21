
## To Do List
- [ ] Possibly change the Crawler app in Django to 'Echo'

### Infrastructure
- [ ] Determine if the current docker-compose setup is best for running both Django and Angular projects
- [ ] Configure the Google Cloud Developer Project
### Code
- [ ] Add the use of Google APIs
	- [ ] Google Trends
	- [ ] Google Ads Keywords
- [ ] Add the use of Twitter
- [ ] Build a method of starting the web crawling celery task
- [ ] Implement the scrapy framework inside Django
	- [x] Start the scrapy project and configure it to work inside django
	- [ ] Create a new spider class to handle broad crawling
	- [ ] Create a new pipeline for the saving of results to models
	- [x] Configure the logging in scrapy
	- [ ] Create a django management command
	- [ ] Integrate Scrapy with Celery
- [ ] Build a spider for crawling Google SERPs
	- [ ] Use the found code repo for creating a way of searching google
	- [ ] Implement my custom Rest Adapter for use in the spider
- [x] Completely rebuild the crawler models, serializers and views
	- [x] Add a model/serializer/viewset for crawl configs, histories and results

## Completed
- [x] Better optimize Docker image build.
- [x] Determine a more secure way of storing the Django secret key.
	 - [x] Store secret key in .env file.
- [x] Fix the error with VS Code debug terminal connecting to debugpy.
	- [x] Fix web's service in docker-compose.override.
 - [x] Build a webcrawler that can lookup desired pieces of information. This is done because every website is different, so some editing may need to be done by the user.
	 - [x] Install requests and beautifulsoup.
	 - [x] Determine if you can use the RestAdapter class from your other project.
	 - [x] Create a web crawler that will find all links on a website.
	 - [x] Create a function based view in Django to run the crawler.
		 - [x] Fix errors with the absolute imports.
	 - [x] Create functions to be used as shared tasks, handed off to Celery worker.
	 - [x] Create a model, serializer and viewset class to display data through DRF.
	 - [x] Alter the crawler app to use DRF viewsets and routing.
- [x] Fix problem with celery service not properly mounting volume.
- [x] Add front end application to docker-compose.
	- [x] Configure docker-compose and nginx to the correct ports.
- [x] Install and Configure django rest framework.
	- [x] Use viewsets instead of views.
	- [x] configure url routing for drf.
- [x] Determine the best front end environment to display your app. Angular
- [x] Create the echo-chamber-front project.
	- [x] Create the Git repository.
	- [x] Determine a way to install the Angular framework.
- [x] Add Dockerfile and docker-compose for project.
- [x] Set the volume for postgres and gitignore the directory.
- [x] Configure Django to use postgres.
- [x] Add Celery to be used for asynchronous task handling.
	- [x] Configure Django to use celery.
- [x] Add Redis and Celery services to the docker-compose.

## Rejected
-  Build out the Articles application. Holds articles, where I post the results of my crawler and analysis engine. 
	- *The Articles app was replaced with the Crawler app*
- Refactor the web crawler class to work with django models instead of saving files
	- Build a method to parse the url passed in the class init
	- Build a method to use the parsed url when creating the rest adapter
	- *The WebCrawler app and the use of Beautifulsoup was replaced with scrapy for a more complete framework*
## Articles
- Django Tutorial - https://docs.djangoproject.com/en/5.1/intro/tutorial01/
- Django, Postgres and Docker - https://learndjango.com/tutorials/django-docker-and-postgresql-tutorial
- Django and Celery - https://realpython.com/asynchronous-tasks-with-django-and-celery/
- Python Crawler - https://www.zenrows.com/blog/web-crawler-python#transitioning-to-a-real-world-web-crawler
- Undercrawler - https://github.com/TeamHG-Memex/undercrawler/blob/master/undercrawler/spiders.py 
  *Note - Older Link*
- Google Search on Python - https://github.com/Nv7-GitHub/googlesearch/blob/master/googlesearch/__init__.py
- 