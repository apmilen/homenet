"""
Functions for managing configuration and sytem setup.

Do not import any django code in this file, if you must, inline the imports
in the function, not at the top!!!
"""

import os
import sys
import pwd
import getpass

from datetime import datetime
from typing import Optional, Iterable, Dict, Union, Set, IO, Callable, List, Any

import psutil
import shutil
import subprocess

from dotenv import dotenv_values


PLACEHOLDER_FOR_SECRET = 'set-this-value-in-secrets.env'
COMMIT_ID_LENGTH = 9


class AttributeDict(dict): 
    """Helper to allow accessing dict values via Example.key or Example['key']"""

    def __getattr__(self, attr: str) -> Any:
        return dict.__getitem__(self, attr)

    def __setattr__(self, attr: str, value: Any) -> None:
        return dict.__setitem__(self, attr, value)


class PrettyTerm:
    """Helper for printing and formatting pretty terminal output"""

    ANSI_COLOR = '\033[{fg};{bg}m'
    COLORS = {
        'RESET':    ANSI_COLOR.format(fg='00', bg='00'),
        'RED':      ANSI_COLOR.format(fg='01', bg='31'),
        'GREEN':    ANSI_COLOR.format(fg='01', bg='32'),
        'YELLOW':   ANSI_COLOR.format(fg='01', bg='33'),
        'BLUE':     ANSI_COLOR.format(fg='01', bg='34'),
        'PURPLE':   ANSI_COLOR.format(fg='01', bg='35'),
        'CYAN':     ANSI_COLOR.format(fg='01', bg='36'),
        'WHITE':    ANSI_COLOR.format(fg='01', bg='37'),
    }

    color: bool
    truncate: bool
    fd: IO

    def __init__(self, color: bool=False, truncate: bool=False, fd: IO=sys.stdout):
        self.color = color
        self.truncate = truncate
        self.fd = fd

    @classmethod
    def num_control_chars(cls, string: str) -> int:
        control_chars = 0
        for color in cls.COLORS.values():
            control_chars += (string.count(color) * len(color))
        return control_chars

    @classmethod
    def truncated(cls, string: str) -> str:
        invisible_chars = cls.num_control_chars(string)
        max_columns = shutil.get_terminal_size((160, 10)).columns
        return string[:max_columns + invisible_chars]

    @classmethod
    def colored(cls, string: str, color: Optional[str]) -> str:
        if color is None:
            return string
        return f'{cls.COLORS[color.upper()]}{string}{cls.COLORS["RESET"]}'

    def format(self, *string, color: Optional[str]=None) -> str:
        out_str = ' '.join(str(s) for s in string)

        if self.color:
            if color:
                out_str = self.colored(out_str, color)
            else:
                out_str = out_str.format(**self.COLORS)
        else:
            out_str = out_str.format(**{key: '' for key in self.COLORS.keys()})

        if self.truncate:
            out_str = self.truncated(out_str)

        return out_str

    def write(self, string: str) -> None:
        self.fd.write(self.format(string))

### System Environment Getters

def get_current_django_command() -> Optional[str]:
    """currently running manage.py command, e.g. runserver, test, migrate, etc"""

    if len(sys.argv) > 1:
        return sys.argv[1].lower()
    return None

def get_current_hostname(fqdn=False) -> str:
    """get short system hostname, e.g. squash, prod, jose-laptop, etc."""
    hostname = os.uname()[1]
    if fqdn:
        if '.' not in hostname:
            print('[!] Warning, tried to get host FQDN, but got short hostname')
        return hostname
    return hostname.split('.', 1)[0]

def get_current_user() -> str:
    """get user running the current process, works on mac, linux, bsd"""
    
    # different systems propagate ownership from parent->child in different ways
    # this handles all the cases and correctly gets only the child proccess user
    return (
        pwd.getpwuid(os.getuid()).pw_name
        or getpass.getuser()
        or os.getlogin()
    )

def get_current_pid() -> int:
    return os.getpid()

def get_current_system_time() -> datetime:
    return datetime.now()

def get_python_implementation() -> str:
    return sys.implementation.name

