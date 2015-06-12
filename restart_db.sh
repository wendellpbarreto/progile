#!/bin/bash
#
#-----------------------------------
# @autor: Wendell P. Barreto
# @email: wendellp.barreto@gmail.com
# @project: progile
# @doc: restart_db.sh
# ----------------------------------


while true; do
    read -p "Are you using Linux (y or n)? " yn
    case $yn in
        [Yy]* )
        	sudo -u postgres psql -c 'DROP DATABASE progile'
			sudo -u postgres psql -c 'CREATE DATABASE progile'
			sudo -u postgres psql -c 'CREATE USER progile'
			sudo -u postgres psql -c 'GRANT ALL PRIVILEGES ON DATABASE progile TO progile'
			# sudo -u postgres psql -d progile -c 'CREATE EXTENSION hstore' 

			break;;
        [Nn]* ) 
			psql -c 'DROP DATABASE progile'
			psql -c 'CREATE DATABASE progile'
			psql -c 'CREATE USER progile'
			psql -c 'GRANT ALL PRIVILEGES ON DATABASE progile TO progile'
			# psql -d progile -c 'CREATE EXTENSION hstore'

			break;;
        * ) echo "Please answer yes or no.";;
    esac
done

python manage.py syncdb
python manage.py collectstatic --noinput