# GOALS:

* provide an alternative to the PHP based tracker frontends such as TBDev and Gazelle
* utilize a MVC framework to create a more organized and modular tracker platform
* establish a platform for users to share modules (apps) that they write, and promote collaboration on addition to the codebase
* remain easy for users to install and modify, but not at the sake of performance
* internationalisation, easily translatable

# DEPENDENCIES:

* Python 2.4 =< (not 3.x) 	http://python.org/download/
* Django 1.2 =< 		http://www.djangoproject.com/download/
* MySQL 5.1 =< 			http://www.mysql.com/downloads/
* mysql-python 1.2.3 =< 	http://mysql-python.sourceforge.net/
* Solr 1.3 =< 			http://lucene.apache.org/solr/ (solr setup instructions @ http://docs.haystacksearch.org/dev/installing_search_engines.html#solr )
* Pysolr 2.0.9 =<		http://github.com/toastdriven/pysolr
* django-haystack 1.0 =< 	http://haystacksearch.org/
* memcached 1.4.5 =<  		http://memcached.org/
* python-memcached 1.45 =<	http://www.tummy.com/Community/software/python-memcached/
* queues .5 =<			http://code.google.com/p/queues/
* queued_search 1.0 =<		http://github.com/toastdriven/queued_search
* piston 0.2.2 =<		http://bitbucket.org/jespern/django-piston/wiki/Home
* django-debug-toolbar =<	http://github.com/robhudson/django-debug-toolbar
* BitTorrent-bencode =< 	http://pypi.python.org/pypi/BitTorrent-bencode/5.0.8 (just copy bencode.py and BTL.py into site-libs)
* Jinja2 2.5 =<			http://jinja.pocoo.org/2/

# SETUP:

## Solr:

	cd $HOME
	curl -O http://apache.mirrors.tds.net/lucene/solr/1.3.0/apache-solr-1.3.0.tgz           (or more recent version of solr, 1.4.1 is the latest)
	tar xvzf apache-solr-1.3.0.tgz
	cd apache-solr-1.3.0/example
	java -jar start.jar

	# Go to your benzene root directory

	python manage.py build_solr_schema > $HOME/apache-solr-1.3.0/example/solr/conf/schema.xml

## MySQL:

	# In mysql ('mysql -u root')

	CREATE USER 'benzene_user'@'localhost';
	CREATE DATABASE benzene;
	GRANT ALL ON benzene.* to 'benzene_user'@'localhost';

	python manage.py syncdb

## Site Setup:

	# Go to your benzene root directory
	
	python manage.py syncdb
	python manage.py benzene