def get_active_git_branch(repo_dir: str) -> str:
    """e.g. master"""
    try:
        with open(os.path.join(repo_dir, '.git', 'HEAD'), 'r') as f:
            return f.read().strip().replace('ref: refs/heads/', '')
    except Exception:
        return 'unknown'

def get_active_git_commit(repo_dir: str, head: str) -> str:
    """e.g. 47df4ed31"""

    try:
        with open(os.path.join(repo_dir, '.git', 'refs', 'heads', head), 'r') as f:
            return f.read().strip()[:COMMIT_ID_LENGTH]
    except Exception:
        return 'unknown'


### Environment Variable and Config Management

EnvSettingTypes = (str, bool, int, float, list)
EnvSetting = Union[str, bool, int, float, list]

def get_env_value(env: dict, key: str, default: EnvSetting=None):
    """get & cast a given value from a dictionary, or return the default"""
    if key in env:
        value = env[key]
    else:
        return default

    ExpectedType = type(default)
    assert ExpectedType in EnvSettingTypes, (
        f'Tried to set unsupported environemnt variable {key} to {ExpectedType}')

    def raise_typerror():
        raise TypeError(f'Got bad environment variable {key}={value}'
                        f' (expected {ExpectedType})')

    if ExpectedType is str:
        return value
    elif ExpectedType is bool:
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        else:
            raise_typerror()
    elif ExpectedType is int:
        if value.isdigit():
            return int(value)
        else:
            raise_typerror()
    elif ExpectedType is float:
        try:
            return float(value)
        except ValueError:
            raise_typerror()
    elif ExpectedType is list:
        return value.split(',')


def unique_env_settings(env: dict, defaults: dict) -> dict:
    """return all the new valid env settings in a dictionary of settings"""

    existing_settings = {
        setting_name: val
        for setting_name, val in (defaults or env).items()
        if not setting_name.startswith('_') and setting_name.isupper()
    }
    if not defaults:
        return existing_settings

    new_settings = {}
    for setting_name, default_val in existing_settings.items():
        loaded_val = get_env_value(env, setting_name, default_val)

        if loaded_val != default_val:
            new_settings[setting_name] = loaded_val

    return new_settings


def load_env_settings(dotenv_path: str=None, env: dict=None, defaults: dict=None) -> dict:
    """load settings from a dotenv file or os.environ by default"""
    assert not (dotenv_path and env), 'Only pass env or dotenv_path, not both'

    env_values = (env or {}).copy()
    defaults = (defaults or {}).copy()
    if dotenv_path:
        env_values = dotenv_values(dotenv_path=dotenv_path)

    return unique_env_settings(env_values, defaults)


def get_setting_source(SETTINGS_SOURCES: Dict[str, Dict[str, Any]], key: str) -> str:
    """determine which file a specific setting was loaded from"""
    for source_name, settings in reversed(list(SETTINGS_SOURCES.items())):
        if key in settings:
            return source_name

    source_names = ', '.join(name for name in SETTINGS_SOURCES.keys())
    raise ValueError(f'Setting {key} is not in any of {source_names})')

def get_secret_setting_names(settings: dict) -> Set[str]:
    """guess the setting names that likely contain sensitive values"""
    excluded = {
        'ENV_SECRETS',
        'ENV_SECRETS_FILE',
        'AUTH_PASSWORD_VALIDATORS',
        'PASSWORD_RESET_TIMEOUT_DAYS',
        'ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE',
        'PLACEHOLDER_FOR_SECRET',
    }
    return {
        key for key in settings.keys()
        if any(s in key for s in ('API_KEY', 'SECRET', 'PASSWORD'))
        and key not in excluded
    } | {
        key for key, value in settings['SETTINGS_DEFAULTS'].items()
        if value == PLACEHOLDER_FOR_SECRET
    }

### Invariant and Assertion Checkers

