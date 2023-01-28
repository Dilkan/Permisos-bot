from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

# Inicializar el navegador
driver = webdriver.Chrome()

# Iniciar sesión en http://gesdepor.dipusevilla.es/login
driver.get("http://gesdepor.dipusevilla.es/login")

# Ingresar el nombre de usuario y la contraseña
usuario = "xxxxx"
contraseña = "xxxxx"

# Encontrar el elemento <input type="text" class="form-control input-lg ng-pristine ng-valid" placeholder="Login o email" ng-model="login" autofocus="">
wait = WebDriverWait(driver, 10)
usuario_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control.input-lg[placeholder='Login o email'][ng-model='login']")))

# Encontrar el elemento <input type="password" class="form-control input-lg ng-pristine ng-valid" placeholder="Contraseña" ng-model="password">
contraseña_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control.input-lg[placeholder='Contraseña'][ng-model='password']")))

# Enviar el nombre de usuario y la contraseña
usuario_input.send_keys(usuario)
contraseña_input.send_keys(contraseña)

# Encontrar el elemento <span ng-show="!logging" class="">Entrar</span>
entrar_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[ng-show='!logging']")))

# Hacer clic en el botón Entrar
entrar_button.click()

# Navegar a la página de reserva pasado 1 segundo
reserva_url = "http://gesdepor.dipusevilla.es/timetable/11694#date=2023-02-09&g=286371"
sleep(0.5)
driver.get(reserva_url)


# Esperar a que el elemento <div class="piece FREE" style="height:60px" ng-repeat="piece in field.pieces[date]" ng-click="goOperate(field, piece)"> esté disponible
# si no esta disponible en 2 segundos, actualizar la página y volver a intentar. Si esta disponible, hacer clic en el elemento
wait = WebDriverWait(driver, 1)
refresh_count = 0
while True:
    try:
        reservation_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.piece.FREE[ng-repeat='piece in field.pieces[date]'][ng-click='goOperate(field, piece)']")))
        reservation_div.click()
        print("Elemento encontrado")
        break
    except TimeoutException:
        refresh_count += 1
        if refresh_count >= 5:
            driver.close()
            print("Elemento no encontrado después de 5 actualizaciones. Cerrando navegador y deteniendo script.")
            exit()
        driver.refresh()

# Buscar el boton alquilar y si no lo encuentra cerrar el navegador y dejar un mensaje en la consola y cerrar el script
try:
# El boton es <a ng-href="/user/booking&amp;f=8755&amp;d=2023-02-02&amp;t1=20:00&amp;t2=21:00" class="btn btn-primary form-control" ng-show="ImUser" href="/user/booking&amp;f=8755&amp;d=2023-02-02&amp;t1=20:00&amp;t2=21:00"><span class="btn-addon glyphicon glyphicon-calendar"></span>&nbsp;Alquilar</a>
    alquilar_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[ng-href='/user/booking&f=8755&d=[0-9]{4}-[0-1][0-9]-[0-3][0-9]&t1=20:00&t2=21:00'][ng-show='ImUser']")))
    alquilar_button.click()
except:
    driver.quit()
    print("No se encontró el botón alquilar")
    exit()


# Esperar 5 segundos a cerrar el navegador
sleep(5)

# Salir del navegador
driver.quit()
# Salir del script
exit()