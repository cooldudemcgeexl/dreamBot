# dreamBot
Python-powered Discord bot to provide [deep-daze](https://github.com/lucidrains/deep-daze) images on demand.
## Getting Started
1. Clone the repository:

`git clone https://github.com/cooldudemcgeexl/DeepDiscordBot.git`

2. Create a new virtual environment and install the required packages from pip:

`pip install -r requirements.txt`

3. Install Nvidia CUDA Toolkit
  * Can be found here: https://developer.nvidia.com/cuda-downloads
  * On Windows, download and run the installer
  * On Linux, CUDA can be installed through your package manager:
    
    Arch:
    
    `sudo pacman -Syu cuda`
    
4. Install Tensorflow:

`pip install tensorflow`

NOTE: On older versions of python (<=3.6), you can use tensorflow-gpu 1.15

`pip install tensorflow-gpu==1.15`

This can be used if running an old version of CUDA

5. Install pytorch for your correct configuration:
  * Find the pip install command for your configuration: https://pytorch.org/
  
6. Create the .env file for the bot using one of the provided templates and a Discrd client token

## Usage
Detailed wiki instructions coming soon™️

## Contributing
If you belive you've found a bug or would like to request a feature, please open an issue on the [Issues](https://github.com/cooldudemcgeexl/dreamBot/issues) page.
Pull requests are welcome.

## Built with
* [deep-daze](https://github.com/lucidrains/deep-daze)
* [discord.py](https://github.com/Rapptz/discord.py)

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
