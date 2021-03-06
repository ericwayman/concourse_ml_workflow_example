#!/bin/bash

set -e # fail fast
set -x # print commands

git clone push_data_to_db_repo updated_push_data_to_db_repo

cd updated_push_data_to_db_repo/
echo -e "SCHEMA: $SCHEMA\nTRAIN_TABLE: $TRAIN_TABLE\nTEST_TABLE: $TEST_TABLE" > $TABLE_NAME_FILE

git config --global user.email "nobody@concourse.ci"
git config --global user.name "Concourse"

git add .
git commit -m "Added model file $TABLE_NAME_FILE"