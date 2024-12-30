# DepthCameraLegacy

I am currently developing a project for taking pictures similar to [depth maps](https://en.wikipedia.org/wiki/Depth_map) Using an Iphone. I have decided that this project would be more useful in swift as an app, so this python code has become antiquated. The new and improved repository for this project is located [here](https://github.com/ADeckerDev/Depth-Camera/blob/main/README.md)

## Users Guide-Setup

### [IOS Side](./IOS%20Side)

The two sides of this program work independantly and are therefore **completely optional** see below

The IOS Side of the code will most certainly be the most difficult to set up. This is swift code ripped straight out of an xcode project. If you want to run this app yourself on your phone, you will need to do the following 

* Install XCode (I'm so sorry)
* Create a new project with the ARKit framework
* Copy and paste my code in
* Create a prompt for camera access
* Switch your phone to developer mode
* Open the xcode project and hit Command R (or the triangle)
* add yourself as a trusted developer (under VPN and Device management in setting)
* There you go I think

**Completely Optional:** The IOS App outputs a .txt file containing the data from a [CVPixelBuffer](https://developer.apple.com/documentation/corevideo/cvpixelbuffer-q2e), ie the distance sensor. The app is necessary to create your own. **If you don't want to bother with the IOS side** I have provided some of these [.txt](./TXT%20Files) files from my own experimentation.

### Python Side

The python script is run through [depthImageProcessor.py](depthImageProcessor.py). Since this is a proof of concept, there is no user input. Just change the variables at the top of the file in the file itself. It works using the [tkinter](https://docs.python.org/3/library/tkinter.html) module.

## [The Future For this project](https://github.com/ADeckerDev/Depth-Camera/blob/main/README.md)

nvm lol i made it private
