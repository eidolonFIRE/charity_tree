cd /home/pi/charity_tree
git pull
sudo python3 agent.py >> "logs/$(date +%Y-%m-%d_%H_%M).log"