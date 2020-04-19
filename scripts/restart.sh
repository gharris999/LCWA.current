
#!/bin/bash


if [ $(ps -efa | grep -v grep | grep test_speed1_3.py -c) -gt 0 ] ;
then
    echo "Process running ...";
else

python3 /home/pi/git/speedtest/src/test_speed1_3.py -t 10 -d /home/pi/git/speedtest/src/LCWA_d.txt -s 18002 &

echo "Starting the process";
fi;
