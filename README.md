# Pennybags (aka HomeNet)

Apartment rental listing platform to match realtors with potential home renters and buyers.

- https://homenet.zalad.io
- https://homenet.zalad.io/admin

Services:  
- https://dashboard.stripe.com/account/team
- https://app.mailgun.com/app/account/settings
- https://dash.cloudflare.com/413ad3842c5a82a780b582d8de8dc903/zalad.io/dns
- https://console.cloud.google.com/google/maps-apis/overview?pli=1&project=pennybags-1556050514027

## Project Quickstart

---

### 0. Clone the repository

Clone this repo into the `/opt` directory:
```bash
# Use ssh (not https) to avoid push permission errors
# (replace YOUR_GITHUB_USER with your github username)
git clone git@github.com:YOUR_GITHUB_USER/pennybags.git /opt/monadical.homenet
```

If you clone it elsewhere instead (e.g. inside your home folder), you must symlink `/opt/monadical.homenet` to the repo location:
```bash
ln -s /path/to/cloned/repo/pennybags /opt/monadical.homenet
ln -s /opt/monadical.homenet /opt/pennybags
```

---

### 1. Install the dependencies

#### Make the JS and Python dependencies accessible from your `$PATH`

If you use Bash, add these lines to your `~/.bashrc` or `~/.bash_profile` file:
```bash
PATH=./node_modules/.bin:./.venv/bin:./../.venv/bin:$PATH
PIPENV_VENV_IN_PROJECT=1
PIPENV_IGNORE_VIRTUALENVS=1
```

If you use Fish, add these lines to your `~/.config/fish/config.fish` file:
```fish
set -x PATH ./node_modules/.bin ./.venv/bin ./../.venv/bin $PATH
set -x PIPENV_VENV_IN_PROJECT 1
set -x PIPENV_IGNORE_VIRTUALENVS 1
```

#### Python dependencies

##### Install `Python >= 3.7.4`
```bash
sudo apt install python3.7 python3-pip python3.7-dev libpango1.0-0  # or `brew install python3 pango`
```
Optional: You can also use [pyenv](https://github.com/pyenv/pyenv) to install python3.7 if you have trouble installing it with `apt` or `brew`.

##### Install the [`pipenv`](https://github.com/pypa/pipenv) package manager
```bash
python3.7 -m pip install pipenv
```

##### Install the project Python dependencies

(The Python dependencies are defined in `./Pipfile`)
```bash
cd /opt/monadical.homenet
pipenv install --dev
pipenv clean
pipenv lock --clear
pipenv check
```

#### Javascript dependencies (dev machines only):

##### Install `Node >= 12.6.0`

On Ubuntu:
```bash
sudo apt install npm gdal-bin
```
On Mac:
```bash
brew install node gdal
```

##### Install the [`yarn`](https://yarnpkg.com/) package manager
```bash
npm install --global npm
npm install --upgrade --global yarn
```

##### Install the project JS dependencies

(The JS dependencies are defined in `./pennydjango/js/package.json`)
```bash
cd /opt/monadical.homenet/pennydjango/js
yarn install
```

---

### 2. Setup the system environment

#### Point `homenet.l` domain traffic to localhost

Add this line to your `/etc/hosts` file (`sudo` is required to edit it):
```
127.0.0.1   homenet.l
```


#### Install supervisord

Supervisord is used to manage starting and stopping nginx, postgresql, and any other background services.

On Ubuntu:
```bash
sudo apt install supervisor
systemctl enable supervisor
```

On Mac:
```bash
brew install supervisor
brew services start supervisor
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

# Postgresl is managed by supervisord, so we dont want it being started at boot
systemctl stop postgresql
systemctl disable postgresql
```

On macOS:
```bash
brew install postgresql
brew link --overwrite --force postgresql

# Postgresl is managed by supervisord, so we dont want it being started at boot
brew services stop postgresql
```

#### Instantiate the pennybags database
```bash
cd /opt/monadical.homenet

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
cd /opt/monadical.homenet

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
systemctl stop nginx
systemctl disable nginx
```

On macOS:
```bash
brew install nginx
brew services stop nginx
```

#### Generate a self-signed SSL certificate
```bash
cd /opt/monadical.homenet
./bin/generate_dev_ssl homenet.l openssl
./bin/generate_dev_ssl homenet.zalad.io openssl
# optionally specify mkcert arg instead of openssl if its installed
# https://github.com/FiloSottile/mkcert
```

---

### 5. Run the development server

#### Start Postgresql and Nginx
Background processes are managed by Supervisord, they must be started in order for Django to work.

**First, link the supervisord config to your system supervisord config folder.**

On Ubuntu:
```bash
ln -s /opt/monadical.homenet/etc/supervisor/monadical.homenet.dev.ubuntu.conf /etc/supervisor/conf.d/
```

On macOS:
```bash
mkdir /usr/local/etc/supervisor.d
ln -s /opt/monadical.homenet/etc/supervisor/monadical.homenet.dev.ubuntu.conf /usr/local/etc/supervisor.d/
```

**Then start supervisord and confirm the background tasks have been started succesfully.**
```bash
supervisorctl reread
supervisorctl update
supervisorctl status
```
Should output something like:
```
monadical.homenet:nginx          RUNNING   pid 28518, uptime 0:25:32
monadical.homenet:django         RUNNING   pid 28517, uptime 0:25:32
monadical.homenet:postgres       RUNNING   pid 28516, uptime 0:25:32
```

If you encounter any problems, you can check the logs here:  
`/opt/monadical.homenet/data/logs/*.log`


#### Start Django Runserver
```bash
cd /opt/monadical.homenet

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
cd /opt/monadical.homenet
source .venv/bin/activate
# or `source .venv/bin/activate.fish`
# or `pipenv shell`
```

### Start/stop/restart Nginx or Postgresql

```bash
cd /opt/monadical.homenet

# make sure supervisord is running first
systemctl start supervisor  # on mac: brew services start supervisor

# then check the status of all services or a specific service
supervisorctl status <service|all>
supervisorctl stop <service|all>
supervisorctl start <service|all>
```

### Inspect logfile output
```bash
cd /opt/monadical.homenet/data/logs
tail -f nginx.err
tail -f nginx.out
tail -f postgres.log
tail -f reloads.log
tail -f django.log
# etc.
```

### Run Migrations
```bash
# first make sure postgresql is running with supervisord

cd /opt/monadical.homenet/pennydjango
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
