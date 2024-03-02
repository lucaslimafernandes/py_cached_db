cp ./pycacheddb.service /etc/systemd/system/pycacheddb.service
mkdir -p /opt/pycacheddb
cp -r . /opt/pycacheddb

systemctl daemon-reload
systemctl start pycacheddb