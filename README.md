SkinnerBox
==========
* sudo apt-get install python-setuptools
* sudo apt-get install python-pip
* sudo apt-get install aptitude
* build mongo from [these directions](http://c-mobberley.com/wordpress/2013/10/14/raspberry-pi-mongodb-installation-the-working-guide/) THIS WILL TAKE LIKE *FOR-EV-ER*. 
* sudo pip install pymongo
* sudo apt-get install ipython
```
sudo apt-get install libblas-dev liblapack-dev python-dev libatlas-base-dev gfortran 
sudo easy_install scipy                 
sudo apt-get install python-matplotlib
```

* Now install the bottle web server, websockets, and the picamera. 
* sudo pip install bottle picamera bottle-websocket
* if mongo explodes: mongod --dbpath /var/lib/mongodb --repair
  * then sudo rm the lock file
  * sudo /etc/init.d/mongod start
  

* Original bottle-bootstrap code cribbed from [here](https://github.com/ejconlon/bottle-bootstrap).
* Complete build instructions [here]( http://www.kscottz.com/)
* 3D Models are [here.]()
* Some build photos can be [found here.](http://imgur.com/a/Aiw09)
