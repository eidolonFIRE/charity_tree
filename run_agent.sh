cd /home/pi/charity_tree
sleep 5
git pull
sleep 5
sudo python3 agent.py >> "logs/$(date +%Y-%m-%d_%H_%M).log"