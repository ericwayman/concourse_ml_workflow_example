#!/bin/sh

set -e # fail fast
set -x # print commands

git clone train_test_tables_repo updated_train_test_tables_repo

cd updated_train_test_tables_repo/
echo "SCHEMA: $SCHEMA\nTRAIN_TABLE: $TRAIN_TABLE\nTEST_TABLE: $TEST_TABLE" > $TABLE_NAME_FILE

git config --global user.email "nobody@concourse.ci"
git config --global user.name "Concourse"

git add .
git commit -m "Added model file $TABLE_NAME_FILE"