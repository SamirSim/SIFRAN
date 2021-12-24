# SIFRAN: Simulating IoT with a FRAmework of NS-3
SIFRAN is a developing framework for setting up and running IoT simulation without writing a single script. It is a no-code initiative for extending the use of NS-3 to non-programmers and IoT community.
# How to deploy
# Install a virtualenv
sudo apt install python3-venv
# Creat virtual environment
python3 -m venv env 
# Activate virtualenv
source env/bin/activate
# Install requirements.txt
pip3 install -r requirements.txt
# To deactivate virtualenv
deactivate
# Configuring and building NS-3
Navigate inside the directory of NS-3 (ns-3) in static
# Configure waf
 ./waf configure --build-profile=optimized --disable-werror
# Build waf
./waf build
# Launch the flask platform
python3 app.py

The website is now accessible at 127.0.0.1 through your browser.