#!/bin/bash

apt install nginx

echo '[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock
#xd
[Install]
WantedBy=sockets.target'> /etc/systemd/system/gunicorn.socket

direccion=$(pwd)

echo "[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=$USERNAME
Group=www-data
WorkingDirectory=$direccion
ExecStart=$direccion/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          sgp.wsgi:application
#xd
[Install]
WantedBy=multi-user.target "> /etc/systemd/system/gunicorn.service

systemctl start gunicorn.socket
systemctl enable gunicorn.socket

systemctl daemon-reload
systemctl restart gunicorn


echo "server {
    listen 8080;
    server_name 127.0.0.1;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root $direccion;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
    #xd
}"> /etc/nginx/sites-available/sgp

ln -s /etc/nginx/sites-available/sgp /etc/nginx/sites-enabled

#service apache2 stop

systemctl restart nginx

ufw delete allow 8000

ufw allow 'Nginx Full'
