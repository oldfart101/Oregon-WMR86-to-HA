# Oregon-WMR86-to-HA via MQTT
Oregon WMR86 Weather Station to MQTT to Home Assistant

I have an Oregon WMR86 Weather Station, which has these bits in the pack:
* Wind Sensor (WGR800)
* Temperature and Humidity Sensor  (THGR800)
* Rain Gauge (PCR800)

I also have an Acurite 00592TXR temperature & humidity monitor (sensor model number 0600RM)

The above items transmit on the 433MHz band

Also sending data to my MQTT broker are:
EmponPi energy monitor
Sonoff Powr2 
Sonoff basic 2

The Oregon parts normally transmit via 433MHz to a bespoke receiver, but I capture the stream and then send to my MQTT server, using a NooElec NESDR Mini USB RTL-SDR, DVB-T & ADS-B Receiver.

My set-up works for me! I have a central MQTT server, which everyone in the house can access. So all data for Home Assistant can be got from there.

Thanks to Benjamin Larsson for his Program to decode traffic from Devices that are broadcasting on 433.9 MHz like temperature sensors. - https://github.com/merbanan/rtl_433

On the Raspberry Pi with the NooElec NESDR, I have 433_rtl installed.
I run 
```
rtl_433 -R 40 -R 12 -F json -M utc | mosquitto_pub -h 192.168.1.10 -p port# -u username -P password -t home/rtl_433 -l
```
where 192.168.1.10 is the address of my MQTT broker

You can check the MQTT messages with:
```
mosquitto_sub -h 192.168.1.10 -p port# -u username -P password -t '#' -v
```
In Home Assistant, my MQTT server is set up (configuration.yaml):
```
mqtt:
  sensor: !include_dir_merge_list mqtt/
```
to read the sensors:
I have a mqtt sub-directory (config/mqtt) in the HA config directory, which contains the yaml files:
```
oregon.yaml
acurite.yaml
power.yaml
3dprinter-power.yaml
garage.yaml
```
