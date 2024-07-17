#!/usr/bin/python

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('burattino.p@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345678')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
 
    yield driver
 
    driver.quit()
 
def test_show_all_users_pets(driver):
    # Вводим email
    # driver.find_element(By.ID, 'email').send_keys('burattino.p@gmail.com')
    # Вводим пароль
    # driver.find_element(By.ID, 'pass').send_keys('12345678')
    # Нажимаем на кнопку входа в аккаунт
    # driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    # assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.get('https://petfriends.skillfactory.ru/my_pets')
 
    # elt = driver.find_element(By.XPATH, '//div[contains(@class,".col-sm-4 left")]')
    elt = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,".col-sm-4 left")]')))
    pets_num = int(elt.text[18])

    # elts = driver.find_elements(By.XPATH, '//div[@title="Удалить питомца"]')
    elts = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@title="Удалить питомца"]')))
    
    assert pets_num == len(elts)

def test_half_pets_have_photo(driver):
    driver.get('https://petfriends.skillfactory.ru/my_pets')
    
    # elts = driver.find_elements(By.XPATH, '//div[@title="Удалить питомца"]')
    elts = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@title="Удалить питомца"]')))
    total_pets = len(elts)

    # elts = driver.find_elements(By.XPATH, '//img[@style="max-width: 100px; max-height: 100px;"]')
    elts = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//img[@style="max-width: 100px; max-height: 100px;"]')))
    pets_w_photo = len(elts)

    assert total_pets/pets_w_photo <= 2

def test_all_pets_have_attributes(driver):
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    # elts = driver.find_elements(By.XPATH, '//div[@title="Удалить питомца"]')
    elts = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@title="Удалить питомца"]')))
    total_pets = len(elts)

    # elts = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')
    elts = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')))

    names_num = 0
    for elt in elts:
        if elt.text != "":
            names_num += 1
    
    # elts = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[2]')
    elts = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[2]')))

    breeds_num = 0
    for elt in elts:
        if elt.text != "":
            breeds_num += 1


    # elts = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[3]')
    elts = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[3]')))

    ages_num = 0
    for elt in elts:
        if elt.text != "":
            ages_num += 1

    assert total_pets == names_num == breeds_num == ages_num

def test_all_pets_have_different_names(driver):
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    # elts = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')
    elts = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')))
    
    names = []
    for elt in elts:
        names.append(elt.text)

    match_ = False
    for name in names:
        for name1 in names:
            if name == name1:
                match_ = True

    assert match_ == False
