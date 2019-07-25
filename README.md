# Pennybags (aka HomeNet)

Apartment rental listing platform to match realtors with potential home renters and buyers.

## Project Quickstart

---

### 0. Clone the repository

Clone this repo into the `/opt` directory:
```bash
# Use ssh (not https) to avoid push permission errors
git clone git@github.com:pirate/pennybags.git /opt/pennybags
```

If you clone it elsewhere instead (e.g. inside your home folder), you must symlink `/opt/pennybags` to the repo location:
```bash
ln -s /path/to/cloned/repo/pennybags /opt/pennybags
```

---

### 1. Install the dependencies

#### Python dependencies

##### Install `Python >= 3.7.4`
```bash
sudo apt install python3.7 python3-pip python3.7-dev libpango1.0-0  # or `brew install python3 pango`
```
Optional: You can also use [pyenv](https://github.com/pyenv/pyenv) to install python3.7 if you have trouble installing it with `apt` or `brew`.

##### Install the [`pipenv`](https://github.com/pypa/pipenv) package manager
```bash
python3.7 -m pip install --user pipenv
```

##### Install the project Python dependencies

(The Python dependencies are defined in `./Pipfile`)
```bash
cd /opt/pennybags
pipenv install
```

#### Javascript dependencies (dev machines only):

##### Install `Node >= 12.6.0`
```bash
sudo apt install npm gdal-bin   # or `brew install node gdal`
npm install -g npm
```

##### Install the [`yarn`](https://yarnpkg.com/) package manager
```bash
npm install --upgrade --global yarn
```

##### Install the project JS dependencies

(The JS dependencies are defined in `./pennydjango/js/package.json`)
```bash
cd /opt/pennybags/pennydjango/js
yarn install
```

---

### 2. Setup the system environment

#### Point `homenet.l` domain traffic to localhost

Add this line to your `/etc/hosts` file (`sudo` is required to edit it):
```
127.0.0.1   homenet.l
```

#### Make the JS and Python dependencies accessible from your `$PATH`

If you use Bash, add these lines to your `~/.bashrc` or `~/.bash_profile` file:
```bash
PATH=./node_modules/.bin:$PATH
PIPENV_VENV_IN_PROJECT=1
```

If you use Fish, add these lines to your `~/.config/fish/config.fish` file:
```fish
set -x ./node_modules/.bin $PATH
set -x PIPENV_VENV_IN_PROJECT 1
```

#### Install supervisord

Supervisord is used to manage starting and stopping nginx, postgresql, and any other background services.
```bash
sudo apt install supervisor   # or `brew install supervisor`
```

---

### 3. Setup Postgresql

#### Install the latest Postgresl version

On Ubuntu:
```bash
sudo echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" >> /etc/apt/sources.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt install postgresql libpq-dev
```

On macOS:
```bash
brew install postgresql
brew link --overwrite --force postgresql
```

#### Instantiate the pennybags database
```bash
cd /opt/pennybags

# instantiate a new postgresql db data dir
initdb data/database

# Create role, db, and grant privileges
pg_ctl -D data/database start
psql -c "CREATE USER penny WITH PASSWORD 'penny';" postgres
psql -c "CREATE DATABASE penny OWNER penny;" postgres
psql -c "GRANT ALL PRIVILEGES ON DATABASE penny TO penny;" postgres
psql -c "ALTER USER penny CREATEDB;" postgres
pg_ctl -D data/database stop
```

#### Run the initial migrations
```bash
cd /opt/pennybags

# Run the initial db migrations
pg_ctl -D data/database start
./.venv/bin/python ./pennydjango/manage.py migrate
pg_ctl -D data/database stop
```

---

### 4. Setup the Nginx webserver

#### Install the latest Nginx version

On Ubuntu:
```bash
sudo add-apt-repository -y ppa:nginx/stable
sudo apt update
sudo apt install nginx
```

On macOS:
```bash
brew install nginx
```

#### Generate a self-signed SSL certificate for `homenet.l`
```bash
cd /opt/pennybags/data/certs
./generate.sh homenet.l
```

---

### 5. Run the development server

#### Start Postgresql and Nginx
Background processes are managed by Supervisord, they must be started in order for Django to work.

On Ubuntu:
```bash
supervisord -c /opt/pennybags/etc/supervisor/ubuntu-dev.conf
```

On macOS:
```bash
supervisord -c /opt/pennybags/etc/supervisor/mac-dev.conf
```

#### Start Django Runserver
```bash
cd /opt/pennybags

# activate the virtualenv
pipenv shell
# or source .venb/bin/activate       (in bash)
# or source .venv/bin/activate.fish  (in fish)

# Start the django runserver
./manage.py runserver
```

✅ Then open [https://homenet.l](https://homenet.l) in your browser.

Alternatively, open [http://127.0.0.1:8000](http://127.0.0.1:8000) to access runserver directly without using nginx (always use nginx if possible though).

---

## Common Tasks

### Activate the Python Virtualenv
```bash
cd /opt/pennybags
source .venv/bin/activate  # or source .venv/bin/activate.fish
```

### Start/stop/restart Nginx or Postgresql

Replace `ubuntu-dev.conf` below with `mac-dev.conf` if using macOS.
```bash
cd /opt/pennybags

# make sure supervisord is running first
supervisord -c etc/supervisor/ubuntu-dev.conf

# then check the status of all services or a specific service
supervisorctl -c etc/supervisor/ubuntu-dev.conf status <service|all>
supervisorctl -c etc/supervisor/ubuntu-dev.conf stop <service|all>
supervisorctl -c etc/supervisor/ubuntu-dev.conf start <service|all>
```

### Inspect logfile output
```bash
cd /opt/pennybags/data/logs
tail -f nginx.err
tail -f nginx.out
tail -f postgresql.err
tail -f postgresql.out
tail -f reloads.log
# etc.
```

### Run Migrations
```bash
# first make sure postgresql is running with supervisord

cd /opt/pennybags/pennydjango
# activate virtualenv (see above)

./manage.py migrate
```

---

## Troubleshooting

#### Check the installed binary versions
```bash
python3 --version       # should be >= 3.7.3, check inside virtualenv too
pipenv --version        # should be >= 2018.11.26

node --version          # should be >= 12.6.0
npm --version           # should be >= 6.10.2
yarn --version          # should be >= 1.17.3

supervisord --version   # should be >= 3.3.5
postgres --version      # should be >= 10.0
nginx --version         # should be >= 1.15.12      
```

#### Check the installed binary locations
```bash
which <binary>      # e.g. `which nginx` or `which python3`
```

#### Yarn install/locking failures
Clear the yarn cache and try again.
```bash
yarn cache clean
yarn install
```

#### Pipenv install/locking failures
Clear the pipenv cache and try again.
```bash
pipenv lock --clear
pipenv clean
pipenv install
```
