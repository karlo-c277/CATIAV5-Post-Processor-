>Web versions will be defined as followed: v1.2.3.4 where the 1. stands for web software version, 2. stands for web patch number, 3. Post processor version, 4 post processor patch number  

# APT-Gcode
This is an open source post processor for ATP files outputed by CAM programs  
It features - translating ATP commands into G-code, also it has select presets for output files, so you dont need to worry if your controler will open the file. But also it allows to make a costum file header, name and extension  

# Usage
The program will ask you to select some options, and the rest is automated  
    - Select the program on your machine for easier startup (Costum/0   WinNC Sinumerik/1):  
        -> here you can choose to load a finished preset or configure the needed information by hand  

# Documentatuion and recources
Most of information about APT and Gcode that used is directly from school  
    But for some things there just is no way for me to understand from 15 APT code files therefore I had to turn to Chrome's smart internet search tool  
    I also used https://archive.org/details/numericalcontrol0000stan for APT commands, but what is the problem? That book is from 1988. So i naturarly used everything from that book since it explains everything  
    Then I used those 15 APT file that I mentioned  

# Main problem and some other issues
-> I have to manually compare every output for the same cycle whilst changing just one value per file to see where is that value located in the code  
CATIA APT1.0 has 0 documentation, all that I could find were like 2 or 3 notifications about how they changed output for some commands. and that is it  
I only have access to CATIAV5 from 2013? I think, and that only in school  
I also have acces to WinNC Sinumerik the newer looking one, but I just made it so it switches to ISO 6983 mode

# Development plan
v0.9 CYCLE/ commands full support  
v1.0 Helix tool path support  
v1.+ G-code output in ISO 6983, WinNC Sinumerik, WinNC Fanuc  
v2.0 SolidWorks APT code support  
v2.+ Support for other CNC controlers  

# Contributing
Can contact me on karlo.ugrin@gmail.com if you want to learn more or do some coding