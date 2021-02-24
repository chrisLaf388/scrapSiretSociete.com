from selenium import webdriver
import time
import pandas as pd

sirets = []
nafs = []
taillesEntreprise = []
capitaux = []

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
    except:#gere l'exception quand le bouton 'Voir la fiche est placé avant'
        driver.find_element_by_xpath('//*[@id="etablissement"]/a').click()
        time.sleep(1)
    #Scrap code Naf +
    print(driver.find_element_by_xpath('//*[@id="ape-histo-description"]').text)
    # nb salarié +
    print(driver.find_element_by_xpath('//*[@id="trancheeff-histo-description"]').text)
    # capital
    print(driver.find_element_by_xpath('//*[@id="capital-histo-description"]').text)
    #Enregistrement des donnée code naf, taille et capital
    naf = driver.find_element_by_xpath('//*[@id="ape-histo-description"]').text
    tailleEntreprise = driver.find_element_by_xpath('//*[@id="trancheeff-histo-description"]').text
    capital = print(driver.find_element_by_xpath('//*[@id="capital-histo-description"]').text)
    #ajout dans les tableaux
    sirets.append(str(valeurInput))
    nafs.append(naf)
    taillesEntreprise.append(tailleEntreprise)
    capitaux.append(capital)

    # affichage en tableau sans adresse
    test = pd.DataFrame({
        'Siret' : sirets,
        'Code NAF': nafs,
        'Taille Entreprise': taillesEntreprise,
        'Capital' : capitaux
    })

    # creation de fichier csv
    test.to_csv('updateBySiretAtSocieteCom.csv', sep="|", encoding='cp1252')

    driver.close()
