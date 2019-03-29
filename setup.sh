#!/bin/bash/usr

##### Config #####

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VIRTUALENV_DIR="./${SCRIPT_DIR}/venv"

##################

install_dependencies() {
  pip install -r requirements.txt
}

configure_venv() {
  if [ ! -e "${VIRTUALENV_DIR}" ]; then
    echo "Creating virtual python environment in ${VIRTUALENV_DIR}..."
    virtualenv -p python3 venv
    source ./venv/bin/activate
    install_dependencies
  else
    echo "Virtual environment appears to exist already in ${VIRTUALENV_DIR}; skipping creation..."
  fi
}

##### Main #####
configure_venv