def check_system_invariants(settings: dict):
    """Check basic system setup and throw if there is any misconfiguration"""

    s = AttributeDict(settings)

    assert s.SERVER_ENV in s.ALLOWED_ENVS, (
        f'SERVER_ENV={s.SERVER_ENV} is not one of the allowed values: '
        f'{",".join(s.ALLOWED_ENVS)}')

    assert sys.version_info >= s.MIN_PYTHON_VERSION, (
        f'Installed Python version {sys.version_info} is not high enough '
        f' (you must install Python >={s.MIN_PYTHON_VERSION.join(".")})'
    )

    assert sys.implementation.name in s.ALLOWED_PYTHON_IMPLEMENTATIONS, (
        f'The active Python implementation type "{sys.implementation.name}" '
        f'is not supported (must be one of {s.ALLOWED_PYTHON_IMPLEMENTATIONS})'
    )

    assert os.path.realpath(s.REPO_DIR) == os.path.realpath(s.ALLOWED_REPO_DIR), (
        'Project directory was not found in the expected location. '
        f'(you must move or symlink {s.REPO_DIR} to {s.ALLOWED_REPO_DIR})'
    )

    try:
        with open('/etc/passwd', 'r') as f:
            f.read()
        if not s.ALLOW_ROOT:
            raise PermissionError(f'Django should never be run as root ({s.DJANGO_USER} can read /etc/passwd)!')
    except PermissionError:
        pass

    # running as root even once will corrupt the permissions on all the DATA_DIRS
    if s.DJANGO_USER == 'root':
        if not s.ALLOW_ROOT:
            raise PermissionError('Django should never be run as root!')
        else:
            print(
                '[!] Warning: Running Django as root because ALLOW_ROOT=True. '
                '(You must manually fix the data folder permissions after '
                'quitting in order to be able to run it as your normal user).'
            )

    # python -O strips asserts from our code, but we use them for critical logic
    try:
        assert not __debug__
        print('Never run grater with python -O, asserts are needed in production.')
        raise SystemExit(1)
    except AssertionError:
        pass

    if hasattr(sys.stderr, 'encoding'):
        # Set these in ~/.bashrc or ~/.config/fish/config.fish to fix encoding:
        #   LANG='en_US.UTF-8',
        #   LC_ALL='en_US.UTF-8',
        #   PYTHONIOENCODING='UTF-8'
        assert sys.stderr.encoding == sys.stdout.encoding == 'UTF-8', (
            f'Bad shell encoding setting "{sys.stdout.encoding}". '
            'System, Shell, and Python system locales must be set to '
            '(uppercase) "UTF-8" to run properly.'
        )


def check_prod_safety(settings: dict):
    s = AttributeDict(settings)

    # DEBUG features and permissions mistakes must be forbidden on production boxes
    if s.PROD_SAFETY_CHECK:
        assert not s.DEBUG, 'DEBUG=True is never allowed on prod and beta!'
        assert s.SERVER_ENV == 'PROD', 'Prod must always be run with SERVER_ENV=PROD'
        assert s.DJANGO_USER == 'www-data', 'Django can only be run as user www-data'
        assert s.DEFAULT_HTTP_PROTOCOL == 'https', 'https is required on prod servers'
        assert s.TIME_ZONE == 'UTC', 'Prod servers must always be set to UTC timezone'

        # tests can pollute the data dir and use lots of CPU / Memory
        # only disable this check if you're 100% confident it's safe and have a
        # very good reason to run tests on production. remember to try beta first
        assert not s.IS_TESTING, 'Tests should not be run on prod machines'
    elif s.SERVER_ENV == 'PROD':
        # can be safely ignored when testing PROD mode on dev machines
        print(
            f'[!] Warning: Running with SERVER_ENV=PROD but '
            f'PROD_SAFETY_CHECK is set to False! '
            '(dangerous if server is publicly accessible)'
        )


