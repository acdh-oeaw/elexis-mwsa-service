#!/bin/sh
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
cd /usr/src/app || exit
ssh -Tvvv -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no git@gitlab.com
pip install --upgrade pip setuptools wheel
touch ~/.gitconfig
#pip install "dvc[gs]"==2.0.18
ls -la /usr/src/app/models
ls -la /usr/src/app
ls -la /mwsa
cp -R /usr/src/app/models/* /mwsa
ls -la /mwsa
sleep 5m