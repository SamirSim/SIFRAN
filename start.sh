BUILD_DIR=$(cat .ns_build_symlink)
ln -s /app $BUILD_DIR
cd /app/static/ns3; nohup ./waf &
gunicorn --bind "0.0.0.0:$PORT" -w 2 "app:app" --access-logfile "-" --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s' --log-level info 