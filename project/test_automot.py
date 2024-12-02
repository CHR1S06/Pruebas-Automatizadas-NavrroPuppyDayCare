import time
import pytest
import subprocess
import pytest_html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


# Configuracion de la fixture para el driver de Selenium
@pytest.fixture
def driver():
    # Configuracion del path del EdgeDriver
    edge_driver_path = r"C:\Users\UserGPC\Downloads\edgedriver_win64\msedgedriver.exe"
    
    # Configuracion de las opciones de Microsoft Edge
    options = EdgeOptions()
    options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  # Path al ejecutable de Edge
    
    # Creacion de instancia del navegador Microsoft Edge
    driver = webdriver.Edge(service=EdgeService(edge_driver_path), options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


# Funcion para guardar capturas de pantalla automáticamente
def take_screenshot(driver, name):
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    path = os.path.join(screenshots_dir, f"{name}.png")
    driver.save_screenshot(path)
    return path


# Hook para agregar capturas de pantalla al reporte HTML si una prueba falla
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Hook para capturar detalles de cada prueba
    outcome = yield
    report = outcome.get_result()

    # Solo actua en pruebas fallidas
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")  # Obtener el driver de la prueba
        if driver:
            screenshot_path = take_screenshot(driver, item.name)
            if screenshot_path:
                # Adjuntar la captura de pantalla al reporte
                report.extra = getattr(report, "extra", [])
                report.extra.append(pytest_html.extras.image(screenshot_path))


# Prueba 1: Verificar que el nombre de la mascota se ingresa correctamente
def test_validate_pet_name(driver):
    driver.get("file:///C:/Users/UserGPC/Documents/Proycto%20Final%20P3/Navro-DayPetCare/index.html")
    time.sleep(5)

    pet_name_input = driver.find_element(By.ID, "petName")
    pet_name_input.clear()
    pet_name_input.send_keys("Rex")

    date_input = driver.find_element(By.ID, "date")
    date_input.send_keys("01-02-2025")

    time_input = driver.find_element(By.ID, "time")
    time_input.send_keys("10:00:am")

    extras_input = driver.find_element(By.ID, "extras")
    extras_input.send_keys("Baño")

    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    time.sleep(2)

    # Verificar el resultado
    alert = driver.switch_to.alert
    alert_text = alert.text
    assert "Cita agendada con éxito." in alert_text, "El nombre de la mascota no se guardó correctamente." 
    alert.accept() 
    take_screenshot(driver, "test_validate_pet_name")


# Prueba 2: Verificar que la fecha es válida
def test_validate_future_date(driver):
    driver.get("file:///C:/Users/UserGPC/Documents/Proycto%20Final%20P3/Navro-DayPetCare/index.html")
    time.sleep(5)

    # Probar fecha atrasada
    pet_name_input = driver.find_element(By.ID, "petName")
    pet_name_input.clear()
    pet_name_input.send_keys("Rex")

    date_input = driver.find_element(By.ID, "date")
    date_input.send_keys("01-12-2024")

    time_input = driver.find_element(By.ID, "time")
    time_input.send_keys("10:00:am")

    extras_input = driver.find_element(By.ID, "extras")
    extras_input.send_keys("Baño")

    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    time.sleep(2)

    
    alert = driver.switch_to.alert
    alert_text = alert.text
    assert "La fecha debe ser hoy o una fecha futura." in alert_text, "La fecha no se guardó correctamente."
    alert.accept()
    take_screenshot(driver, "test_validate_future_date")


# Prueba 3: Verificar que la hora esta dentro del rango permitido
def test_validate_time(driver):
    driver.get("file:///C:/Users/UserGPC/Documents/Proycto%20Final%20P3/Navro-DayPetCare/index.html")
    time.sleep(5)

    # Probar horario fuera de rango
    pet_name_input = driver.find_element(By.ID, "petName")
    pet_name_input.clear()
    pet_name_input.send_keys("Rex")

    date_input = driver.find_element(By.ID, "date")
    date_input.send_keys("06-12-2024")

    time_input = driver.find_element(By.ID, "time")
    time_input.send_keys("07:59:pm")

    extras_input = driver.find_element(By.ID, "extras")
    extras_input.send_keys("Baño")

    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    time.sleep(2)

    alert = driver.switch_to.alert
    alert_text = alert.text
    assert "El horario debe estar dentro del horario laboral" in alert_text, "El mensaje de error no es el esperado."
    alert.accept()
    take_screenshot(driver, "test_validate_time")


# Prueba 4: Validar listado de citas
def test_render_appointments(driver):
    driver.get("file:///C:/Users/UserGPC/Documents/Proycto%20Final%20P3/Navro-DayPetCare/index.html")
    time.sleep(5)

    # Agendamos una cita para que poder ver el listado
    pet_name_input = driver.find_element(By.ID, "petName")
    pet_name_input.clear()
    pet_name_input.send_keys("Rex")

    date_input = driver.find_element(By.ID, "date")
    date_input.send_keys("12-12-2024")

    time_input = driver.find_element(By.ID, "time")
    time_input.send_keys("10:00:am")

    extras_input = driver.find_element(By.ID, "extras")
    extras_input.send_keys("Baño")

    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    time.sleep(1)

    # Verificar que las citas estan siendo renderizadas correctamente
    alert = driver.switch_to.alert
    alert_text = alert.text
    assert "Cita agendada con éxito." in alert_text, "El listado de citas no se muestra correctamente."
    alert.accept()
    take_screenshot(driver, "test_render_appointments")


# Funcion para ejecutar pytest y generar el reporte en HTML
def run_pytest_report():
    subprocess.run(["pytest", "--maxfail=3", "--disable-warnings", "--html=report/test_report.html", "--self-contained-html", "--tb=short"])


if __name__ == "__main__":
    run_pytest_report()
