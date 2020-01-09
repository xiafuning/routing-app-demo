# routing app #
routing app for multi-RAT platform
## TestMan ##
In this app we use TestMan(Original repo: https://github.com/vodafone-chair/TestMan.git) to do inter-program communication.
### Dependencies ###
`pip install numpy`  
`pip install signalslot`  
`pip install pythonnet` (**Attention:** pythonnet is installed for using module clr, don't use `pip install clr`)  
* pythonnet depends on clang, mono, glib, python-dev, please run `sudo apt update && sudo apt install clang libglib2.0-dev python-dev mono-complete` before installing pythonnet(**Attention:** TestMan doesn't support latest version mono(> 6), don't follow the installation guide on https://www.mono-project.com/download/stable/#download-lin)
* On Ubuntu 16.04 errors may occur when installing pythonnet. This may be because a wrong mono version is installed. By default mono 4.2.1 will be installed, if error occurs please do the following steps to install another version(here we use mono 5.0.0)  
`sudo apt install gnupg ca-certificates`  
`sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF`  
`echo "deb https://download.mono-project.com/repo/ubuntu stable-jessie/snapshots/5.0.0 main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list` (this line assigns a specific mono version which will be installed, please change `stable-jessie/snapshots/5.0.0` part if you want to install other versions.)  
`sudo apt update`  
`sudo apt install mono-complete`  
Then install pythonnet again.
