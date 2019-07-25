# pennybags
Super secret real-estate project...

## Project Quickstart

### 0. Clone the repository

Make sure to clone the repo into the `/opt` directory:
```bash
# Make sure to clone with ssh (not https)
git clone git@github.com:pirate/pennybags.git /opt/pennybags
```
If you clone it elsewhere instead, make sure to symlink `/opt/pennybags` to the repo location:
```bash
ln -s /path/to/repo/pennybags /opt/pennybags
```

### 1. Install the dependencies

#### Python dependencies

Install Python >=3.7.4:
```bash
sudo apt install python3.7 python3-pip python3.7-dev  # or `brew install python3`
```
Optional: You can also use [pyenv](https://github.com/pyenv/pyenv) to install python3.7 if you have trouble installing it with `apt` or `brew`.

Install [`pipenv`](https://github.com/pypa/pipenv):
```bash
python3.7 -m pip install --user pipenv
```

Install the Python dependencies defined in `./Pipfile`:
```bash
cd /opt/pennybags
pipenv install
```

#### Javascript dependencies (dev machines only):

Install [`yarn`](https://yarnpkg.com/):
```bash
sudo apt install npm gdal-bin   # or `brew install node gdal`
npm install -g npm
npm install --upgrade --global yarn
```

Then install the JS dependencies defined in `./pennydjango/js/package.json`:
```bash
cd /opt/pennybags/pennydjango/js
yarn install
```

### 2. Setup the system environment

#### Point homenet.l domain to localhost

Add this line to your `/etc/hosts` file:
```
127.0.0.1   homenet.l
```

#### Make project JS and Python binaries runnable

Add these lines to your `~/.bashrc` or `~/.bash_profile` file:
```bash
PATH=./node_modules/.bin:$PATH   # for fish: `set -x ./node_modules/.bin $PATH`
PIPENV_VENV_IN_PROJECT=1         # for fish: `set -x PIPENV_VENV_IN_PROJECT 1`
```

If you're using Fish, add these lines to `~/.config/fish/config.fish` instead:
```fish
set -x ./node_modules/.bin $PATH
set -x PIPENV_VENV_IN_PROJECT 1
```

#### Install supervisord
```bash
sudo apt install supervisor   # or `brew install supervisor`
```

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
psql -c "CREATE USER penny WITH PASSWORD 'penny';" postgres
psql -c "CREATE DATABASE penny OWNER penny;" postgres
psql -c "GRANT ALL PRIVILEGES ON DATABASE penny TO penny;" postgres
psql -c "ALTER USER penny CREATEDB;" postgres
```

#### Run the initial migrations
```bash
# Run the initial db migrations
./.venv/bin/python ./pennydjango/manage.py migrate
```

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

#### Install a self-signed SSL certificate
```bash
cd /opt/pennybags/data/certs
./generate.sh
```

### 5. Run the development server

```bash
cd /opt/pennybags

# start nginx/postgresql/etc for your environment using supervisord
# <file> can be one of: mac-dev.conf, ubuntu-dev.conf, or ubuntu-prod.conf
supervisord -c etc/supervisor/<file>

# Start the django runserver
./manage.py runserver
```

✅ Then open [https://homenet.l](https://homenet.l) in your browser.

*Note: It will warn about using an invalid/self-signed certificate.*  
Click "Advanced" and then "Visit site" to bypass the warning, or install a trusted local development certificate with [mkcert](https://github.com/FiloSottile/mkcert) to get rid of it entirely:
```bash
cd /opt/pennybags/data/certs
./generate.sh homenet.l
```

Alternatively, open [http://127.0.0.1:8000](http://127.0.0.1:8000) to access runserver directly without using nginx (always use nginx if possible though).
