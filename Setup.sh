git pull --rebase
pip3 install -r requirements.txt

echo "Credentials.json location"
read credentialsLocation

echo "Google Site Key"
read googleSiteKey

echo "Google Secret Key"
read googleSecretKey

echo "Information Base Directory"
read infoBaseDirectory

python3 credentials.py set $credentialsLocation $googleSiteKey $googleSecretKey $infoBaseDirectory
python3 googleEmail.py