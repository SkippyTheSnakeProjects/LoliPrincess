#!/bin/bash
docker stop "Loli-Princess"
docker rm "Loli-Princess"
docker run -d --restart unless-stopped --name="Loli-Princess" -e TZ="Europe/London" -v '/mnt/appdata/Loli-Princess':'/app/data':'rw' 'skippythesnake/Loli-Princess'