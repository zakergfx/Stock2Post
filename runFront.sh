pwd=$(pwd)
# vars
testFrontEnv="$pwd/test_env/front_env"
prodFrontEnv="$pwd/prod_env/front_env"
# changement des vars d'environnement vers prod
mv "$testFrontEnv/.env" "$testFrontEnv/.env.test"
mv "$testFrontEnv/.env.prod" "$testFrontEnv/.env"
# build
cd "$testFrontEnv"
npm run build
# copie du code vers l'env de prod local
rm -rf "$prodFrontEnv/image/frontend"
cp -r "$testFrontEnv/build" "$prodFrontEnv/image/frontend"
# remise des variables d'env en mode test
mv "$testFrontEnv/.env" "$testFrontEnv/.env.prod"
mv "$testFrontEnv/.env.test" "$testFrontEnv/.env"
# copie build vers la prod
ssh root@vps.loicktest.be "rm -rf /root/autoscout_fb_sync/front_env"
scp -r $prodFrontEnv root@vps.loicktest.be:/root/autoscout_fb_sync
# run
ssh root@vps.loicktest.be "cd /root/autoscout_fb_sync/front_env && chmod 777 run.sh && ./run.sh"
