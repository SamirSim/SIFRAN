#from os import posix_fallocate
from flask import session
import datetime
from forms import RegisterForm

class ModelRecords:
    def wifiPeriodicRec(self):
        post ={
            "dateTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": session['username'],
            "parameters": {
                "network": session['network'],
                "traffic_direction": session['traffic_direction'],
                "traffic_profile": "periodic",
                "packet_size": session['packet_size'],
                "load_frequency": session['load_freq'],
                "number_devices": session['number_devices'],
                "distance_devices_gateway": session['distance_devices_gateway'],
                "simulation_time": session['simulation_time'],
                "hidden_devices": session['hidden_devices'],
                "propagation_delay_model": session['propagation_delay_model'],
                "propagation_loss_model": session['propagation_loss_model'],
                "mcs": session['mcs'],
                "bandwidth": session['bandwidth'],
                "spatial_streams": session['spatial_streams'],
                "tx_current": session['tx_current'],
                "rx_current": session['rx_current'],
                "idle_current": session['idle_current'],
                "cca_busy_current": session['cca_busy_current'],
                "voltage": session['voltage'],
                "battery_capacity": session['battery_capacity']
            },
            "results": {
                "throughput": session['throughput'],
                "latency": session['latency'],
                "success_rate": session['success_rate'],
                "energy_consumption": session['energy_consumption'],
                "battery_lifetime": session['battery_lifetime']
            }
            }
        return post
    
    def wifiStochasticRec(self):
        post ={
            "dateTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": session['username'],
            "parameters": {
                "network": session['network'],
                "traffic_direction": session['traffic_direction'],
                "traffic_profile": "stochastic",
                "packet_size": session['packet_size'],
                "mean_load": session['mean_load'],
                "number_devices": session['number_devices'],
                "distance_devices_gateway": session['distance_devices_gateway'],
                "simulation_time": session['simulation_time'],
                "hidden_devices": session['hidden_devices'],
                "propagation_delay_model": session['propagation_delay_model'],
                "propagation_loss_model": session['propagation_loss_model'],
                "mcs": session['mcs'],
                "bandwidth": session['bandwidth'],
                "spatial_streams": session['spatial_streams'],
                "tx_current": session['tx_current'],
                "rx_current": session['rx_current'],
                "idle_current": session['idle_current'],
                "cca_busy_current": session['cca_busy_current'],
                "voltage": session['voltage'],
                "battery_capacity": session['battery_capacity']
            },
            "results": {
                "throughput": session['throughput'],
                "latency": session['latency'],
                "success_rate": session['success_rate'],
                "energy_consumption": session['energy_consumption'],
                "battery_lifetime": session['battery_lifetime']
            }
        }    
        return post

    def lorawanRec(self):
        post ={
            "dateTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": session['username'],
            "parameters": {
                "network": session['network'],
                "traffic_direction": session['traffic_direction'],
                "traffic_profile": session['traffic_profile'],
                "packet_size": session['packet_size'],
                "load_frequency": session['load_freq'],
                "number_devices": session['number_devices'],
                "distance_devices_gateway": session['distance_devices_gateway'],
                "hidden_devices": session['hidden_devices'],
                "propagation_delay_model": session['propagation_delay_model'],
                "propagation_loss_model": session['propagation_loss_model'],
                "cyclic_redundacy_check": session['cyclic_redundacy_check'],
                "low_data_rate_optimization": session['low_data_rate_optimization'],
                "implicit_header_mode": session['implicit_header_mode'],
                "sf": session['sf'],
                "bandwidth": session['bandwidth'],
                "tx_current": session['tx_current'],
                "rx_current": session['rx_current'],
                "idle_current": session['idle_current'],
                "voltage": session['voltage'],
                "battery_capacity": session['battery_capacity']
            },
            "results": {
                "throughput": session['throughput'],
                "latency": session['latency'],
                "success_rate": session['success_rate'],
                "energy_consumption": session['energy_consumption'],
                "battery_lifetime": session['battery_lifetime']
            }
        }    
        return post

class ModelUsers:
    def userProfile(self):
        form = RegisterForm()
        post = {"username": form.username.data, "email": form.email.data, "password": session['hasspass']}
        return post
