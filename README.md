# Fast-Switching-Webradio
A simple python webradio implementation using mpd to play webradio streams and mpc to control the mpd-servers. The streams are played in parallel (prebuffering) since they dont need much bandwidth and it makes switching stations with a slider fast and responsive.

This code should be easily adaptable to other interfaces and hardware. 

Feel free to contact me on GitHub or Thingiverse if any help is needed.

Needed Hardware for this project on Thingiverse:
Tested on raspbian. 

Usage:
1. Install mpd, mpc and python3.

2. Unzip mpd-config.zip and replace the folder ~/.config/mpd with it. (Included are the configuration files for running the mpd servers in parallel.)
Warning: If you use mpd to play music and have your own mpd setup on the raspberry, incorporate the files with your own configuration or backup your own config before replacing the folder.

3. Modify the ten webradio stations in ~/.config/mpd/playlists/webradio_stations.m3u to your liking

4. Copy the two python files on the Raspberry Pi and start the webradio: "python3 webradio_parallel.py"

Hints: 
* Use an external USB soundcard for a better soundquality.
* Run the python script on startup for ease of use.

Troubleshooting:
* Problem: The Raspberry Pi restarts when the script is starting the mpd-servers. 
Possible Solution: With all ten mpd-Servers running, the raspberry pi is driven close to 100% CPU load. Make sure your power supply is capable of delivering the necessary current.

* Problem: The Sound stops after a longer period of listening and recovers for a short period after muting and unmuting with button_0.
Possible Solution: With all ten mpd-Servers running, the raspberry pi is driven close to 100% CPU load. Make sure your CPU is properly cooled with a heatsink.
