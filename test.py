import subprocess

output = subprocess.check_output('cd static/ns3; ./waf --run wifi-periodic 2> ../../log.txt', shell=True, text=True)

print(output)