def check_http_settings(settings: dict):
    """check the server url scheme, host, and port config"""
    s = AttributeDict(settings)

    baseurl_scheme, baseurl_host, *_ = s.BASE_URL.split('://', 1) + ['']
    baseurl_domain, baseurl_port, *_ = baseurl_host.split(':', 1) + ['']

    # check scheme
    assert baseurl_scheme in ('http', 'https'), (
        'BASE_URL scheme must be http or https')
    assert baseurl_scheme == s.DEFAULT_HTTP_PROTOCOL, (
        'BASE_URL scheme must match DEFAULT_HTTP_PROTOCOL')
    if baseurl_scheme == 'http':
        assert not (s.SESSION_COOKIE_SECURE or s.CSRF_COOKIE_SECURE), (
            'SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE must be False '
            'when using http (to fix, set them to False in env/secrets.env)'
        )
    elif baseurl_scheme == 'https':
        assert s.SESSION_COOKIE_SECURE and s.CSRF_COOKIE_SECURE, (
            'SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE must be True '
            'when using https (to fix, set them to False in env/secrets.env)'
        )

    # check host
    assert baseurl_domain == s.DEFAULT_HOST, (
        'BASE_URL must use the DEFAULT_HOST for links on the site to work')
    assert baseurl_domain.replace('.', '').replace('-', '').isalnum(), (
        'DEFAULT_HOST must be a valid hostname or IP address e.g. '
        '127.0.0.1 or example.zalad.io (without scheme, port, or path)'
    )
    assert baseurl_domain in s.ALLOWED_HOSTS, (
        'DEFAULT_HOST must be in ALLOWED_HOSTS for the site to be accessible')

    # check port
    assert isinstance(s.DEFAULT_HTTP_PORT, int)
    if s.DEFAULT_HTTP_PORT == 80:
        assert s.DEFAULT_HTTP_PROTOCOL == 'http', (
            'DEFAULT_HTTP_PROTOCOL must be http when DEFAULT_HTTP_PORT=80')
    elif s.DEFAULT_HTTP_PORT == 443:
        assert s.DEFAULT_HTTP_PROTOCOL == 'https', (
            'DEFAULT_HTTP_PROTOCOL must be https when DEFAULT_HTTP_PORT=443')
    else:
        assert s.DEFAULT_HTTP_PROTOCOL in ('http', 'https')
        assert 65535 > s.DEFAULT_HTTP_PORT > 1024

    if baseurl_port:
        assert baseurl_port.isdigit()
        assert int(baseurl_port) == s.DEFAULT_HTTP_PORT, 'port in '
    else:
        assert s.DEFAULT_HTTP_PORT in (80, 443)

    # check BASE_URL
    assert not s.BASE_URL.endswith('/'), (
        'BASE_URL should not have a trailing slash')
    if s.DEFAULT_HTTP_PORT in (80, 443):
        assert ':' not in s.BASE_URL.split('://')[1], (
            'Port should not be included in BASE_URL when using '
            'https on 443 or http on 80')
    else:
        assert s.BASE_URL.endswith(f':{s.DEFAULT_HTTP_PORT}'), (
            ':port must be included in BASE_URL when using a non-standard port')



def check_secure_settings(settings: dict):
    """Check that all secure settings are defined safely in secrets.env"""
    
    s = AttributeDict(settings)

    # Some config should not be in git and can only be passed via secrets or os.env
    SECURE_SETTINGS_SOURCES = (s.ENV_SECRETS_FILE, 'os.environ')
    SECURE_SETTINGS = get_secret_setting_names(settings=settings)

    # make sure all security-sensitive settings are coming from safe sources
    for name in SECURE_SETTINGS:
        value = settings.get(name, '')
        defined_in = get_setting_source(s.SETTINGS_SOURCES, name)

        # Do not comment this out, instead move the secret into secrets.env
        # and PM the secret to other devs to update their secrets.env
        try:
            assert defined_in in SECURE_SETTINGS_SOURCES, (
                'Security-sensitive settings must only be defined in secrets.env!\n'
                f'    Got:       {name}={value} in {defined_in}\n'
                f'    Expected:  {name}={value} in secrets.env'
            )
            # make sure settings are not defaults on prod
            assert value and value != PLACEHOLDER_FOR_SECRET, (
                'Required API key or secret was not defined in secrets.env or os.environ\n'
                f'    Got:       {name}={value} from {defined_in}'
                f'    Expected:  {name}=somesecretvalue or {name}=UNUSED in secrets.env'
            )
        except AssertionError as e:
            if s.SERVER_ENV == 'PROD' or s.PROD_SAFETY_CHECK:
                raise e
            elif not s.DEBUG:
                print(f'[!] Warning: {e}')

    # if s.IS_TESTING:
    #     assert s.REDIS_DB != s.SETTINGS_DEFAULTS['REDIS_DB'], (
    #         'Tests must be run with a different redis db than the main redis')


