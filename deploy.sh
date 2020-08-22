#!/bin/bash
docker stop "loli-princess"
docker rm "loli-princess"
docker run -d --restart unless-stopped --name="loli-princess" -e TZ="Europe/London" -v '/mnt/appdata/loli-princess':'/app/data':'rw' 'skippythesnake/loli-princess'