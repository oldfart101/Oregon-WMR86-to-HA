# Oregon-WMR86-to-HA
Oregon WMR86 Weather Station to MQTT to Home Assistant

I have an Oregon WMR86 Weather Station, which has these bits in the pack:
* Wind Sensor (WGR800)
* Temperature and Humidity Sensor  (THGR800)
* Rain Gauge (PCR800)

I also have an Acurite 00592TXR temperature & humidity monitor (sensor model number 0600RM)

The above items transmit on the 433MHz band

The Oregon parts transmit via 433MHz to a bespoke receiver, but I capture the stream and then send to my MQTT server, using a NooElec NESDR Mini USB RTL-SDR, DVB-T & ADS-B Receiver.

My set-up works for me! I have a central MQTT server, which everyone in the house can access. So all data for Home Assistant can be got from there.

Thanks to Benjamin Larsson for his Program to decode traffic from Devices that are broadcasting on 433.9 MHz like temperature sensors. - https://github.com/merbanan/rtl_433

On the Raspberry Pi with the NooElec NESDR, I have 433_rtl installed.
I run 
```
rtl_433 -R 40 -R 12 -F csv -U | mosquitto_pub -h 192.168.1.20 -p 1885 -u username -P password -t home/rtl_433 -l
```
where 192.168.1.20 is the address of my MQTT server

There are other methods of sending the file, such as JSON or syslog, but I chose csv.

Now, on the MQTT server, I intercept the MQTT messages and reformat them for Home Assistant using a small python script. (mqtt_read_csv.py)

You can check the MQTT messages with:
```
mosquitto_sub -h 192.168.1.20 -p 1885 -u username -P password -t 'Oregon/#' -v
```
In Home Assistant, my MQTT server is set up (configuration.yaml):
```
mqtt:
 broker: 192.168.1.20
 port: 1885
 client_id: home-assistant
 username: username
 password: password
 keepalive: 30

to read the sensors:
- platform: mqtt
  state_topic: 'acurite/temp'
  name: 'Acurite Temp'
  unit_of_measurement: '°C'
  value_template: '{{ value | round(1) }}' 
  
- platform: mqtt
  state_topic: 'Oregon/gust'
  name: 'Wind Gust'
  unit_of_measurement: 'm/s'
  # m/s
  value_template: '{{ value }}'    
    
    
- platform: mqtt
  state_topic: 'Oregon/direction'
  name: 'Wind Direction'
  unit_of_measurement: ''
  value_template: >-
      {%if states.sensor.wind_direction.state | float<=11 %}North
      {% elif states.sensor.wind_direction.state | float>348 %}North
      {% elif states.sensor.wind_direction.state | float<=34 | float>11 %}North North East
      {% elif states.sensor.wind_direction.state | float<=56 | float>34 %}North East
      {% elif states.sensor.wind_direction.state | float<=79 | float>56 %}East North East
      {% elif states.sensor.wind_direction.state | float<=101 | float>79 %}East
      {% elif states.sensor.wind_direction.state | float<=124 | float>101 %}East South East
      {% elif states.sensor.wind_direction.state | float<=146 | float>124 %}South East
      {% elif states.sensor.wind_direction.state | float<=169 | float>146 %}South South East
      {% elif states.sensor.wind_direction.state | float<=191 | float>169 %}South
      {% elif states.sensor.wind_direction.state | float<=214 | float>191 %}South South West
      {% elif states.sensor.wind_direction.state | float<=236 | float>214 %}South West
      {% elif states.sensor.wind_direction.state | float<=259 | float>236 %}West South West
      {% elif states.sensor.wind_direction.state | float<=281 | float>259 %}West
      {% elif states.sensor.wind_direction.state | float<=304 | float>281 %}West North West
      {% elif states.sensor.wind_direction.state | float<=326 | float>304 %}West North West
      {% elif states.sensor.wind_direction.state | float<=348 | float>326 %}North North West
      {%- endif %}
       
- platform: mqtt
  state_topic: 'Oregon/rain_total'
  name: 'Rain Total'
  unit_of_measurement: 'in'
  value_template: '{{ value }}'
    
- platform: mqtt
  state_topic: 'Oregon/rain_rate'
  name: 'Rain Rate'
  unit_of_measurement: 'in/hr'
  value_template: '{{ value }}'   
```
