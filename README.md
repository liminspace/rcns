# Robot City Navigation System

Tested on Ubuntu 18.04 with Docker 18.09.7 and Docker-compose 1.24.0

Set up and run:
```bash
$ cp .env.develop.sample .env
$ cp deploy/local_settings.py.develop.sample conf/local_settings.py
$ make refresh
$ make test
$ make shell
> python src/manage.py createsuperuser
<Ctrl+D>
$ make
```

Add `127.0.0.1  navsys.local` in your `/etc/hosts` file.

Open http://navsys.local:8000/
