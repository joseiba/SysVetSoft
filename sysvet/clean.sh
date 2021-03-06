# Eliminar todas los migrations
echo -e "Eliminado migrations...\n" 
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# Eliminar cache migrations
echo -e "Eliminando pycache...\n"
find . -path "*/__pycache__/*.pyc" -not -name "__init__.py" -delete

# Eliminar base de datos
#echo -e "Eliminando base de datos postgres ..."
#sudo -u postgres psql -c "DROP DATABASE sysvetdb;"
#Creando base de datos
#echo -e "\nCreando base de datos postgrest labsoft..."
#sudo -u postgres psql -c "CREATE DATABASE sysvetdb;"
#Creando Migraciones 
#echo -e "\nCreando migraciones..."
#python manage.py makemigrations
#python manage.py migrate

#creando user
#echo -e "\nCreando Super usuario..."
#python manage.py createsuperuser