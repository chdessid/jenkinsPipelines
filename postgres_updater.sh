#!/bin/bash

#Updated command that solves the bug. Courtesy: YoussefBoudaya's comment.
"sudo -u postgres -H -- psql -d jenkinsdb -c "SELECT * FROM articles "