def get_django_status_line(settings: dict, pretty: bool=False) -> str:
    """the status line with process info printed every time django starts"""
    # > ./manage.py check; ⚙️ DEV 👾 True 📂 ../data 🗄 127.0.0.1/penny ...
    
    s = AttributeDict(settings)
    term = PrettyTerm(color=pretty, truncate=pretty)

    cli_arguments = " ".join(sys.argv[1:])


    mng_str = term.format('> ./manage.py ', color='yellow')
    cmd_str = term.format(cli_arguments, color='blue')
    env_str = term.format(s.SERVER_ENV, color='green')
    debug_str = term.format(s.DEBUG, color=('green', 'red')[s.DEBUG])
    pytype_str = " PYPY" if s.PY_TYPE == "pypy" else ""
    path_str = s.DATA_DIR.replace(s.REPO_DIR + "/", "../")

    icons = {
        'env':      '⚙️  ',
        'debug':    '👾 ',
        'data':     '📂 ',
        'db':       '🗄  ',
        'git':      '#️⃣  ',
        'usr':      '👤 ',
        'pid':      '🆔 ',
        'ts':       '🕐 ',
    }
    def section(name, value):
        if pretty:
            return f'{icons[name]}{value} '
        return f'{name}={value} '

    status_line = ''.join((
        mng_str,
        cmd_str,
        '; ',
        section("env",      env_str),
        section("debug",    f'{debug_str}{pytype_str}'),
        section("data",     path_str),
        section("db",       f'{s.POSTGRES_HOST}/{s.POSTGRES_DB}'),
        section("git",      f'{s.GIT_SHA} ({s.GIT_HEAD})'),
        section("usr",      s.DJANGO_USER),
        section("pid",      s.PID),
        section("ts",       int(s.START_TIME.timestamp())),
    ))

    return term.format(status_line)


def log_django_startup(settings: dict) -> None:
    """print and log the django status line to stdout and the reloads log"""
    
    s = AttributeDict(settings)

    # Log status line to reloads log
    with open(s.RELOADS_LOGS, 'a+') as f:
        f.write(f'{s.STATUS_LINE}\n')

    # Log status line to stdout
    if s.CLI_COLOR:
        print(s.PRETTY_STATUS_LINE)
    else:
        print(s.STATUS_LINE)


### File and folder management

def mkchown(path: str, mode: str, user: str, group: str):
    """create and chown a directory to make sure a user can write to it"""

    abilities = {'r':'read', 'w': 'write to'}
    assert mode in abilities
    try:
        if os.path.exists(path) and not os.path.isdir(path):
            raise FileExistsError

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            if sys.platform == 'darwin':
                # on mac, just chown as the user
                shutil.chown(path, user=user)
            else:
                # on linux, chown as user:group
                shutil.chown(path, user=user, group=group)

        if mode == 'r':
            os.listdir(path)
        else:
            os.listdir(path)
            testfile = os.path.join(path, '.django_write_test')
            with open(testfile, 'w') as f:
                f.write('test')
            os.remove(testfile)
    except FileExistsError:
        # sshfs folders can trigger a FileExistsError if permissions
        # are not set up to allow user to access fuse filesystems
        # make sure allow_other is passed to sshfs and www-data is in "fuse" group
        print(
            f'[!] Existing file conflicts with data dir path: {path}\n'
            '(check for incorrect permissions, or remove it and try again)'
        )
        raise
    except PermissionError:
        print(
            f'[!] Django user "{user}" is not able to {abilities[mode]} '
            f'the data dir: {path}'
        )
        raise


def check_data_folders(settings: dict):
    """set the proper permissions on all the data folders used by django"""

    s = AttributeDict(settings)

    # Required permissions for each folder, r=read only, w=read and write
    PROJECT_DIRS = {
        s.REPO_DIR: 'r',
        s.DATA_DIR: 'r',
        s.LOGS_DIR: 'w',
        s.STATIC_ROOT: 'r',
        s.MEDIA_ROOT: 'w',
    }

    for path, mode in PROJECT_DIRS.items():
        mkchown(
            path,
            mode=mode,
            user=s.DJANGO_USER,
            group=s.DJANGO_USER,
        )

    return PROJECT_DIRS


