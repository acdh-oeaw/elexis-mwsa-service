#!/bin/sh
eval $(ssh-agent -s)
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "${GITLAB}" > ~/.ssh/id_rsa
echo "${}"
ls -la ~/.ssh
chmod 700 ~/.ssh/id_rsa
echo "Host gitlab.com\n
      Hostname altssh.gitlab.com\n
      User git\n
      Port 443\n
      PreferredAuthentications publickey\n
      IdentityFile ~/.ssh/id_rsa" >> ~/.ssh/config

ssh -Tvvv -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no git@gitlab.com
cd /usr/src/app || exit
pip install --upgrade pip setuptools wheel
git clone git@gitlab.com:acdh-oeaw/elexis/mwsa-service-generated.git
cd mwsa-service-generated
dvc pull
#touch ~/.gitconfig
#pip install "dvc[gs]"==2.0.18
ls -la /usr/src/app/mwsa-service-generated/models
ls -la /usr/src/app/mwsa-service-generated
ls -la /mwsa
cp -R /usr/src/app/mwsa-service-generated/models/* /mwsa
ls -la /mwsa
sleep 5m