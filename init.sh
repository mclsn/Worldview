sudo pkill -9 python
#sudo pkill -9 gunicorn
#sudo pkill -9 nginx

sudo rm -r /home/projects/snw/core/etc/logs/gunicorn.log

sudo rm /etc/nginx/sites-enabled/default
sudo ln -sf /home/projects/snw/core/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart

sudo pkill -9 gunicorn
#sudo gunicorn -w 3 --keep-alive 1 index:wsgi_app
sudo gunicorn -c core/etc/gunicorn-wsgi.conf index:wsgi_app
