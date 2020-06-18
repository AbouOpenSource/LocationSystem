if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

airmon-ng check kill
#Launch Monitor mode 
airmon-ng start wl2ps0