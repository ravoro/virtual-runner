#!/bin/bash
# Script for deploying the latest code in the repo.

# Config values
SECRET_KEY="secret-key"
GOOGLE_MAPS_API_KEY="google-maps-key"
DB_USER="testuser"
DB_PASS="testpass"
DB_NAME="testdb"

# Date variable used for distinguishing files by time between different deploys
DATE="$(date +%Y%m%d-%s)"

# Base project directory
BASE_DIR="/var/www"

# Directory with website content (the directory that will be renewed)
SITE_DIR="${BASE_DIR}/public_html"

# Directory that will store backup of current version of the site
BACKUP_DIR="${BASE_DIR}/backups"

# Directory that will store (trash) the old version of site after deploy
TRASH_DIR="/tmp/virtualrunner-deploy-trash/${DATE}"

# Directory that will temporarily store the new website content as it is being built
TMP_DIR="${BASE_DIR}/public_html_tmp"

# Git repo containing code that will be deployed
GIT_REPO="https://github.com/ravoro/virtual-runner.git"


function ensure_required_dirs_exist() {
    REQUIRED_DIRS="${BACKUP_DIR} ${SITE_DIR} ${BACKUP_DIR}"
    for DIR in ${REQUIRED_DIRS}; do
        if [ ! -d ${DIR} ]; then
            echo "Required directory (${DIR}) does not exist."
            exit
        fi
    done
}


function backup_db() {
    echo -e "\nCreating gz backup of current database ..."
    mysqldump -u ${DB_USER} -h localhost -p${DB_PASS} ${DB_NAME} | gzip -9 > ${BACKUP_DIR}/db-${DATE}.sql.gz
}


function backup_site() {
    echo -e "\nCreating tgz backup of current version of site ..."
    tar czf ${BACKUP_DIR}/public_html-${DATE}.tgz ${SITE_DIR}
}


function fetch_new_code() {
    echo -e "\nFetching latest code from repo ..."
    git clone ${GIT_REPO} --depth 1 ${TMP_DIR}
    /bin/rm -rf ${TMP_DIR}/.git
}


function setup_config() {
    echo -e "\nConfiguring the new code ..."
    cp ${TMP_DIR}/config.example.py ${TMP_DIR}/config.py
    sed -i 'N; s/class ProdConfig.*\n.*pass//' ${TMP_DIR}/config.py
    cat <<EOF >> ${TMP_DIR}/config.py
class ProdConfig(BaseConfig):
    SECRET_KEY = "${SECRET_KEY}"
    GOOGLE_MAPS_API_KEY = "${GOOGLE_MAPS_API_KEY}"
    SQLALCHEMY_DATABASE_URI = "mysql://${DB_USER}:${DB_PASS}@localhost/${DB_NAME}"
    RELEASE_VERSION = "${RELEASE_VERSION}"
EOF
}


function setup_virtualenv() {
    echo -e "\nSetting up virtualenv and fetching requirements ..."
    virtualenv -p python3 ${TMP_DIR}/venv
    source ${TMP_DIR}/venv/bin/activate
    pip install -r ${TMP_DIR}/requirements.txt
    deactivate
}


function migrate_db() {
    echo -e "\nMigrating any db changes ..."
    cd ${TMP_DIR}
    ./scripts/migrate.sh wsgi.py upgrade
    cd ${BASE_DIR}
}


function trash_current_site() {
    echo -e "\nTrashing current version of the site ..."
    mkdir -p ${TRASH_DIR}
    mv ${SITE_DIR} ${TRASH_DIR}
}


function enable_new_site() {
    echo -e "\nEnabling new version of the website ..."
    mv ${TMP_DIR} ${SITE_DIR}
}


function restart_apache() {
    # If running in embedded mode (instead of daemon), need to restart apache to reflect code changes
    # https://modwsgi.readthedocs.io/en/develop/user-guides/reloading-source-code.html
    echo -e "\nRestarting apache ..."
    service apache2 restart
}


ensure_required_dirs_exist
cd ${BASE_DIR}
backup_db
backup_site
fetch_new_code
setup_config
setup_virtualenv
migrate_db
trash_current_site
enable_new_site
restart_apache
echo -e "\nDeployment done!"
