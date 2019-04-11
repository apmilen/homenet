# pennybags
Super secret real-estate project...

## Project Quickstart

```bash
cd /opt
# Use ssh plz
git clone git@github.com:pirate/pennybags.git

# For Bash: add this line to ~/.bashrc or ~/.bash_profile
PATH=./node_modules/.bin:$PATH

# For fish: add this line to ~/.config/fish/config.fish
set -x PATH ./node_modules/.bin $PATH

# install pipenv https://github.com/pypa/pipenv
# (Optional) install pyenv for manage python versions (3.7.3)
# https://github.com/pyenv/pyenv

# creates venv (make sure uses python 3.7.3)
pipenv shell  
pipenv install  # Uses Pipfile

# init database
initdb data/database
# This needs to be called at start, later we'll use some service
pg_ctl -D data/database -l logs/postgres.log start

# create database and user in psql
# migrate
python manage.py migrate

# Start the development server
python manage.py runserver
```
Open [http://localhost:8000](http://localhost:8000) in your browser.
