# otf

*This program was created for use by me only as I find I develop better tools when I do so targeting a wider audience than myself. However, anyone who finds it useful is welcome to use, distribute, or contribute.*

## Description
This program runs a simple python loop which periodically pings a single-purpose gmail account and checks for new "Performace Summary" emails. These emails are sent out by automatically after each workout session to members' registered email addresses. decided I wanted to be able to track these over time. So, ``otf`` uses [imaplib](https://docs.python.org/2/library/imaplib.html) to authenticate and fetch emails. When new "Performance Summaries" arrive, we use
[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) to parse the emails and extract the numbers of interest. These are then inserted into an [``sqlite3``](https://www.sqlite.org/) database for persistence. 

## Install

### clone the repository

    $ git clone https://github.com/p5a0u9l/otf

### install the python requirements

_NOTE_

* This will install the external library dependancies on your system. It is always a good idea to isolate python programs in virtual environments, see [virtualenv](https://virtualenv.pypa.io/en/stable/).

* If you already know what you're doing, 

    $ pyenv virtualenv 3.6.0 otf
    $ pyenv activate otf
    $ pip install requirements.txt

### run the install hook

    $ ./otf install
    
#### caveats

* authentication (see discussion below)

* file permissions. 
The installer links the shell script to `/usr/local/bin/` by default, but this can be changed in [`config.yml`](./config.yml). 

