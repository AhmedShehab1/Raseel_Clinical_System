sudo apt-get -y update
sudo apt-get -y install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv
sudo apt-get -y install mysql-server postfix supervisor nginx git mysql-client

git clone https://github.com/AhmedShehab1/Raseel_Clinical_System.git

cd Raseel_Clinical_System

python3 -m venv Raseel

source Raseel/bin/activate
sudo apt-get install pkg-config
sudo apt-get install libmysqlclient-dev


pip install wheel gunicorn mysqlclient cryptography

pip install -r requirements.txt

sudo chown ubuntu:ubuntu -R /home/ubuntu/Raseel_Clinical_System

sudo chmod 777 -R /home/ubuntu/Raseel_Clinical_System

echo "MAIL_USERNAME=info@ahmedshehab.tech
MAIL_PASSWORD=Cw$^MRk1
MAIL_DEFAULT_SENDER=info@ahmedshehab.tech
SECRET_KEY=a2f2a81a5a187bc6a76b6a57f340fe17c244d23b2cc66b86d12af1064fa72696
MAIL_SERVER=us2.smtp.mailhostbox.com
MAIL_PORT=587
DATABASE_URL=mysql+mysqldb://raseel:password@localhost:3306/Raseel_db" > .env

echo "FLASK_APP=web_flask.clinical_system
MAIL_USE_TLS=1" > .flaskenv

echo "[mysqld]
server_id           = 1
log_bin             = /var/log/mysql/mysql-bin.log
log_bin_index       = /var/log/mysql/mysql-bin.log.index
relay_log           = /var/log/mysql/mysql-relay-bin
relay_log_index     = /var/log/mysql/mysql-relay-bin.index
binlog_expire_logs_seconds = 864000
max_binlog_size     = 100M
log_replica_updates = 1
auto-increment-increment = 2
auto-increment-offset = 1
bind-address        = 0.0.0.0" >> /etc/mysql/mysql.cnf

sudo systemctl restart mysql

echo "SET GLOBAL validate_password.policy = LOW;
SET GLOBAL validate_password.length = 8;
SET GLOBAL validate_password.mixed_case_count = 0;
SET GLOBAL validate_password.number_count = 0;
SET GLOBAL validate_password.special_char_count = 0;" | sudo mysql -u root


# make a service file for the app gunicorn
echo '[Unit]
Description=gunicorn daemon
After=network.target


[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Raseel_Clinical_System
Environment="PATH=/home/ubuntu/Raseel/bin"
ExecStart=/home/ubuntu/Raseel/bin/gunicorn -w 3 -b
unix:Raseel.sock -m 007 web_flask.clinical_system:app

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/gunicorn.service
'

sudo touch /etc/systemd/system/Raseel.service


sudo echo "[Unit]
Description=Gunicorn instance to serve Raseel
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Raseel_Clinical_System
Environment="PATH=/home/ubuntu/Raseel_Clinical_System/Raseel/bin"
ExecStart=/home/ubuntu/Raseel_Clinical_System/Raseel/bin/gunicorn --workers 3 --bind unix:Raseel.sock -m 007 web_flask.clinical_system:app \
    --access-logfile /tmp/raseel-access.log \
    --error-logfile /tmp/raseel-error.log

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/Raseel.service


sudo systemctl start Raseel
sudo systemctl enable Raseel

sudo nano /etc/nginx/sites-available/Raseel

sudo echo "server {
    listen 80;
    server_name raseel.ahmedshehab.tech;
        access_log  /var/log/raseel_access.log;
        error_log /var/log/raseel_error.log;


   location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/Raseel_Clinical_System/Raseel.sock;
    }
   location ~ ^/(doctor|admin|receptionist|staff) {
                return 403;

        }
  location /static/ {
        alias /home/ubuntu/Raseel_Clinical_System/web_flask/static;
        gzip on;
        gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    }
  location /auth/static/ {
        alias /home/ubuntu/Raseel_Clinical_System/web_flask/auth/static/;
        gzip on;
        gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
        }
}


server {
    listen 80;
    server_name staff.ahmedshehab.tech;
        access_log  /var/log/staff_raseel_access.log;
        error_log /var/log/staff_raseel_error.log;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/Raseel_Clinical_System/Raseel.sock;
    }
  location /static/ {
        alias /home/ubuntu/Raseel_Clinical_System/web_flask/static/;
        gzip on;
        gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    }
  location /auth/static/ {
        alias /home/ubuntu/Raseel_Clinical_System/web_flask/auth/static/;
        gzip on;
        gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
        }
}" > /etc/nginx/sites-available/Raseel

sudo ln -s /etc/nginx/sites-available/Raseel /etc/nginx/sites-enabled

sudo systemctl restart nginx

sudo ufw delete allow 5000

curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list

sudo apt update

sudo apt install elasticsearch

sudo nano /etc/elasticsearch/elasticsearch.yml

sudo systemctl start elasticsearch

sudo systemctl enable elasticsearch


sudo cat /etc/letsencrypt/live/staff.ahmedshehab.tech/fullchain.pem /etc/letsencrypt/live/staff.ahmedshehab.tech/privkey.pem > /etc/haproxy/certs/staff.ahmedshehab.tech.pem