### Process Management

def ps_aux(pattern: Optional[str]=None) -> List[str]:
    """find all processes matching a given str pattern"""

    return [
        line for line in subprocess.Popen(
            ['ps', 'axw'],
            stdout=subprocess.PIPE,
        ).stdout
        if (pattern and pattern in line) or not pattern
    ]


def kill(pid_lines: list) -> None:
    """for each process line produced by ps_aux, kill the process"""
    
    for line in pid_lines:
        pid = line.decode().strip().split()[0]
        assert pid.isdigit(), 'Found invalid text when expecting PID'
        subprocess.Popen(['kill', pid])


def matching_pids(match_func: Callable[[psutil.Process, str], bool]) -> Iterable[int]:
    """yield all pids that match using a given function match function"""
    for proc in psutil.process_iter():      # python api for ps -aux
        with proc.oneshot():
            try:
                cmd = proc.cmdline()
            except Exception:
                continue

            # ['python', './manage.py', 'table_heartbeat', '6a7d6689']
            if len(cmd) >= 3 and match_func(proc, cmd):
                yield proc.pid


def find_django_process(mgmt_command: str,
                        *command_args,
                        exact=False,
                        exclude_pid=None) -> Optional[int]:
    """find the pid for a given management command thats running"""

    def pid_matches(proc: psutil.Process, cmd: str) -> bool:
        if not cmd[2] == mgmt_command:
            return False

        if exact:
            return cmd[3:] == command_args
        
        return all(arg in cmd for arg, cmd in zip(command_args, cmd[3:]))

    pids = list(matching_pids(pid_matches))
    if pids and pids[0] != exclude_pid:
        return pids[0]

    return None


def stop_process(pid: int, block: bool=True) -> bool:
    """stop the process identified by pid, optionally block until it's dead"""
    
    if not pid:
        return False

    proc = psutil.Process(pid)
    proc.terminate()
    if block:
        proc.wait()
    return True


def DOUBLE_FORK():
    """
    Perform a UNIX double-fork to detach, and re attach process to
    init so it's not a child of web worker
    """
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError as e:
        print("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)

    # decouple from parent environment
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            sys.exit(0)
    except OSError as e:
        print("fork #2 failed: %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)


### Load Management


MAX_LOAD = {
    'PROD': {
        'CPU': 70,
        'Number of Processes': 70,
        'Memory': 75,
        'Disk Space': 95,
    },
    # dev limits are not enforced because we run tons of other programs
    'DEV': {
        'CPU': 1000,
        'Number of Processes': 1000,
        'Memory': 1000,
        'Disk Space': 1000,
    },
}

# All return integer percentages 0 - 100%


def cpu_usage() -> int:
    num_cpus = os.cpu_count() or 1
    load_avg = os.getloadavg()[1]  # get 5min load level of [1min 5min 15min]
    cpu_use_pct = int((load_avg / num_cpus) * 100)
    return cpu_use_pct


def proc_usage() -> int:
    num_procs = len(list(psutil.process_iter()))
    max_procs = 300
    return int((num_procs / max_procs) * 100)


def mem_usage() -> int:
    memory_use_pct = psutil.virtual_memory()._asdict()['percent']
    return int(memory_use_pct)


def disk_usage() -> int:
    disk_use = psutil.disk_usage('/')
    return int((disk_use.used / disk_use.total) * 100)


def io_usage() -> int:
    # TODO
    # io_use = psutil.disk_io_counters()
    # some math here to figure out rate of use / capacity
    raise NotImplementedError()


def net_usage() -> int:
    # TODO
    # net_use = psutil.net_io_counters()
    # some math here to figure out rate of use / capacity
    raise NotImplementedError()


def load_summary() -> dict:
    """Get system load as 0-100 integer percentages of total capacity in use"""
    return {
        'CPU': cpu_usage(),
        'Number of Processes': proc_usage(),
        'Memory': mem_usage(),
        'Disk Space': disk_usage(),
        # 'Disk IO': io_usage(),
        # 'Network IO': net_usage(),
    }
