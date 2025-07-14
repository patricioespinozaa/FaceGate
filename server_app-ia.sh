#!/bin/bash
source "$HOME/miniforge3/bin/activate" facegate && \
cd "$HOME/facegate/app-ia" && \
mod_wsgi-express start-server application.wsgi --port 8911 \
      --server-root "$HOME/facegate/apache-app-ia" \
      --access-log --log-to-terminal \
       2>&1 | /usr/bin/cronolog "$HOME/facegate/apache-app-ia/logs/apache.%Y-%m-%d.log"