sudo apt-get -y update
sudo apt-get -y install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv
sudo apt-get -y install mysql-server postfix supervisor nginx git

git clone https://github.com/AhmedShehab1/Raseel_Clinical_System.git

cd Raseel_Clinical_System

python3 -m venv Raseel

source Raseel/bin/activate

pip install wheel gunicorn mysqlclient cryptography

pip install -r requirements.txt

echo "MAIL_USERNAME=info@ahmedshehab.tech
MAIL_PASSWORD=Cw$^MRk1
MAIL_DEFAULT_SENDER=info@ahmedshehab.tech
SECRET_KEY=a2f2a81a5a187bc6a76b6a57f340fe17c244d23b2cc66b86d12af1064fa72696
MAIL_SERVER=us2.smtp.mailhostbox.com
MAIL_PORT=587
DATABASE_URL=mysql+mysqldb://Ahmed:ahmedshehab@localhost:3306/Raseel_db" > .env

echo "FLASK_APP=web_flask.clinical_system MAIL_USE_TLS=1" > .flaskenv
