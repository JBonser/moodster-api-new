#! /usr/bin/env bash

# Let the DB start
sleep 15;
# Run migrations
alembic -x data=true upgrade head