# pennybags
Super secret real-estate project...

## Project Quickstart

```bash
cd /opt
# Use ssh plz
git clone git@github.com:pirate/pennybags.git
cd pennybags

# Install system packages
apt install python3.7 python3-pip python3.7-dev libpq-dev postgresql npm

# install pipenv https://github.com/pypa/pipenv
python3.7 -m pip install --user pipenv

# (Optional) install pyenv for manage python versions (3.7.3)
# https://github.com/pyenv/pyenv

# creates venv (make sure uses python 3.7.3)
pipenv shell  
pipenv install  # Uses Pipfile

# init database
initdb data/database
mkdir -p data/logs
# This needs to be called at start, later we'll use some service
pg_ctl -D data/database -l data/logs/postgres.log start

# Create role, db and grant privileges
psql -c "CREATE USER penny WITH PASSWORD 'penny';" postgres
psql -c "CREATE DATABASE penny OWNER penny;" postgres
psql -c "GRANT ALL PRIVILEGES ON DATABASE penny TO penny;" postgres
psql -c "ALTER USER penny CREATEDB;" postgres


# Install javascript dependencies (dev machines only)
npm install -g npm
npm install --upgrade --global yarn

# For Bash: add this line to ~/.bashrc or ~/.bash_profile
PATH=./node_modules/.bin:$PATH
# For fish: add this line to ~/.config/fish/config.fish
set -x PATH ./node_modules/.bin $PATH

cd pennydjango/js
yarn install
cd ..

# create database and user in psql
# migrate
python manage.py migrate

# Start the development server
python manage.py runserver
```
Open [http://localhost:8000](http://localhost:8000) in your browser.
