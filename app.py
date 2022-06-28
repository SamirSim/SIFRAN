import json
import os, threading, subprocess
import logging
import io
from subprocess import CalledProcessError
import random, string
import binascii

from bson.objectid import ObjectId
from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask.scaffold import F
from flask_wtf import FlaskForm
from forms import ScenarioForm, RegisterForm, LoginForm
import pymongo, bcrypt
from pymongo import MongoClient
from models import ModelUsers, ModelRecords 
import matplotlib.pyplot as plt


def configure_auto_logging(force_debug=False):
    debug = force_debug or os.getenv('VERBOSE') == '1'
    level_info = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(format="%(message)s" ,level=level_info)

def _check_output(cmd: str, **kwargs) -> str:
    logging.debug(f'cmd: {cmd}')
    output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
    logging.debug(f'output: {output}')
    return output

def _log_file_content(file: str) -> None:
    absolute_path = os.path.abspath(file)
    logging.debug(absolute_path)
    if not os.path.isfile(absolute_path):
        logging.error(f"{absolute_path} does not exists")
        return 

    with io.open(absolute_path) as file_pointer:
        content = file_pointer.read()
        logging.debug(content)

configure_auto_logging()

#cluster = MongoClient("mongodb+srv://admin:KesummWHH5yr68c@cluster0.mi5o8.mongodb.net/web_simulation?retryWrites=true&w=majority")
MONGO_URL=os.getenv('MONGO_URL')
SECRET_KEY=os.getenv('SECRET_KEY', '5791628bb0b13ce0c676dfde280ba245')
NS3_DIR=os.getenv('NS3_DIR', 'static/ns3')

""" 
# To test on local
MONGO_URL = "mongodb://127.0.0.1:27017"
db = cluster["sifran"]
"""

# To run on production
#MONGO_URL=os.getenv('MONGO_URL')
#cluster = MongoClient(MONGO_URL)

#db = cluster.get_default_database()
#db = cluster["sifran"]
#users = db["users"]
#records = db["records"]

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

@app.route('/login', methods = ['POST','GET'])
def login():
    form = LoginForm()
    if 'username' in session:
        return redirect(url_for('dashboard'))    

    if form.validate_on_submit():
        login_user = users.find_one({"username":form.username.data})
        if login_user:
            if bcrypt.checkpw(form.password.data.encode('utf-8'),login_user['password']):
                session['username'] = login_user['username']
                session['email'] = login_user['email']
                return redirect(url_for('dashboard')) 
            else:
                flash("Invalid username/password combination!", "danger")                
        else:
            flash("Invalid username/password combination!", "danger")        
    return render_template("login.html", form=form)

@app.route('/register', methods= ['POST','GET'])
def register():
    form = RegisterForm()
    model = ModelUsers()
    if form.validate_on_submit():
        # Check existing user
        existing_user = users.find_one({"username":form.username.data})
        existing_email = users.find_one({"email":form.email.data})
        print(existing_email, existing_user)
        valid = True
        if existing_user != None:
            valid=False
            flash("This username already exists.", "warning")  

        if existing_email != None:
            valid=False  
            flash("This email address already exists.", "warning")   
        if valid:    
            hasspass = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()) 
            session['hasspass'] = hasspass
            post = model.userProfile()
            users.insert(post)
            session['username'] = form.username.data
            session['email'] = form.email.data
            del session['hasspass']
            return redirect(url_for("dashboard"))

    return render_template("register.html", form=form)    

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user_records = records.find({"username":session['username']})
        return render_template("dashboard.html", user_records=user_records)    
    return redirect(url_for("index"))    

