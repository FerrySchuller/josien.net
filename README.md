# josien.net

Live site: https://josien.net

josien systemd file:

```
cat /etc/systemd/system/josien.service
[Unit]
Description=uWSGI josien.net
After=network.target
  
[Service]
User=root
Group=www-data
WorkingDirectory=/prod/apps/josien.net
Environment="PATH=/prod/apps.josien.net/env/bin"
ExecStart=/prod/apps/josien.net/env/bin/uwsgi --ini web.ini

[Install]
WantedBy=multi-user.target

systemctl start josien
systemctl enable josien
systemctl status josien
```

nginx settings:
```
cat /etc/nginx/sites-available/josien.net
server {
    listen [::]:80;
    listen 80;
    server_name josien.net;
    # redirect http to https www
    return 301 https://josien.net$request_uri;

}

server {
    listen [::]:443 ssl http2;
    listen 443 ssl http2;
    server_name josien.net;
    ssl_certificate /etc/letsencrypt/live/josien.net-0001/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/josien.net-0001/privkey.pem;
    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        include uwsgi_params;
        uwsgi_pass unix:/prod/apps/josien.net/web.sock;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Access-Control-Allow-Origin "https://josien.net";
        add_header Referrer-Policy "origin-when-cross-origin" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubdomains; preload";
    }
}
```
