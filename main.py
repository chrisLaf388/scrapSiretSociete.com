from selenium import webdriver
import time
import pandas as pd

#tableau de siret qui ouvre un page Web
df = pd.read_excel('siret.ods', engine="odf")
len = len(df)
print(len)
for i in range(0,len):
    valeurInput = df['siret'][i]
    # Ouvertur de la page Chrome, Démarrage du robot
    driver = webdriver.Chrome('chromedriver.exe')
    driver.maximize_window()

    # Lien de la page formulaire
    driver.get('https://www.societe.com/')

    #Accepter cookies
    driver.find_element_by_xpath('//*[@id="didomi-notice-agree-button"]').click()

    #inserer le numero de Siret dans le champ text Société.com
    driver.find_element_by_xpath('//*[@id="input_search"]').send_keys(str(valeurInput))
    #Click entrer ou bnt loupe
    driver.find_element_by_xpath('//*[@id="buttsearch"]').click()

    time.sleep(1)

    #Click sur Voir la fiche
    try:
        driver.find_element_by_xpath('//*[@id="etablissement"]/a[2]').click()
        time.sleep(1)
    except:
        driver.find_element_by_xpath('//*[@id="etablissement"]/a').click()
        time.sleep(1)
    #Scrap code Naf +
    print(driver.find_element_by_xpath('//*[@id="ape-histo-description"]').text)
    # nb salarié +
    print(driver.find_element_by_xpath('//*[@id="trancheeff-histo-description"]').text)
    # capital
    print(driver.find_element_by_xpath('//*[@id="capital-histo-description"]').text)

    driver.close()
