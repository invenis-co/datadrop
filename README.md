# DataDrop
Easily get files from other people in a secure way.

## Features
- allow external users to upload files without account (just send them a unique link)
- get notified by email when the upload is done
- only registered users can download uploaded files
- log downloads

## How to use it
### How to receive file(s)
1. Go to Link Tab, (optionally) fill fields and generate the link
2. Send the generate URL to the sender
3. Receive an email when the download is complete
4. Download received file(s)
5. (Optional) disable the link

## Installation for production
### Build the Docker
```bash
./build-docker.sh
```

###Customize your settings 
Edit *settings-prod.py* to setup HOSTNAME, SECRET_KEY, your SMTP, etc.

###Run the Docker
```bash
./run-docker.sh
docker exec -it datadrop ./manage.py migrate
docker exec -it datadrop ./manage.py collectstatic
docker exec -it datadrop ./manage.py createsuperuser
```

### Get a certificate
The above documentation is done with a certbot / letsencrypt certificate generated

###Configure nginx
Add `client_max_body_size 10G;` to the *http* part of `/etc/nginx/nginx.conf` to enable big file upload

Create a site-available like this, replace YOUR_HOSTNAME by yours and enable it
```nginx
upstream django {
	server 127.0.0.1:8000;
}

server {
	root /var/www/html;
	server_name YOUR_HOSTNAME;

	location / {
		proxy_set_header X-Forwarded-Host $host:$server_port;
		proxy_set_header X-Forwarded-Server $host;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto https;
		proxy_pass http://localhost:8000;
	}

	location /static/ {
		alias /mnt/datadrop-static/;
	}

	listen 443 ssl;
	ssl_certificate /etc/letsencrypt/live/YOUR_HOSTNAME/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/YOUR_HOSTNAME/privkey.pem;
}

server {
	if ($host = YOUR_HOSTNAME) {
		return 301 https://$host$request_uri;
	}

	listen 80;

	server_name YOUR_HOSTNAME;
	return 404;
}
```
Restart nginx and enjoy :-D


## Installation for dev
```bash
poetry install
poetry run ./manage.py migrate
poetry run ./manage.py createsuperuser
poetry run ./manage.py runserver
```
