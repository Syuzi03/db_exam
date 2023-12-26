DB_NAME="store"
DB_USER="syuzi"
DB_PASSWORD="syuzi123"
DB_OWNER="syuzi"

sudo -u postgres psql -c "DROP USER IF EXISTS $DB_USER;"

sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"

sudo -u postgres psql -c "ALTER DATABASE $DB_NAME OWNER TO $DB_OWNER;"