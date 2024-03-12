cd /var/www/flasklingo

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

sudo systemctl restart flasklingo.service 
