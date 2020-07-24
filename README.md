# EpicGamesFreeGame
Script uses selenium to browse epic games and claim free games.

REQUIREMENTS
-------------------------------------------------------------------------------------------------------------
Package           Version
----------------- ---------
selenium          3.141.0
win10toast        0.9

1. pip install selenium
2. pip install win10toast

SETTING UP SELENIUM
--------------------------------------------------------------------------------------------------------------
1. Download chrome webdriver so selenium can use your google chrome:
  https://chromedriver.chromium.org/
2. Save chrome webdriver somewhere in your files e.g.(C:\\Program Files (x86)\\chromedriver.exe)
3. Copy the path and paste it into PATH variable

SETTING UP CONFIG.PY
--------------------------------------------------------------------------------------------------------------
1. Open the folder in which you saved app.py and create config.py
2. Enter your credentials.
  e.g. email = 'totallylegit@email.com'
       password = 'mysecurepassword'
       user_agent = '*Type my user agent in google chrome and paste the whole thing'
3. save the file


if captcha keeps popping up, comment out last line of code, run the code a few times and fill out captcha every time.
