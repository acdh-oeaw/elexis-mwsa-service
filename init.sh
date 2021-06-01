#!/bin/sh
# This is a comment!
apk update
apk add git
sleep 5m
eval $(ssh-agent -s)
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "${K8S_SECRET_GITLAB}" > ~/.ssh/id_rsa
ls -la ~/.ssh
chmod 700 ~/.ssh/id_rsa
echo "Host gitlab.com\n
      Hostname altssh.gitlab.com\n
      User git\n
      Port 443\n
      PreferredAuthentications publickey\n
      IdentityFile ~/.ssh/id_rsa" >> ~/.ssh/config
cd /builds/acdh-oeaw/elexis/mwsa-service-generated
ssh -Tvvv -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no git@gitlab.com
pip install --upgrade pip setuptools wheel
touch ~/.gitconfig
#pip install "dvc[gs]"==2.0.18
cp -R /builds/acdh-oeaw/elexis/mwsa-service-generated/models/* /mwsa/models