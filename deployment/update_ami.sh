cd /opt/code
sudo git checkout -- package-lock.json
sudo git pull
sudo npm install --unsafe-perm
sudo npm run build-production 