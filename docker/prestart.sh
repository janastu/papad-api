#!/usr/bin/env bash

cat << EOF > /app/config.json
{
    "db": {
        "host": "db",
        "name": "papad"
    },
    "server": {
        "host": "0.0.0.0",
        "port": 9000
    }
}
EOF

python /app/init-db.py