@app.route('/', methods = ['POST', 'GET'])
def index():
    form = ScenarioForm()
    messages_error = ["", ""]
    if request.method == "POST" :
        valid = True
        print("Submitted")
        network = form.network.data
        num_devices = form.num_devices.data
        dist_devices_gateway = form.dist_devices_gateway.data
        simulation_time = form.simulation_time.data
        if num_devices<1 :
            valid =False  
        if simulation_time < 5:
            valid = False
            messages_error[1] = "Simulation time must be > 5."
        if network != "LoRaWAN" and  network != "Wi-Fi HaLow":
            packet_size = form.packet_size_wifi.data
            print("Packet size, WiFi = "+str(packet_size), type(packet_size))
            if packet_size<1 or packet_size>1500 :
                valid = False
                print("Wi-Fi-False")
            if dist_devices_gateway<0 or dist_devices_gateway>50 :
                valid = False    
                messages_error[0] = "Distance must be between 0 and 50 meters."
        else :
            packet_size = form.packet_size_lorawan.data
            print("Packet size, LoRaWAN = "+str(packet_size), type(packet_size))
            if packet_size<1 or packet_size>230 :
                valid = False
                print("LoRaWAN-False")
            if dist_devices_gateway<0 or dist_devices_gateway>8000 :
                valid = False
                messages_error[0] = "Distance must be between 0 and 8000 meters."   
        if form.validate() or valid :       
            session['network'] = form.network.data
            session['traffic_direction'] = form.traffic_dir.data
            session['traffic_profile'] = form.traffic_profile.data
            session['packet_size'] = str(packet_size)
            session['load_freq'] = str(form.load_freq.data)
            session['mean_load'] = str(form.mean_load.data)
            session['fps'] = str(form.fps.data)
            session['mean'] = str(form.mean.data)
            session['variance'] = str(form.variance.data)
            session['number_devices'] = str(form.num_devices.data)
            session['distance_devices_gateway'] = str(form.dist_devices_gateway.data)
            session['simulation_time'] = str(form.simulation_time.data)
            session['hidden_devices'] = dict(form.hidden_devices.choices).get(form.hidden_devices.data)
            session['sf'] = dict(form.sf.choices).get(form.sf.data)
            session['propagation_delay_model'] = dict(form.prop_delay.choices).get(form.prop_delay.data)
            session['radio_environment'] =  str(dict(form.radio_environment.choices).get(form.radio_environment.data))
            session['cyclic_redundacy_check'] = str(form.cyclic_redundacy_check.data)
            session['coding_rate'] = str(form.coding_rate.data)
            session['confirmed_traffic'] = str(form.confirmed_traffic.data)
            session['min_BE'] = str(form.min_BE.data)
            session['max_BE'] = str(form.max_BE.data)
            session['max_frame_retries'] = str(form.max_frame_retries.data)
            session['csma_backoffs'] = str(form.csma_backoffs.data)
            session['mcs'] = str(dict(form.mcs.choices).get(form.mcs.data))
            session['bandwidth'] = str(form.bandwidth.data)
            session['spatial_streams'] = str(form.spatial_streams.data)
            session['tx_current'] = str(form.tx_current.data)
            session['rx_current'] = str(form.rx_current.data)
            session['idle_current'] = str(form.idle_current.data)
            session['cca_busy_current'] = str(form.cca_busy_current.data)
            session['sleep_current'] = str(form.sleep_current.data)
            session['voltage'] = str(form.voltage.data)
            session['battery_capacity'] = str(form.battery_cap.data)

            # Copy all varaibles to environment varaibles to use in the shell script
            os.environ['NETWORK']=session['network']
            os.environ['DISTANCE']=session['distance_devices_gateway'] 
            os.environ['SIMULATION_TIME']=session['simulation_time'] 
            os.environ['NUMDEVICES']=session['number_devices'] 
            os.environ['TRAFFICDIR']=session['traffic_direction']
            os.environ['TRAFFICPROF']=session['traffic_profile']
            os.environ['PACKETSIZE']=session['packet_size']
            os.environ['LOADFREQ']=session['load_freq'] 
            os.environ['FPS']=session['fps'] 
            os.environ['MEAN']=session['mean'] 
            os.environ['VARIANCE']=session['variance'] 
            os.environ['MEANLOAD']= str(session['mean_load'])
            os.environ['HIDDENDEVICES']=form.hidden_devices.data

            os.environ['PROPDELAY']=session['propagation_delay_model']
            os.environ['RADIOENVIRONMENT']=session['radio_environment']
            os.environ['BANDWIDTH']=session['bandwidth']
            os.environ['TXCURRENT']=session['tx_current']
            os.environ['RXCURRENT']=session['rx_current']
            os.environ['IDLECURRENT']=session['idle_current']
            os.environ['CCABUSYCURRENT']=session['cca_busy_current']
            os.environ['SLEEPCURRENT']=session['sleep_current']
            os.environ['VOLTAGE']=session['voltage']
            os.environ['BATTERYCAP']=session['battery_capacity'] 

            # Advanced variables for Wi-Fi
            os.environ['MCS']=form.mcs.data
            os.environ['SPATIALSTREAMS']=session['spatial_streams'] 

            #advanced variables for LoRaWAN
            os.environ['CRC']=session['cyclic_redundacy_check']
            os.environ['CODINGRATE']=session['coding_rate']
            os.environ['CONFIRMEDTRAFFIC']=session['confirmed_traffic']
            os.environ['SF']=form.sf.data

             #advanced variables for 6LoWPAN
            os.environ['MINBE']=session['min_BE']
            os.environ['MAXBE']=session['max_BE']
            os.environ['CSMABACKOFFS']=session['csma_backoffs']
            os.environ['MAXFRAMERETRIES']=session['max_frame_retries']

            output="#"
            latency="#"

            #Create class of a thread
            class myThread (threading.Thread):
                def __init__(self, threadID, output, latency) :
                    threading.Thread.__init__(self)
                    self.threadID = threadID
                    self.output = output
                    self.latency = latency
                def run(self):
                    logging.debug(f"Start Thread {self.threadID}")
                    self.output, self.latency=simulationCall(self.threadID)
                    logging.debug(f"Exit Thread {self.threadID}")
            
            def simulationCall(threadID):
                if threadID==1 :
                    try:
                        logging.debug(f"working dir : {os.getcwd()}")
                        logging.debug(os.environ['NETWORK'])
                        cd_ns3_dir = f"cd {NS3_DIR}; "
                        if os.environ['TRAFFICPROF'] == "cbr":
                            if os.environ['NETWORK'] == "Wi-Fi 802.11ac":
                                output = _check_output(cd_ns3_dir + './waf --jobs=2 --run "wifi-cbr --distance=$DISTANCE --simulationTime=$SIMULATION_TIME --nWifi=$NUMDEVICES --trafficDirection=$TRAFFICDIR --payloadSize=$PACKETSIZE --dataRate=$MEANLOAD --hiddenStations=$HIDDENDEVICES --txCurrent=$TXCURRENT --rxCurrent=$RXCURRENT --idleCurrent=$IDLECURRENT --ccaBusyCurrent=$CCABUSYCURRENT --MCS=$MCS --channelWidth=$BANDWIDTH --propDelay=$PROPDELAY --radioEnvironment=$RADIOENVIRONMENT --spatialStreams=$SPATIALSTREAMS --batteryCap=$BATTERYCAP --voltage=$VOLTAGE"')
                                with open("log.txt", "w") as text_file:
                                    text_file.write(output)
                                _check_output('cat "log.txt" | grep -e "client sent 1023 bytes" -e "server received 1023 bytes from" > "log-parsed.txt";')
                                latency = _check_output('python3 static/ns3/wifi-scripts/get_latencies.py "log-parsed.txt"')

                        elif os.environ['TRAFFICPROF'] == "vbr":
                            if os.environ['NETWORK'] == "Wi-Fi 802.11ac":
                                output = _check_output(cd_ns3_dir +'./waf --jobs=2 --run "wifi-vbr --distance=$DISTANCE --simulationTime=$SIMULATION_TIME --nWifi=$NUMDEVICES --trafficDirection=$TRAFFICDIR --fps=$FPS --mean=$MEAN --variance=$VARIANCE --hiddenStations=$HIDDENDEVICES --MCS=$MCS --channelWidth=$BANDWIDTH --propDelay=$PROPDELAY --radioEnvironment=$RADIOENVIRONMENT --txCurrent=$TXCURRENT --rxCurrent=$RXCURRENT --idleCurrent=$IDLECURRENT --ccaBusyCurrent=$CCABUSYCURRENT --spatialStreams=$SPATIALSTREAMS --batteryCap=$BATTERYCAP --voltage=$VOLTAGE" 2> log.txt')
                                with open("log.txt", "w") as text_file:
                                    text_file.write(output)
                                _check_output('cat "log.txt" | grep -e "client sent 1023 bytes" -e "server received 1023 bytes from" > "log-parsed.txt";')
                                latency = _check_output('python3 static/ns3/wifi-scripts/get_latencies.py "log-parsed.txt"')                               

                        elif os.environ['TRAFFICPROF'] == "periodic":
                            if os.environ['NETWORK'] == "Wi-Fi 802.11ac":
                                output = _check_output(cd_ns3_dir +'./waf --jobs=2 --run "wifi-periodic --distance=$DISTANCE --simulationTime=$SIMULATION_TIME --nWifi=$NUMDEVICES --trafficDirection=$TRAFFICDIR --payloadSize=$PACKETSIZE --period=$LOADFREQ --hiddenStations=$HIDDENDEVICES --radioEnvironment=$RADIOENVIRONMENT --spatialStreams=$SPATIALSTREAMS --txCurrent=$TXCURRENT --rxCurrent=$RXCURRENT --idleCurrent=$IDLECURRENT --ccaBusyCurrent=$CCABUSYCURRENT --MCS=$MCS --channelWidth=$BANDWIDTH --propDelay=$PROPDELAY --spatialStreams=$SPATIALSTREAMS --batteryCap=$BATTERYCAP --voltage=$VOLTAGE 2> log.txt"')
                                output1 = _check_output('cat "log.txt"')
                                print("LOG: ", output1)
                                with open("log.txt", "w") as text_file:
                                    text_file.write(output)
                                _check_output('cat "log.txt" | grep -e "client sent 1023 bytes" -e "server received 1023 bytes from" > "log-parsed.txt";')
                                latency = _check_output('python3 static/ns3/wifi-scripts/get_latencies.py "static/ns3/log-parsed.txt"')

                            elif os.environ['NETWORK'] == "LoRaWAN":
                                output = _check_output(cd_ns3_dir +'./waf --jobs=2 --run "lora-periodic --distance=$DISTANCE --simulationTime=$SIMULATION_TIME --nSta=$NUMDEVICES --payloadSize=$PACKETSIZE --period=$LOADFREQ --SF=$SF --crc=$CRC --codingRate=$CODINGRATE --trafficType=$CONFIRMEDTRAFFIC --channelWidth=$BANDWIDTH --propDelay=$PROPDELAY --radioEnvironment=$RADIOENVIRONMENT --voltage=$VOLTAGE --txCurrent=$TXCURRENT --rxCurrent=$RXCURRENT --sleepCurrent=$SLEEPCURRENT" 2> log.txt')
                                with open("log.txt", "w") as text_file:
                                    text_file.write(output)
                                output = output + "Energy consumption: " + _check_output(cd_ns3_dir+"cat log.txt | grep -e 'LoraRadioEnergyModel:Total energy consumption' | tail -1 | awk 'NF>1{print $NF}' | sed 's/J//g'")
                                latency = _check_output(cd_ns3_dir+'cat log.txt | grep -e "Total time" > log-parsed.txt; python3 lora-scripts/get_latencies.py log-parsed.txt')
                                latency = _check_output('cat "log-parsed.txt"')
                            
                            elif os.environ['NETWORK'] == "6LoWPAN":
                                output = _check_output(cd_ns3_dir +'./waf --jobs=2 --run "6lowpan-periodic --distance=$DISTANCE --simulationTime=$SIMULATION_TIME --nSta=$NUMDEVICES --packetSize=$PACKETSIZE --period=$LOADFREQ --min_BE=$MINBE --max_BE=$MAXBE --csma_backoffs=$CSMABACKOFFS --maxFrameRetries=$MAXFRAMERETRIES --voltage=$VOLTAGE --txCurrent=$TXCURRENT --rxCurrent=$RXCURRENT --idleCurrent=$IDLECURRENT" 2> log.txt')
                                with open("log.txt", "w") as text_file:
                                    text_file.write(output)
                                _check_output(cd_ns3_dir+'cat "log.txt" | grep -e "client sent 50 bytes" -e "server received 50 bytes from" > "log-parsed.txt";')
                                latency = _check_output('python3 static/ns3/wifi-scripts/get_latencies.py "static/ns3/log-parsed.txt"')
                            
                            elif os.environ['NETWORK'] == "Wi-Fi HaLow":
                                output = _check_output('cd static/ns3-halow; ./waf --jobs=2 --run "rca --rho=$DISTANCE --simulationTime=$SIMULATION_TIME --Nsta=$NUMDEVICES --payloadSize=$PACKETSIZE --trafficInterval=$LOADFREQ --mcs=$MCS --bandWidth=$BANDWIDTH --voltage=$VOLTAGE --txCurrent=$TXCURRENT --rxCurrent=$RXCURRENT --idleCurrent=$IDLECURRENT" 2> log.txt')
                                with open("log.txt", "w") as text_file:
                                    text_file.write(output)
                                _check_output('cd static/ns3-halow; cat log.txt | grep -e "UdpEchoClientApplication" -e "UdpEchoServerApplication" > log-parsed.txt;')
                                latency = _check_output('python3 static/ns3-halow/halow-scripts/get_latencies.py "static/ns3-halow/log-parsed.txt"')
                                
                    except CalledProcessError as exception:
                        _log_file_content(f'{NS3_DIR}/log.txt')
                        _log_file_content(f'{NS3_DIR}/log-parsed.txt')
                        logging.error(exception.output)
                        logging.error(exception.stderr)
                        raise exception
                    finally:
                        pass
                        #_check_output(cd_ns3_dir+'rm "log.txt"; rm "log-parsed.txt"')

                    return output, latency
            #Call NS-3 simulation by python shell script according network type
            try:
                model = ModelRecords()
                if (network == 'LoRaWAN') :
                    thread1 = myThread(1, output, latency)
                    thread1.start()
                    thread1.join()
                    output, latency = thread1.output, thread1.latency
                    throughput = 0
                    lines = output.splitlines()
                    line = lines[0]
                    i = 0
                    while "Success" not in line:
                        i = i + 1
                        line = lines[i]

                    success_rate = round(float(lines[i].split()[-1]), 2)
                    throughput = round(float(lines[i+1].split()[-1]), 2)
                    energy = float(lines[i+2].split()[-1])
                    capacity = (float(session['battery_capacity']) / 1000.0) * float(session['voltage']) * 3600
                    battery_lifetime = round(((capacity / energy) * float(session['simulation_time'])) / 86400 / 365, 2)
                    energy = round(energy, 2)
                    session['energy_consumption'] = energy
                    latency = float(latency) * 1000
                    session['latency'] = str(latency) # To get in ms
                    session['latency'] = latency
                    session['throughput'] = throughput
                    session['success_rate'] = success_rate
                    session['battery_lifetime'] = battery_lifetime

                    densities = [int(session['number_devices']) + i for i in range(1,5)]
                    results_exploration = explore('LoRaWAN', densities)

                    print(results_exploration)

                    success_rates = [row[1] for row in results_exploration]
                    battery_lifetimes = [row[2] for row in results_exploration]

                    id = binascii.b2a_hex(os.urandom(12)).decode("ascii")
                    session['id'] = id
                    session['path'] = id

                    plt.figure()
                    plt.plot(densities, success_rates)
                    plt.xlabel('Number of end-devices')
                    plt.ylabel('Success Rate')
                    plt.savefig('static/img/'+id+'-success-rate.png')
                    #plt.show()

                    #If a user has already login, save input parameters and results in JSON. 
                    if 'username' in session:
                        post = model.lorawanRec()

                elif (network == '6LoWPAN') :
                    thread1 = myThread(1, output, latency)
                    thread1.start()
                    thread1.join()
                    output, latency = thread1.output, thread1.latency
                    lines = output.splitlines()
                    line = lines[0]
                    i = 0
                    while "Total" not in line:
                        i = i + 1
                        line = lines[i]
                    
                    energy = float(lines[i].split()[-1])
                    battery_lifetime = float(lines[i+1].split()[-1])
                    throughput = float(lines[i+2].split()[-1])
                    success_rate = float(lines[i+3].split()[-1])
                    latency = float(latency)

                    session['energy_consumption'] = energy
                    session['throughput'] = throughput
                    session['latency'] = str(latency) # To get in ms
                    session['success_rate'] = success_rate
                    session['battery_lifetime'] = battery_lifetime

                    densities = [int(session['number_devices']) + i for i in range(1,5)]
                    results_exploration = explore('6LoWPAN', densities)

                    print(results_exploration)

                    success_rates = [row[1] for row in results_exploration]
                    battery_lifetimes = [row[2] for row in results_exploration]
                    latencies = [row[3] for row in results_exploration]

                    id = binascii.b2a_hex(os.urandom(12)).decode("ascii")
                    session['id'] = id
                    session['path'] = id

                    plt.figure()
                    plt.plot(densities, success_rates)
                    plt.xlabel('Number of end-devices')
                    plt.ylabel('Success Rate')
                    plt.savefig('static/img/'+id+'-success-rate.png')
                    #plt.show()

                    plt.figure()
                    plt.plot(densities, battery_lifetimes)
                    plt.xlabel('Number of end-devices')
                    plt.ylabel('Battery Lifetime')
                    plt.savefig('static/img/'+id+'-battery-lifetime.png')
                    #plt.show()

                    plt.figure()
                    plt.plot(densities, latencies)
                    plt.xlabel('Number of end-devices')
                    plt.ylabel('Packet Latency')
                    plt.savefig('static/img/'+id+'-latency.png')
                    #plt.show()

                    if 'username' in session:
                        post = model.sixlowpanRec()

                elif (network == 'Wi-Fi HaLow'):
                    thread1 = myThread(1, output, latency)
                    thread1.start()
                    thread1.join()
                    output, latency = thread1.output, thread1.latency
                    lines = output.splitlines()
                    line = lines[0]
                    i = 0
                    while "Total" not in line:
                        i = i + 1
                        line = lines[i]

                    energy = float(lines[i].split()[-1])
                    battery_lifetime = float(lines[i+1].split()[-1])
                    throughput = float(lines[i+2].split()[-1])
                    success_rate = float(lines[i+3].split()[-1])
                    latency = float(latency) * 1000

                    session['energy_consumption'] = energy
                    session['throughput'] = throughput
                    session['latency'] = str(latency) # To get in ms
                    session['success_rate'] = success_rate
                    session['battery_lifetime'] = battery_lifetime

                    id = binascii.b2a_hex(os.urandom(12)).decode("ascii")
                    session['id'] = id
                    session['path'] = id

                    densities = [int(session['number_devices']) + i for i in range(1,5)]
                    results_exploration = explore('Wi-Fi HaLow', densities)

                    print(results_exploration)

                    success_rates = [row[1] for row in results_exploration]
                    battery_lifetimes = [row[2] for row in results_exploration]
                    latencies = [row[3] for row in results_exploration]

                    plt.figure()
                    plt.plot(densities, success_rates)
                    plt.xlabel('Number of end-devices')
                    plt.ylabel('Success Rate')
                    plt.savefig('static/img/'+id+'-success-rate.png')
                    #plt.show()

                    plt.figure()
                    plt.plot(densities, battery_lifetimes)
                    plt.xlabel('Number of end-devices')
                    plt.ylabel('Battery Lifetime')
                    plt.savefig('static/img/'+id+'-battery-lifetime.png')
                    #plt.show()

                    plt.figure()
                    plt.plot(densities, latencies)
                    plt.xlabel('Number of end-devices')
                    plt.ylabel('Packet Latency')
                    plt.savefig('static/img/'+id+'-latency.png')
                    #plt.show()

                    #If a user has already login, save input parameters and results in JSON. 
                    if 'username' in session:
                        post = model.wifiPeriodicRec()

                else :
                    thread1 = myThread(1,output, latency)
                    thread1.start()
                    thread1.join()
                    output, latency = thread1.output, thread1.latency
                    lines = output.splitlines()
                    line = lines[0]
                    i = 0
                    while "Total" not in line:
                        i = i + 1
                        line = lines[i]
                    energy = lines[i].split()[-1]
                    battery_lifetime = lines[i+1].split()[-1]
                    throughput = lines[i+2].split()[-1]
                    success_rate = lines[i+3].split()[-1]

                    session['energy_consumption'] = energy
                    session['throughput'] = throughput
                    latency = float(latency) * 1000
                    session['latency'] = str(latency) # To get in ms
                    session['success_rate'] = success_rate
                    session['battery_lifetime'] = battery_lifetime
                    
                    densities = [int(session['number_devices']) + i for i in range(1,5)]
                    results_exploration = explore('Wi-Fi', densities)

                    print(results_exploration)

                    success_rates = [row[1] for row in results_exploration]
                    battery_lifetimes = [row[2] for row in results_exploration]
                    latencies = [row[3] for row in results_exploration]

                    id = binascii.b2a_hex(os.urandom(12)).decode("ascii")
                    session['id'] = id
                    session['path'] = id

                    plt.figure()
                    plt.plot(densities, success_rates)
                    plt.xlabel('Number of end-devices')
                    plt.ylabel('Success Rate')
                    plt.savefig('static/img/'+id+'-success-rate.png')
                    #plt.show()

                    plt.figure()
                    plt.plot(densities, battery_lifetimes)
                    plt.xlabel('Number of end-devices')
                    plt.ylabel('Battery Lifetime')
                    plt.savefig('static/img/'+id+'-battery-lifetime.png')
                    #plt.show()

                    plt.figure()
                    plt.plot(densities, latencies)
                    plt.xlabel('Number of end-devices')
                    plt.ylabel('Packet Latency')
                    plt.savefig('static/img/'+id+'-latency.png')
                    #plt.show()

                    # If a user has already login, save input parameters and results in JSON. 
                    if 'username' in session:
                        if form.traffic_profile.data == 'periodic':   
                            post = model.wifiPeriodicRec()           
                        else:
                            post = model.wifiStochasticRec()
                # Insert a record of parameters and results according to an account of a user to a collection "records", if this user has already login
                if 'username' in session:
                    records.insert_one(post)  

                jResults = {
                    "throughput": throughput,
                    "latency":  latency, # To get in ms
                    "success_rate": success_rate,
                    "energy_consumption": energy,
                    "battery_lifetime": battery_lifetime,
                    "path": id
                }
               
                return render_template("results.html", jResults=jResults)
            except Exception as e:
                print('error:', e)    
                flash("There was a problem during simulation.", "warning")             
    print("Messages error distance ="+messages_error[0])   
    return render_template("index.html", form=form, messages_error=messages_error)

