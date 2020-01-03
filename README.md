# routing app #

routing app for multi-RAT platform

## TestMan ##
In this app we use TestMan(Original repo: https://github.com/vodafone-chair/TestMan.git) to do inter-program communication.
### Dependencies ###
* `pip install signalslot`
* `pip install pythonnet` (**Attention:** pythonnet is installed for using module clr, don't use `pip install clr`)
* `sudo apt update && sudo apt install mono-devel mono-complete`(**Attention:** TestMan doesn't support latest version mono(> 6), don't follow the installation guide on https://www.mono-project.com/download/stable/#download-lin)
