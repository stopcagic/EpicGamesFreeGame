from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from win10toast import ToastNotifier

from time import sleep

import os
import sys
import config

def log_in():
    sign_in_button = driver.find_element_by_xpath('//*[@id="user"]/ul/li/a')
    sign_in_button.click()
    sleep(3)
    login_with_epic = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="login-with-epic"]/div[2]/span/h6'))
    )
    login_with_epic.click()

    username = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="email"]'))
    )
    password = driver.find_element_by_xpath('//*[@id="password"]')
    username.send_keys(config.email)
    password.send_keys(config.password)
    sleep(3)
    login = driver.find_element_by_xpath('//*[@id="login"]')
    login.click()
#---------------------Captcha-----------------------------------------------------------
    try:
        WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="dieselReactWrapper"]/div/div[4]/main/div/div/div/div/div[2]/div/section/div'))
        )
    except:
        WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/form'))
        )
        print('Cock blocked by captcha.')
        driver.quit()
        os.execv(sys.executable, ['python'] + sys.argv)

def browse_games():
    games_carousel = driver.find_elements_by_xpath('//*[@id="dieselReactWrapper"]/div/div[4]/main/div/div/div/div/div[2]/div/section/div/div')
    iterator = 1
    for item in games_carousel:
        check_free = item.find_element_by_xpath('.//div/div/a/div/div/div[1]/div[2]/div/div/span')
        if(check_free.text.upper() == 'FREE NOW'):
            game_name = driver.find_element_by_xpath('//*[@id="dieselReactWrapper"]/div/div[4]/main/div/div/div/div/div[2]/div/section/div/div[{}]/div/div/a/div/div/div[3]/span[1]'.format(iterator))
            addGame = '//*[@id="dieselReactWrapper"]/div/div[4]/main/div/div/div/div/div[2]/div/section/div/div[{}]/div/div/a/div/div/div[1]/div[2]/div/div/span'.format(iterator)
            games.append({
                'name': game_name.text,
                'path': addGame
            })
            iterator = iterator + 1
        else:
            pass
    get_games()

def get_games():
    for game in games:
        sleep(5)
        clickGame = driver.find_element_by_xpath(game['path'])
        clickGame.click()
        #Wait for the page to load and find the button with ugly css selector cuz XPath doesn't work for some reason.
        sleep(5)
        if_owned = driver.find_element_by_css_selector('#dieselReactWrapper > div > div.css-1pmvko1 > main > div > div > div.ProductDetails-wrapper_2d124844 > div > div.ProductDetailHeader-wrapper_e0846efc > div:nth-child(2) > div > div > div.Description-ctaWrapper_e8d00c38 > div > div > div > div.PurchaseButton-ctaButtonContainer_c531d577 > div > button > span > span')
        #Provjerimo dal nam igra vec postoji u library.
        if(if_owned.text.upper() == 'OWNED'):
            notify.show_toast(title='I ran.', msg='You already own ' + game['name'])
            driver.get('https://www.epicgames.com/store/en-US/')
        else:
            #Get the game.
            if_owned.click()

            sleep(5)
            #Brza provjera da li je igra zaista besplatna. Better be safe than sorry.
            check_price = driver.find_element_by_xpath('//*[@id="purchase-app"]/div/div[4]/div[1]/div[2]/div[2]/div[1]/div[1]/div[3]/div[2]/div/span')
            game_price = check_price.text

            if(game_price.split('€')[1] == '0.00'):
                place_order_button = driver.find_element_by_xpath('//*[@id="purchase-app"]/div/div[4]/div[1]/div[2]/div[5]/div/div')
                place_order_button.click()

                accept_refund_rights = driver.find_element_by_xpath('//*[@id="purchase-app"]/div/div[4]/div[1]/div[2]/div[6]/div[2]/div/div[2]/button[2]')
                #And with this, you have your game.
                accept_refund_rights.click()
                driver.get('https://www.epicgames.com/store/en-US/')
                notify.show_toast(title='I got a new game: ', msg=game['name'])
            else:
                print('There is a problem with the price of the game')
                driver.get('https://www.epicgames.com/store/en-US/')


#----------------------------------MAIN--------------------------------------
PATH = 'C:\\Program Files (x86)\\chromedriver.exe'
opts = Options()
opts.headless = False
opts.add_argument('user-agent=' + config.user_agent)
driver = webdriver.Chrome(PATH,options=opts)
driver.get('https://www.epicgames.com/store/en-US/')

games = []
notify = ToastNotifier()

#Try to login
try:
    log_in()
except:
    notify.show_toast(title='Error: ', msg='I failed to login.')

#look up free games
try:
    browse_games()
except:
    notify.show_toast(title='Error: ', msg='I am unable to fetch a game.')


driver.quit()