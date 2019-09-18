# Complete-Server

This is the server for Complete, the VSCode extension that introduces other people's ideas into your code. Written by [Curtis Chong](https://github.com/curtischong), [Akshay Saxena](https://github.com/akshay2000saxena), [Mayank Kanoria](https://github.com/mkanoria),and [Vikram Subramanian](https://github.com/vikramsubramanian). Read what it can do here: [github.com/curtischong/complete](https://github.com/curtischong/complete).

### Installation (For Unix-based computers)

### Setting up Selenium

Since the server needs to scrape data from a webpage, you need to run Selenium.<br>
You will need to install a Chrome driver for your computer (found [here](https://chromedriver.chromium.org/downloads)).<br>
Then go to [scrape.py](scrape.py) and replace the path in the line:<br>

`executable_path='/Users/curtis/Downloads/chromedriver'`<br>
With the path of the Chrome driver on your machine.


### Setting up Flask
First you'll have to tell Flask where the `main.py` file is.<br>
So run `pwd` to get the current directory of the server.<br>
For me, this is `/Users/curtis/Desktop/dev/Complete-Server`.<br>
Then I will open up my `.bash_profile` file (for mac) via `vim ~/.bash_profile`. If you are on linux, run `vim ~/.bashrc`.<br>
Then export the FLASK_APP variable inside the file somewhere:<br>

`export FLASK_APP=/Users/curtis/Desktop/dev/Complete-Server/main.py`<br>

(Don't forget to change my path `/Users/curtis/Desktop/dev/Complete-Server` with the location of yours!)<br>
Now when you leave vim, run `source ~/.bash_profile` (Mac) or `source ~/.bashrc` (Linux).<br>
This will load the path of the server into your terminal session.<br>

Now type `flask run` to turn on the server!




Apologies for forgetting to make a virtual environment and simplifying the requirements installation. This will be fixed in the future.


