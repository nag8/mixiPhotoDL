from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import configparser
import urllib.request

# 設定ファイル取得
def getIniFile():
    iniFile = configparser.ConfigParser()
    iniFile.read('./config.ini', 'UTF-8')
    return iniFile

# chromeを準備
def initDriver(iniFile):

    # driverを定義
    options = webdriver.ChromeOptions()

    #プロファイル場所を定義
    options.add_argument('--user-data-dir=' + iniFile.get('settings', 'user-data-dir'))
    return webdriver.Chrome(options=options)

# 写真IDのリストを取得
def getKeyList(iniFile):
    keyList = []
    with open(iniFile.get('settings', 'READFILE'),'r') as f:
        line = f.readline()
        while line:
            keyList.append(line.strip())
            line = f.readline()

    return keyList


# 写真を保存
def savePicture(driver, iniFile, key):

    # 画面遷移
    driver.get('https://photo.mixi.jp/view_photo.pl?photo_id=' + key + '&owner_id=' + iniFile.get('profile', 'OWNER'))

    # 対象写真を取得
    img = driver.find_element_by_xpath('//p[@class="photo"]/a/img')
    src = img.get_attribute('src')

    # 画像をDL
    urllib.request.urlretrieve(src, iniFile.get('settings', 'OUT') + key + ".png")


# メイン処理
def main():

    # 設定ファイル取得
    iniFile = getIniFile()

    # chrome画面を準備
    driver = initDriver(iniFile)
    
    # URLリストを取得
    keyList = getKeyList(iniFile)

    # 写真IDの数だけ画像DL
    for key in keyList:
        savePicture(driver, iniFile, key)

    # 終了
    driver.quit()
    exit()


if __name__ == '__main__':
    main()
