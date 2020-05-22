# SQL Examples

## Usage
On macOS install the postgres app then install psycopg2 with the xcode command line tools from [here](https://developer.apple.com/download/more/) so you don't need to download multiple gigabytes of xcode.

Then run:
`
psql -U <username>
default pass is root
then proceed to create a database with 
CREATE DATABASE <name>;
`

To disconnect all other sessions use:
`
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE datname = current_database()
  AND pid <> pg_backend_pid();
`

The file credit_card_complaint_examples/psycopg.py lists all major SQL interactions.