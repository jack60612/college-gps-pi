# offline-gps-pi

 Offline GPS Raspberry pi app

## Installation

1. Install updates

    ```bash
    sudo apt update & sudo apt upgrade -y
    ```

2. Update boot Config File, enable serial and i2c, and disable serial console. look in the examples folder.

    ```bash
    sudo nano /boot/config.txt
    ```

3. Install required software packages for the gps chip

    ```bash
    sudo apt install -y chrony gpsd gpsd-tools git pps-tools 
    ```

4. Install required software packages for the lcd screen

    ```bash
    sudo apt install -y python3-pip python3-pil python3-numpy python3-smbus python3-serial python3-dev python3-spidev
    ```

5. Install required software packages for this app

    ```bash
    sudo apt install -y libosmium2-dev osmium-tool pyosmium
    ```

5. Turn off the pi

    ```bash
    sudo reboot
    ```

6. Install the components for both devices
    if you do this earlier it might make your pi unstable (ask me how i know), at least leave the power lines disconnected until the software is installed.

7. Configure gpsd and chrony using the provided files in the examples folder

8. enable the gpsd service & chrony service

    ```bash
    sudo systemctl enable gpsd && sudo systemctl start gpsd
    sudo systemctl enable chrony && sudo systemctl start chrony
    ```

9. test gpsd

    ```bash
    cgps -s
    ```

10. test pps

    ```bash
    sudo ppstest /dev/pps0
    ```

11. Clone repo :)

12. create venv and install requirements

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

13. run the app

    ```bash
    python3 -m gpspi
    ```

14. cry because it doesn't work
