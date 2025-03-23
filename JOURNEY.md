
## To Do List
- [ ] Add documentation on how to get past the CSRF token check in Postman
	- [ ] Put the documentation in the git repo and the postman workspace

### Infrastructure
- [ ] Determine if the current docker-compose setup is best for running both Django and Angular projects
- [ ] Configure the Google Cloud Developer Project
### Code
- [ ] Add the use of Google APIs
	- [ ] Google Trends
	- [ ] Google Ads Keywords
- [ ] Add the use of Twitter
- [ ] Implement the scrapy framework inside Django
	- [x] Start the scrapy project and configure it to work inside django
	- [x] Create a new pipeline for the saving of results to models
	- [x] Configure the logging in scrapy
	- [x] Determine the best way to start the google search spider inside a view
		- [x] Handle CSRF token issues
	- [ ] Create a django management command
	- [x] Integrate Scrapy with Celery
- [ ] Fix the Google search spider to properly scrape SERPs
	- [ ] Fix the ability to save the results as models

## Completed
- [x] Find the best way of exploring the postgres database
- [x] Build a spider for crawling Google SERPs
	- [x] Use the found code repo for creating a way of searching google
	- [x] Implement my custom Rest Adapter for use in the spider
	- [x] Build the custom parser
	- [x] Implement the use items and pipelines
	- [x] Test the implementation of all the pieces
- [x] Completely rebuild the crawler models, serializers and views
	- [x] Add a model/serializer/viewset for crawl configs, histories and results
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
- Create a new spider class to handle broad crawling
	- *Crawling Google search results can be a great way to have endless information but only need a simple crawler*
## Articles
- Django Tutorial - https://docs.djangoproject.com/en/5.1/intro/tutorial01/
- Django, Postgres and Docker - https://learndjango.com/tutorials/django-docker-and-postgresql-tutorial
- Django and Celery - https://realpython.com/asynchronous-tasks-with-django-and-celery/
- Python Crawler - https://www.zenrows.com/blog/web-crawler-python#transitioning-to-a-real-world-web-crawler
- Undercrawler - https://github.com/TeamHG-Memex/undercrawler/blob/master/undercrawler/spiders.py 
  *Note - Older Link*
- Google Search on Python - https://github.com/Nv7-GitHub/googlesearch/blob/master/googlesearch/__init__.py
- 