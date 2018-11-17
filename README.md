# usbloader-rpc
(Ab)using Wiinnertag to create a Discord rich presence for USB Loaders

I'm too lazy to write a full README, so I will list all the important stuff quickly below.

## Requirements
* Python 3.6 or higher (I might make Windows executables soon)
* A Wii and PC with an internet connection
* A correctly set up USB loader (more below)
* Last but certainly not least: **A Wi-Fi hotspot on the PC that runs the application.** More below.

## Wi-Fi hotspot
Believe it or not, this is actually **very** (!1!11!!) important. Due to unknown reasons, the webhook sent by the Wii will fail to send to an internal IP address unless it's connected to a hotspot on the PC. If you like wikiHow (who doesn't?), [check out this tutorial to assist you into setting one up.](https://www.wikihow.com/Create-a-WiFi-Hotspot-Using-the-Command-Prompt)

## Settings
**Note: this program was tested using USB loader GX. Support for other loaders was made based on assumptions.**

Contact me if you want to test other loaders so I can add them below.

### USB Loader GX
For this loader, you should make sure to enable the "autoinit network" and "Wiinnertag" settings. It might ask you to create a config file; make a guess and pick either yes or no. It doesn't really matter.

This script creates a config file for USB loader GX on every boot (named Wiinnertag.xml). Place this file in SD:/apps/usbloadergx/ and you should be set. Make sure to refresh it once in a while; based on your router, the internal IP of your PC may change, breaking the program. To prevent this, set up a static IP address.
