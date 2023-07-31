python3 -m pip install -r requirements.txt
python3.8 manage.py makemigrations --noinput
python3.8 manage.py migrate --noinput
python3.8 manage.py collectstatic --noinput --clear