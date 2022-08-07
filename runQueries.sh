#!/bin/bash
psql -U postgres -d jaridaa_dev -c "update articles set sitename = 'siasat' where urls like '%siasat.com%' "
