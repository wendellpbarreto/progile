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
        	sudo -u postgres psql -c 'DROP DATABASE development'
			sudo -u postgres psql -c 'CREATE DATABASE development'
			sudo -u postgres psql -c 'CREATE USER progile'
			sudo -u postgres psql -c 'GRANT ALL PRIVILEGES ON DATABASE development TO progile'
			# sudo -u postgres psql -d development -c 'CREATE EXTENSION hstore' 

			break;;
        [Nn]* ) 
			psql -c 'DROP DATABASE development'
			psql -c 'CREATE DATABASE development'
			psql -c 'CREATE USER progile'
			psql -c 'GRANT ALL PRIVILEGES ON DATABASE development TO progile'
			# psql -d development -c 'CREATE EXTENSION hstore'

			break;;
        * ) echo "Please answer yes or no.";;
    esac
done

python manage.py syncdb
python manage.py collectstatic --noinput