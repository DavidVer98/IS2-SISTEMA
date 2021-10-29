

import undetected_chromedriver.v2 as uc
import random,time,os,sys
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.action_chains import ActionChains
import unittest
from pathlib import Path
import shutil
unittest.TestLoader.sortTestMethodsUsing = None


class Test_funcional(StaticLiveServerTestCase):

    def setUp(self):
        if(os.path.exists('./chrome_profile')):
            shutil.rmtree('./chrome_profile')
        os.mkdir('./chrome_profile')
        Path('./chrome_profile/First Run').touch()
        chrome_options = uc.ChromeOptions()

        chrome_options.add_argument('--user-data-dir=./chrome_profile/')

        chrome_options.add_argument("--disable-extensions")

        chrome_options.add_argument("--disable-popup-blocking")

        chrome_options.add_argument("--profile-directory=Default")

        chrome_options.add_argument("--ignore-certificate-errors")

        chrome_options.add_argument("--disable-plugins-discovery")

        chrome_options.add_argument("--incognito")

        chrome_options.add_argument("user_agent=DN")

        self.driver = uc.Chrome(options=chrome_options)
        self.driver.delete_all_cookies()

    def login(self,GMAIL,PASSWORD):
        self.driver.get('http://127.0.0.1:8080/')
        self.driver.maximize_window()
        self.driver.find_element_by_id('google-connect').click()
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(
            GMAIL)
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(
            Keys.RETURN)
        time.sleep(1)
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input").send_keys(
            PASSWORD)
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input").send_keys(
            Keys.RETURN)


    def ingresarAproyecto(self):
        time.sleep(1)
        self.driver.find_element_by_xpath("/html/body/div[1]/ul/li[4]/a").click()  # entrar a lista de proyectos
        time.sleep(1)
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div/div/table/tbody[2]/tr/td[4]/button[2]").click()  # ingresar a un proytecyo
        time.sleep(1)

    def ingresarproyectodeveloper(self):
        time.sleep(1)
        self.driver.find_element_by_xpath("/html/body/div[1]/ul/li[4]/a").click()  # entrar a lista de proyectos
        time.sleep(1)
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/table/tbody[2]/tr/td[4]/button').click()
        time.sleep(1)
    def test_1_crearproyecto(self):
        # python manage.py test desarrollo.tests.test_views.Test_funcional.test_1_crearproyecto
        GMAIL = 'marioaptobenitez@gmail.com'
        PASSWORD = 'aptobenitez69'
        try:
            self.login(GMAIL,PASSWORD)
            time.sleep(1)
            self.driver.find_element_by_xpath("/html/body/div[1]/ul/li[4]/a").click()  # entrar a lista de proyectos
            time.sleep(1)
            self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/button").click() #boton de crear proyecyo
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="id_nombre_proyecto"]').send_keys("Proyecto de Prueba")
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="id_descripcion"]').send_keys("Descripcion para el proyecto de prueba")
            time.sleep(1)

            self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/form/div[3]/select/option[4]').click() #seleccionar scrum
            time.sleep(2)
            self.driver.find_element_by_xpath('//*[@id="id_fecha_inicio"]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/form/button').click()
            time.sleep(2)
            self.driver.close()
        except:
            print("Error ")
            time.sleep(1)
            self.driver.close()
        # python manage.py test desarrollo.tests.test_views.Test_funcional.test_1_crearproyecto

    # def test_2_añadir_miembro(self):
    #     # python manage.py test desarrollo.tests.test_views.Test_funcional.test_2_añadir_miembro
    #     GMAIL = 'chapiparrizo@gmail.com'
    #     PASSWORD = 'panchicarrizo'
    #     try:
    #         self.login(GMAIL,PASSWORD)
    #         self.ingresarAproyecto()
    #         self.driver.find_element_by_xpath('/html/body/div[1]/ul/li[5]/a').click() #ir a pestaña miembros
    #         time.sleep(2)
    #         self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/button').click()# boton añadir miembro
    #         time.sleep(2)
    #         self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/form/div[1]/select/option[3]').click()
    #         time.sleep(2)
    #         self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/form/div[2]/select/option[2]').click() #asignar rol de developer
    #         time.sleep(2)
    #         self.driver.find_element_by_xpath('//*[@id="id_produccion_diaria"]').clear()
    #         self.driver.find_element_by_xpath('//*[@id="id_produccion_diaria"]').send_keys(5)
    #         time.sleep(2)
    #         self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/form/button').click()
    #         time.sleep(3)
    #         self.driver.close()
    #     except:
    #         print("Error")
    #         time.sleep(1)
    #         self.driver.close()
    #     # python manage.py test desarrollo.tests.test_views.Test_funcional.test_2_añadir_miembro

    # def test_3_iniciar_proyecto(self):
    #     # python manage.py test desarrollo.tests.test_views.Test_funcional.test_3_iniciar_proyecto
    #     GMAIL = 'chapiparrizo@gmail.com'
    #     PASSWORD = 'panchicarrizo'
    #     try:
    #         self.login(GMAIL,PASSWORD)
    #         self.ingresarAproyecto()
    #         self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[2]/button').click() #boton iniciar proyecto
    #         time.sleep(1)
    #         self.driver.close()
    #     except:
    #         print("Error")
    #         time.sleep(1)
    #         self.driver.close()
    #     # python manage.py test desarrollo.tests.test_views.Test_funcional.test_3_iniciar_proyecto

    def test_4_añadir_us(self):
        # python manage.py test desarrollo.tests.test_views.Test_funcional.test_4_añadir_us
        GMAIL = 'chapiparrizo@gmail.com'
        PASSWORD = 'panchicarrizo'
        try:
           self.login(GMAIL,PASSWORD)
           self.ingresarAproyecto()
           self.driver.find_element_by_xpath('/html/body/div[1]/ul/li[4]/a').click()  #boton para ir la modulo de desrrollo
           time.sleep(1)
           self.driver.find_element_by_xpath('/html/body/div[1]/ul/li[7]/a').click()  # boton para entrar en el product backlog
           time.sleep(1)
           self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/div/div[2]/button').click()  #boton para crear us
           time.sleep(1)
           self.driver.find_element_by_xpath('//*[@id="id_nombre"]').send_keys('US1 para test')   #nombre del us
           time.sleep(1)
           self.driver.find_element_by_xpath('//*[@id="id_descripcion"]').send_keys('Historia de usuario')  #descripcion del us
           time.sleep(1)
           self.driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[3]/select/option[2]').click() #establecer prioridad
           time.sleep(1)
           self.driver.find_element_by_xpath('/html/body/div[2]/div/div/form/button').click()  #confirmar creacion
           time.sleep(2)
           self.driver.close()
        except:
            print("Error")
            self.driver.close()
        # python manage.py test desarrollo.tests.test_views.Test_funcional.test_4_añadir_us

    def test_5_sprintplanning1(self):
        # python manage.py test desarrollo.tests.test_views.Test_funcional.test_5_sprintplanning1
        GMAIL = 'chapiparrizo@gmail.com'
        PASSWORD = 'panchicarrizo'
        try:
            self.login(GMAIL, PASSWORD)
            self.ingresarAproyecto()
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/ul/li[4]/a').click()          #ir a modulo de desarrollo

            time.sleep(1)
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/ul/li[7]/a').click()  # boton para entrar en el product backlog
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div/div[1]/div/table/tbody[2]/tr/td[4]/button[1]').click()  #enviar us al sprint planning
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/ul/li[6]/a').click()  #ir al sprint planning
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[1]/div[1]/div/table/tbody/tr/td[5]/button[1]').click()  # boton para comenzar el proceso de asignacion us a miembro
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div/form/div/select/option[2]' ).click() #se elige al usuario
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div/form/button').click()     # confirmar la asginacion
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[1]/div[1]/div/table/tbody/tr/td[5]/button[2]'  ).click()   #el scrum comienza el proceso de plannign poker
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//*[@id="id_estimacion_scrum"]').clear()
            self.driver.find_element_by_xpath(
                '//*[@id="id_estimacion_scrum"]').send_keys(10)     #se rellena el campo
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div/form/button' ).click()    #se confirma la estimacion del scrum
            time.sleep(1)
            self.driver.close()
        except:
            print("Error")
            self.driver.close()
        # python manage.py test desarrollo.tests.test_views.Test_funcional.test_5_sprintplanning1

    def test_6_sprintplanning2(self):
        # python manage.py test desarrollo.tests.test_views.Test_funcional.test_6_sprintplanning2
        GMAIL = 'pistoleronani1912@gmail.com'
        PASSWORD = 'pistola19'
        try:
            self.login(GMAIL, PASSWORD)
            self.ingresarproyectodeveloper()
            time.sleep(1)

            time.sleep(1)
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/ul/li[6]/a').click()  #ir al sprint planning
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[1]/div[1]/div/table/tbody/tr/td[5]/button').click()  #el developer comienza el continua con el proceso de estimacion
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//*[@id="id_estimacion_miembro"]').clear()
            self.driver.find_element_by_xpath(
                '//*[@id="id_estimacion_miembro"]').send_keys(10)   #el developer completa su estimacion
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '/html/body/div[2]/div/div/form/button').click()    # se confirma la estimacion
            self.driver.refresh()
            time.sleep(2)
            self.driver.close()

        except:
            print("Error")
            time.sleep(1)
            self.driver.close()
            # python manage.py test desarrollo.tests.test_views.Test_funcional.test_6_sprintplanning2
    # def test_7_iniciarSprint(self):
    #     # python manage.py test desarrollo.tests.test_views.Test_funcional.test_7_iniciarSprint
    #     GMAIL = 'chapiparrizo@gmail.com'
    #     PASSWORD = 'panchicarrizo'
    #     try:
    #         self.login(GMAIL, PASSWORD)
    #         self.ingresarAproyecto()
    #         time.sleep(1)
    #         self.driver.find_element_by_xpath(
    #             '/html/body/div[1]/ul/li[4]/a').click()  # ir a modulo de desarrollo
    #         time.sleep(1)
    #         self.driver.find_element_by_xpath(
    #             '/html/body/div[1]/ul/li[6]/a').click()  # ir al sprint planning
    #         time.sleep(1)
    #         self.driver.find_element_by_xpath(
    #             '/html/body/div[2]/div/div[1]/div[1]/div/div/div[2]/button').click()
    #         time.sleep(2)
    #         self.driver.close()
    #
    #     except:
    #         print("Error")
    #         time.sleep(1)
    #         self.driver.close()
    #     # python manage.py test desarrollo.tests.test_views.Test_funcional.test_7_iniciarSprint
    def test_8_añadirregistro(self):
        # python manage.py test desarrollo.tests.test_views.Test_funcional.test_8_añadirregistro
        GMAIL = 'pistoleronani1912@gmail.com'
        PASSWORD = 'pistola19'
        try:
            self.login(GMAIL,PASSWORD)
            self.ingresarproyectodeveloper()
            self.driver.find_element_by_xpath("/html/body/div[1]/ul/li[5]/a").click()   #ir a tablero kamban
            time.sleep(1)

            self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/div[3]/a[1]").click()  #Agregar registro
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="id_detalles"]').send_keys("Se registran las 3 horas trabajadas en el dia")
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="id_horas_trabajadas"]').clear()
            self.driver.find_element_by_xpath('//*[@id="id_horas_trabajadas"]').send_keys(3)
            time.sleep(1)
            self.driver.find_element_by_xpath("/html/body/div[2]/div/div/form/button").click()
            time.sleep(2)
            self.driver.close()
        except:
            self.assertEqual(1,0,"No se cumplio el flujo de eventos")
            time.sleep(1)
            self.driver.close()
        # python manage.py test desarrollo.tests.test_views.Test_funcional.test_8_añadirregistro

    def test_9_verBC(self):
        # python manage.py test desarrollo.tests.test_views.Test_funcional.test_9_verBC
        GMAIL = 'chapiparrizo@gmail.com'
        PASSWORD = 'panchicarrizo'
        GMAIL = 'chapiparrizo@gmail.com'
        PASSWORD = 'panchicarrizo'
        try:
            self.login(GMAIL, PASSWORD)
            self.ingresarAproyecto()
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/ul/li[4]/a').click()  # boton para ir la modulo de desrrollo
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/ul/li[10]/a').click()
            time.sleep(1)
            self.driver.close()
        except:
            self.assertEqual(1, 0, "No se cumplio el flujo de eventos")
            time.sleep(1)
            self.driver.close()
        # python manage.py test desarrollo.tests.test_views.Test_funcional.test_9_verBC