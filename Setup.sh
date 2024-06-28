git pull --rebase
pip3 install -r requirements.txt

echo "Base Directory"
read baseDirectory

echo "Google Site Key"
read googleSiteKey

echo "Google Secret Key"
read googleSecretKey

python3 credentials.py $baseDirectory $googleSiteKey $googleSecretKey