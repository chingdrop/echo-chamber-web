
## To Do List

### Infrastructure
- [ ] Better optimize Docker image build.
- [ ] Add front end application to docker-compose.

### Code
 - [ ] Connect the front end to the back end.
 - [ ] Build a webcrawler that can lookup desired pieces of information. This is done because every website is different, so some editing may need to be done by the user.
	 - [x] Install requests and beautifulsoup.
	 - [x] Determine if you can use the RestAdapter class from your other project.
	 - [x] Create a web crawler that will find all links on a website.
	 - [x] Create a function based view in Django to run the crawler.
		 - [x] Fix errors with the absolute imports.
	 - [x] Create functions to be used as shared tasks, handed off to Celery worker.\
	 - [ ] Create an area to display results from the statically crawled site.

## Completed
- [x] Install and Configure django rest framework.
- [x] Determine the best front end environment to display your app.
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
	- *This was replaced with the crawler app.*
## Articles
- Django Tutorial - https://docs.djangoproject.com/en/5.1/intro/tutorial01/
- Django, Postgres and Docker - https://learndjango.com/tutorials/django-docker-and-postgresql-tutorial
- Django and Celery - https://realpython.com/asynchronous-tasks-with-django-and-celery/
- Python Crawler - https://www.zenrows.com/blog/web-crawler-python#transitioning-to-a-real-world-web-crawler
- 