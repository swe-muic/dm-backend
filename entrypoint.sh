set -e

python manage.py migrate

exec "$@"
