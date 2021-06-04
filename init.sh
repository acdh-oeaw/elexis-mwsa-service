#!/bin/sh
eval $(ssh-agent -s)
mkdir -p ~/.ssh
mkdir -p ~/.creds
chmod 700 ~/.ssh
ls -la ~/.ssh
echo "${GITLAB}" > ~/.ssh/id_rsa
printf '%s\n' "$GOOGLE_APPLICATION_CREDENTIALS" > ~/.creds/gcp.json
#echo "${GOOGLE_APPLICATION_CREDENTIALS}" > ~/.creds/gcp.json
export GOOGLE_APPLICATION_CREDENTIALS="~/.creds/gcp.json"
chmod 700 ~/.ssh/id_rsa
chmod 700 ~/.creds/gcp.json
echo "Host gitlab.com\n
      Hostname altssh.gitlab.com\n
      User git\n
      Port 443\n
      PreferredAuthentications publickey\n
      IdentityFile ~/.ssh/id_rsa" >> ~/.ssh/config

ssh -T -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no git@gitlab.com
cd /usr/src/app || exit
pip install --upgrade pip setuptools wheel
git clone git@gitlab.com:acdh-oeaw/elexis/mwsa-service-generated.git
cd mwsa-service-generated || exit
dvc pull
#touch ~/.gitconfig
#pip install "dvc[gs]"==2.0.18
ls -la /usr/src/app/mwsa-service-generated/models
ls -la /usr/src/app/mwsa-service-generated
ls -la /mwsa
cp -R /usr/src/app/mwsa-service-generated/models/* /mwsa
ls -la /mwsa
