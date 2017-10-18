#NOTE : git clone on /root  directory
#!/usr/bin/env bash

sudo apt-get update
sudo apt-get -y install python-pip
sudo pip install --upgrade pip

#Install Required Packages for Python2.7
echo "Installing Required Packages for Python2.7"
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

#Download Python 2.7.13
echo "Downloading and Installing Python2.7"
cd /usr/src
wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz
#extract the downloaded package
tar xzf Python-2.7.13.tgz
#Compile Python Source
cd Python-2.7.13
sudo ./configure
sudo make altinstall
#Check the Python Version
python2.7 -V


# Remove existing downloads and binaries so we can start from scratch.
echo "Removing existing downloads and binaries"
rm ~/google-chrome-stable_current_amd64.deb
rm ~/selenium-server-standalone-3.0.1.jar
rm ~/chromedriver_linux64.zip
sudo rm /usr/local/bin/chromedriver
sudo rm /usr/local/share/chromedriver
sudo rm /usr/local/bin/selenium-server-standalone-3.0.1.jar
sudo rm /usr/local/share/selenium-server-standalone-3.0.1.jar

# Install dependencies.
echo "Installing Dependencies..."
cd ~
sudo apt-get install -y openjdk-8-jre-headless xvfb libxi6 libgconf-2-4
apt install unzip

# Install Chrome.
echo "Installing Chrome"
wget -N https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -P ~/
sudo dpkg -i --force-depends ~/google-chrome-stable_current_amd64.deb
sudo apt-get -f install -y
sudo dpkg -i --force-depends ~/google-chrome-stable_current_amd64.deb

# Install ChromeDriver.
echo "Installing Chrome Driver"
cd /root/IP_blacklist_check
wget "http://chromedriver.storage.googleapis.com/2.33/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
rm chromedriver_linux64.zip

# Install Selenium.
echo "Installing Selenium"
pip install selenium

#Install VIrtual Display
echo "Installing virtual display"
pip install pyvirtualdisplay==0.2.1
echo "Installed Everything !!!"