"""
@app.route('/results')
def results():
    return render_template("results.html")
"""
@app.route('/documents')
def documents():
    return render_template("documents.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/api/<id>')    
def api(id):
    objID = ObjectId(id)
    user_record = records.find_one({"_id": objID})
    if user_record != None:
        record_json = json.dumps(user_record, indent=4, default=str)
        print(record_json)
        return render_template("result_records.html",user_record=user_record)
    return "No record found."     

@app.route('/delete/<id>')
def delete(id):
    objID = ObjectId(id)
    try:
        records.delete_one({"_id": objID})
    except Exception as e:
        print('error: ',e)   
        flash("Cannot delete this record!", "danger")
    return redirect(url_for('dashboard')) 

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    #session.pop('username',None)
    session.clear()
    return redirect(url_for('index'))

def explore(technology, densities):
    results_exploration = []
    if technology == "Wi-Fi":
        for nb_devices in densities:
            os.environ['NUMDEVICES'] = str(nb_devices)
            #os.environ['LOGFILE'] = "log-"+technology+"-"+str(use_case)+"-"+str(nb_devices)+"-"+str(packet_period)+".txt"
            #os.environ['LOGFILEPARSED'] = "log-"+technology+"-"+str(use_case)+"-"+str(nb_devices)+"-"+str(packet_period)+"-parsed.txt"

            output = _check_output('cd static/ns3; ./waf --jobs=2 --run "wifi-periodic --distance=$DISTANCE --simulationTime=$SIMULATION_TIME --nWifi=$NUMDEVICES --trafficDirection=$TRAFFICDIR --payloadSize=$PACKETSIZE --period=$LOADFREQ --hiddenStations=$HIDDENDEVICES --radioEnvironment=$RADIOENVIRONMENT --spatialStreams=$SPATIALSTREAMS --txCurrent=$TXCURRENT --rxCurrent=$RXCURRENT --idleCurrent=$IDLECURRENT --ccaBusyCurrent=$CCABUSYCURRENT --MCS=$MCS --channelWidth=$BANDWIDTH --propDelay=$PROPDELAY --spatialStreams=$SPATIALSTREAMS --batteryCap=$BATTERYCAP --voltage=$VOLTAGE 2> log.txt"')
            _check_output('cd static/ns3; cat "log.txt" | grep -e "client sent 1023 bytes" -e "server received 1023 bytes from" > "log-parsed.txt";')
            latency = _check_output('python3 static/ns3/wifi-scripts/get_latencies.py "static/ns3/log-parsed.txt"')

            #latency = subprocess.check_output('cd NS3-6LoWPAN; cat $LOGFILE | grep -e "UdpEchoClientApplication" -e "UdpEchoServerApplication" > $LOGFILEPARSED; python3 wifi-scripts/get_latencies.py $LOGFILEPARSED', shell=True, text=True,stderr=subprocess.DEVNULL)
            #subprocess.check_output('rm "log-wifi.txt"; rm "log-wifi-parsed.txt"', shell=True, text=True,stderr=subprocess.DEVNULL)

            lines = output.splitlines()
            line = lines[0]
            #print(lines)
            i = 0
            while "Total" not in line:
                i = i + 1
                line = lines[i]
            energy = float(lines[i].split()[-1])
            battery_lifetime = float(lines[i+1].split()[-1])
            #throughput = float(lines[i+2].split()[-1])
            success_rate = float(lines[i+3].split()[-1])
            latency = float(latency) * 1000

            result = [nb_devices, success_rate, battery_lifetime, latency]
                                        
            #configuration = "WiFi-"+str(mcs)+"-"+str(sgi)+"-"+str(spatial_stream)+"-"+str(agregation)+"-"+str(ngateway)
            #configuration = "WiFi-GW"+str(ngateway)+"-Nsta"+str(nb_devices)+"-Period"+str(packet_period)+": "+str(result)
            results_exploration.append(result)

            #_check_output('cd static/ns3; rm "log.txt"; rm "log-parsed.txt"')

            #print("WiFi: ", mcs, sgi, spatial_stream, agregation, ngateway, result)


    elif technology == "LoRaWAN":
        for nb_devices in densities:
            os.environ['NUMDEVICES'] = str(nb_devices)
            #os.environ['LOGFILE'] = "log-"+technology+"-"+str(use_case)+"-"+str(nb_devices)+"-"+str(packet_period)+".txt"
            #os.environ['LOGFILEPARSED'] = "log-"+technology+"-"+str(use_case)+"-"+str(nb_devices)+"-"+str(packet_period)+"-parsed.txt"

            output = _check_output('cd static/ns3; ./waf --jobs=2 --run "lora-periodic --distance=$DISTANCE --simulationTime=$SIMULATION_TIME --nSta=$NUMDEVICES --payloadSize=$PACKETSIZE --period=$LOADFREQ --SF=$SF --crc=$CRC --codingRate=$CODINGRATE --trafficType=$CONFIRMEDTRAFFIC --channelWidth=$BANDWIDTH --propDelay=$PROPDELAY --radioEnvironment=$RADIOENVIRONMENT --voltage=$VOLTAGE --txCurrent=$TXCURRENT --rxCurrent=$RXCURRENT --sleepCurrent=$SLEEPCURRENT" 2> log.txt')
            output = output + "Energy consumption: " + _check_output("cd static/ns3; cat log.txt | grep -e 'LoraRadioEnergyModel:Total energy consumption' | tail -1 | awk 'NF>1{print $NF}' | sed 's/J//g'")
            latency = _check_output('cd static/ns3; cat log.txt | grep -e "Total time" > log-parsed.txt; python3 lora-scripts/get_latencies.py log-parsed.txt')
            #subprocess.check_output('rm "log-lora.txt"; rm "log-lora-parsed.txt"', shell=True, text=True,stderr=subprocess.DEVNULL)

            #throughput = 0
            lines = output.splitlines()
            line = lines[0]
            i = 0
            while "Success" not in line:
                i = i + 1
                line = lines[i]
            success_rate = round(float(lines[i].split()[-1]), 2)
            #throughput = round(float(lines[i+1].split()[-1]), 2)
            energy = float(lines[i+2].split()[-1])
            capacity = (float(session['battery_capacity']) / 1000.0) * float(session['voltage']) * 3600
            battery_lifetime = round(((capacity / energy) * float(session['simulation_time'])) / 86400, 2)

            result = [nb_devices, success_rate, battery_lifetime]

            results_exploration.append(result)

            #_check_output('cd static/ns3; rm "log.txt"; rm "log-parsed.txt"')

    elif technology == "6LoWPAN":
        for nb_devices in densities:
            os.environ['NUMDEVICES'] = str(nb_devices)
            os.environ['LOGFILE'] = "log-"+str(nb_devices)+".txt"
            os.environ['LOGFILEPARSED'] = "log-"+str(nb_devices)+"-parsed.txt"

            output = _check_output('cd static/ns3; ./waf --jobs=2 --run "6lowpan-periodic --distance=$DISTANCE --simulationTime=$SIMULATION_TIME --nSta=$NUMDEVICES --packetSize=$PACKETSIZE --period=$LOADFREQ --min_BE=$MINBE --max_BE=$MAXBE --csma_backoffs=$CSMABACKOFFS --maxFrameRetries=$MAXFRAMERETRIES --voltage=$VOLTAGE --txCurrent=$TXCURRENT --rxCurrent=$RXCURRENT --idleCurrent=$IDLECURRENT" 2> $LOGFILE')
            latency = _check_output('cd static/ns3; cat $LOGFILE | grep -e "client sent 50 bytes" -e "server received 50 bytes from" > $LOGFILEPARSED; python3 wifi-scripts/get_latencies.py $LOGFILEPARSED')
            #latency = subprocess.check_output('cd NS3-6LoWPAN; cat $LOGFILE | grep -e "UdpEchoClientApplication" -e "UdpEchoServerApplication" > $LOGFILEPARSED; python3 wifi-scripts/get_latencies.py $LOGFILEPARSED', shell=True, text=True,stderr=subprocess.DEVNULL)
            #subprocess.check_output('rm "log-6lowpan.txt"; rm "log-6lowpan-parsed.txt"', shell=True, text=True,stderr=subprocess.DEVNULL)

            lines = output.splitlines()
            line = lines[0]
            i = 0
            while "Total" not in line:
                i = i + 1
                line = lines[i]
            energy = float(lines[i].split()[-1])
            battery_lifetime = float(lines[i+1].split()[-1])
            #throughput = float(lines[i+2].split()[-1])
            success_rate = float(lines[i+3].split()[-1])
            latency = float(latency) * 1000

            result = [nb_devices, success_rate, battery_lifetime, latency]

            results_exploration.append(result)
            
            #_check_output('cd static/ns3; rm $LOGFILE; rm $LOGFILEPARSED')

    elif technology == "Wi-Fi HaLow":
        for nb_devices in densities:
            os.environ['NUMDEVICES'] = str(nb_devices)
            #os.environ['LOGFILE'] = "log-"+technology+"-"+str(use_case)+"-"+str(nb_devices)+"-"+str(packet_period)+".txt"
            #os.environ['LOGFILE'] = "log-"+technology+"-"+str(use_case)+"-"+str(nb_devices)+"-"+str(packet_period)+"-parsed.txt"

            #subprocess.check_output("cd NS3-802.11ah; ./scratch/RAWGenerate.sh $NBDEVICES $NRAWGROUPS $BEACONINTERVAL", shell=True, text=True,stderr=subprocess.DEVNULL)
            output = _check_output('cd static/ns3-halow; ./waf --jobs=2 --run "rca --rho=$DISTANCE --simulationTime=$SIMULATION_TIME --Nsta=$NUMDEVICES --payloadSize=$PACKETSIZE --trafficInterval=$LOADFREQ --mcs=$MCS --bandWidth=$BANDWIDTH --voltage=$VOLTAGE --txCurrent=$TXCURRENT --rxCurrent=$RXCURRENT --idleCurrent=$IDLECURRENT" 2> log.txt')
            _check_output('cd static/ns3-halow; cat log.txt | grep -e "UdpEchoClientApplication" -e "UdpEchoServerApplication" > log-parsed.txt;')
            latency = _check_output('python3 static/ns3-halow/halow-scripts/get_latencies.py "static/ns3-halow/log-parsed.txt"')
            #latency = subprocess.check_output('cd NS3-802.11ah; cat $LOGFILE | grep -e "UdpEchoClientApplication" -e "UdpEchoServerApplication" > $LOGFILEPARSED; python3 halow-scripts/get_latencies.py $LOGFILEPARSED', shell=True, text=True,stderr=subprocess.DEVNULL)

            #latency = subprocess.check_output('cd NS3-802.11ah; python3 halow-scripts/get_latencies.py $LOGFILE', shell=True, text=True,stderr=subprocess.DEVNULL)
            #subprocess.check_output('rm "log-wifi.txt"; rm "log-wifi-parsed.txt"', shell=True, text=True,stderr=subprocess.DEVNULL)

            lines = output.splitlines()
            line = lines[0]
            i = 0
            while "Total" not in line:
                i = i + 1
                line = lines[i]
            energy = float(lines[i].split()[-1])
            battery_lifetime = float(lines[i+1].split()[-1])
            throughput = float(lines[i+2].split()[-1])
            success_rate = float(lines[i+3].split()[-1])

            latency = float(latency) * 1000

            result = [nb_devices, success_rate, battery_lifetime, latency]

            results_exploration.append(result)

            #_check_output('cd static/ns3-halow; rm "log.txt"; rm "log-parsed.txt"')

    return results_exploration

if __name__ == "__main__" :
    port = os.getenv('PORT', 80)
    app.run(debug=True, port=port, reloader_interval=99999999)