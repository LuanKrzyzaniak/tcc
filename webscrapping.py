import os
import time
import glob

from selenium import webdriver
from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

DOWNLOAD_DIR = r"C:\Users\luan_\Documents\tcc\output\webscrapping"

def main():
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", DOWNLOAD_DIR)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    options.set_preference("pdfjs.disabled", True)

    # Setup webdriver
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()

    os.makedirs("output/", exist_ok=True)

    TIMEOUT = 10
    startId = 253734
    number = 1

    try:
        while startId > 1:
            for tentativa in range(5):
                try:
                    Url = "https://contratos.sistema.gov.br/transparencia/arpshow/" + str(startId) + "/show"

                    print(f"Baixando arquivo nº {number} da URL {startId}")
                    # Abre a página
                    driver.get(Url)
                    time.sleep(1)

                    Button = WebDriverWait(driver, TIMEOUT).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[@title='Baixar arquivo']"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", Button)
                    Button.click()
                    
                    time.sleep(2)  # espera o download terminar

                    # Pega o último arquivo PDF da pasta
                    arquivos = glob.glob(os.path.join(DOWNLOAD_DIR, "*.pdf"))
                    if not arquivos:
                        print(f"Download do ID {startId} falhou.")
                    else:
                        arquivo_baixado = max(arquivos, key=os.path.getctime)
                        novo_nome = os.path.join(DOWNLOAD_DIR, f"{startId}.pdf")
                        os.rename(arquivo_baixado, novo_nome)
                        print(f"Renomeado para: {novo_nome}")

                    break
                except (StaleElementReferenceException, TimeoutException) as e:
                    if isinstance(e, StaleElementReferenceException):
                        tipo_erro = "stale"
                    else:
                        tipo_erro = "timeout"
                    print(f"Tentativa {tentativa+1} falhou: elemento deu {tipo_erro}.")

            number += 1
            startId -= 1


    finally:
        # Fecha o navegador
        driver.quit()

if __name__ == "__main__":
    main()