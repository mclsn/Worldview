sudo pkill -9 python
sudo pkill -9 gunicorn
sudo pkill -9 nginx

sudo rm -r /home/projects/snw/core/etc/logs/gunicorn.log
sudo rm /etc/nginx/sites-enabled/default

sudo ln -sf /home/projects/snw/core/bin/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart

sudo pkill -9 gunicorn
sudo gunicorn -c core/etc/gunicorn-wsgi.conf index:wsgi_app
