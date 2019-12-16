## @ 89
## Copyright (c) 2011-2019 Cybervines, LLC
##########################################################################################
## .------..------..------..------..------..------..------.         .------..------.        
## |W.--. ||E.--. ||L.--. ||C.--. ||O.--. ||M.--. ||E.--. | .-.     |T.--. ||O.--. |        
## | :/\: || (\/) || :/\: || :/\: || :/\: || (\/) || (\/) |((3))    | :/\: || :/\: |        
## | :\/: || :\/: || (__) || :\/: || :\/: || :\/: || :\/: | '-.-.   | (__) || :\/: |        
## | '--23|| '--'5|| '--12|| '--'3|| '--15|| '--13|| '--'5|  ((22)) | '--20|| '--15|        
## `------'`------'`------'`------'`------'`------'`------'    '-'  `------'`------'        
## .------..------..------..------..------.         .------..------..------..------..------.
## |C.--. ||Y.--. ||B.--. ||E.--. ||R.--. | .-.     |V.--. ||I.--. ||N.--. ||E.--. ||S.--. |
## | :/\: || (\/) || :(): || (\/) || :(): |((3))    | :(): || (\/) || :(): || (\/) || :/\: |
## | :\/: || :\/: || ()() || :\/: || ()() | '-.-.   | ()() || :\/: || ()() || :\/: || :\/: |
## | '--'3|| '--25|| '--'2|| '--'5|| '--18|  ((22)) | '--22|| '--'9|| '--14|| '--'5|| '--19|
## `------'`------'`------'`------'`------'    '-'  `------'`------'`------'`------'`------'
##########################################################################################
## CV Support
## VR Worlds - https://account.altvr.com/worlds/1092922703423210403
## SL - https://cybervines.slack.com
## Email - webadmin@cybervines.com

##########################################################################################
## Ubuntu Install 
## https://www.ubuntu.com/download/desktop

##########################################################################################
## Kali Install
```
sudo wget https://cdimage.kali.org/kali-2019.1a/kali-linux-2019.1a-amd64.iso
sudo wget http://releases.ubuntu.com/19.10/ubuntu-19.10-desktop-amd64.iso

```
##########################################################################################
## Hackrf ONE
## Linux 4.x Linux 64-bit
## UEFI
## Processor 4
## Memory 6144
## Enable Hypervisor
## Graphic 1024
## LAN Static Public IPv6
## Hard Drive 72 GB
## Sound Default
## USB 2.0 & 3.0

##########################################################################################
## Kali Install
## Add Kali Repositories - Add Kali Repositories
```
sudo nano /etc/apt/sources.list
```
```
deb http://http.kali.org/kali kali-rolling main non-free contrib
```
```
deb-src http://http.kali.org/kali kali-rolling main non-free contrib
```

##########################################################################################
## Update
```
sudo apt update
```
```
sudo apt upgrade
```
```
sudo apt autoremove
```

##########################################################################################
## Guest Install 
```
cd vmware-tools-distrib/
```
```
sudo ./vmware-install.pl 
```
```
sudo shutdown now
```

##########################################################################################
## Kali Install
```
sudo apt install kali-linux-sdr
```
```
sudo apt install kali-linux-nethunter 
```
```
sudo apt install kali-linux-rfid 
```
```
sudo apt install kali-linux-wireless 
```
```
sudo apt install kali-linux-voip
```
```
sudo apt install kali-linux-pwtools 
```
```
sudo apt install kali-linux-web
```
```
sudo apt install kali-linux-full
```
```
sudo apt install kali-linux-all
```

##########################################################################################
## 20+ Mbps
```
host cybervines.com
```
```
sudo apt install speedtest-cli
```
```
speedtest-cli
```

##########################################################################################
## SDR Install 
```
sudo apt-get update
```
```
sudo apt install gqrx-sdr gr-dab gr-dab-dev gr-osmosdr hackrf libhackrf-dev libhackrf0 python3-numpy python3-psutil python3-zmq python3-pyqt5 g++ libpython3-dev python3-pip cython3 pavucontrol fldigi
```
```
sudo pip3 install urh
```

##########################################################################################
## Tools
```
sudo apt install emacs
```
```
sudo apt install ccrypt
```
```
sudo apt install iperf iperf3 
```

##########################################################################################
## Update
```
sudo apt update
```
```
sudo apt upgrade
```
```
sudo apt autoremove 
```

##########################################################################################
## NTP
```
sudo apt install ntpdate
```
```
sudo ntpdate -qu time.apple.com
```

##########################################################################################
## UQC / UQN 
```
cd ~/Documents
```
```
sudo git clone https://github.com/CyberVines/Universal-Quantum-Cymatics.git
```

##########################################################################################
## Connect Hackrf ONE
```
sudo hackrf_info 
```
```
sudo pavucontrol
```
```
sudo fldigi
```
```
sudo gnuradio-companion
```

##########################################################################################
## Configure SDR
# gnuradio-companion:
# Open Play.grc
# Open RadioTX.grc
# Open Record.grc

## Family Radio Service (FRS) - https://en.wikipedia.org/wiki/Family_Radio_Service
## General Mobile Radio Service (GMRS) - https://en.wikipedia.org/wiki/General_Mobile_Radio_Service

## EOF
