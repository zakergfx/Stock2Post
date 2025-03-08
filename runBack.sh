# vars
pwd=$(pwd)
prodBackEnv="$pwd/prod_env/back_env"
testBackEnv="$pwd/test_env/back_env"

# collect static
echo "collect static"
cd "$testBackEnv"
source venv/bin/activate
python3 manage.py collectstatic --no-input

# copie vers prod_env local
echo "suppression data backend actuel"
rm -rf "$prodBackEnv/image/backend"


# changement des vars d'environnement vers prod
echo "changement de .env"
echo "$testBackEnv/.env"
mv "$testBackEnv/.env" "$testBackEnv/.env.test"
mv "$testBackEnv/.env.prod" "$testBackEnv/.env"

echo "copie du backend vers prod local"
cp -r "$testBackEnv/" "$prodBackEnv/image/backend"

# remise des variables d'env en mode test
echo "remise des .env"
mv "$testBackEnv/.env" "$testBackEnv/.env.prod"
mv "$testBackEnv/.env.test" "$testBackEnv/.env"

echo "creation pip freeze, (copie db) et suppression venv"
pip freeze > "$prodBackEnv/image/requirements.txt"
#rm -rf "$prodBackEnv/image/backend/db.sqlite3"
rm -rf "$prodBackEnv/image/backend/venv"

# copie vers vps
echo "copie vers vps"
ssh root@vps.loicktest.be "rm -rf back_env"
scp -r "$prodBackEnv" root@vps.loicktest.be:/root/autoscout_fb_sync
# run
echo "lancement docker-compose"
ssh root@vps.loicktest.be "cd /root/autoscout_fb_sync/back_env && chmod 777 -R run.sh && ./run.sh"
