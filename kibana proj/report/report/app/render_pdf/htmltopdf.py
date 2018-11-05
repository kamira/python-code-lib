# -*- coding: utf-8 -*-
#USING UTF-8

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
from io import BytesIO
import tempfile
from fpdf import FPDF
import string
import random

title = 'Network Report'

# PDF Width = 210
class PDF(FPDF):
    def header(self):
        # Logo
        self.image('logo-zyxel.png', 10, 7, 20)
        # Arial bold 15
        self.set_font('Arial', 'B', 20)
        # Move to the right
        # Title
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        self.cell(w, 1, title, 0, 0, 'C')
        self.line(10, self.get_y()+5, 200, self.get_y()+5)
        # Line break
        self.ln(10)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def pdf_generator(url):
    print(url)
    pdf = PDF()
    pdf.add_font('notosanscjktc', '', 'NotoSansCJKtc-Regular.ttf', uni=True)
    img_path = 'report.png'
    pdf_path = "report.pdf"

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # chrome_options.binary_location = 'chromedriver.exe'
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 1000)
        wait.until(lambda driver: driver.current_url != url)
        wait.until(lambda driver: driver.find_element_by_tag_name('svg'))
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        driver.set_window_size(1000, int(total_height))
        sleep(5)
        js = '''
        var x = document.getElementsByClassName('visualize-chart');
        var y = document.getElementsByClassName('panel-title');
        for(var i = x.length-1; i >= 0; --i){
            if(x[i].offsetTop > 10){
                x[i].remove();
            }
        }
        var arr = [];
        for(var i = 0;i < x.length; i++){
            dict = {};
            if (x[i].getElementsByClassName('visualize-error').length > 0) {
                continue;
            }
            if (y[i].getElementsByClassName('table-vis-error').length > 0) {
                continue;
            }
            dict['title'] = y[i].innerText;  
            dict['rect'] = x[i].getBoundingClientRect();
            arr.push(dict);
        }
        return arr;
        '''
        test = driver.execute_script(js)
        sleep(10)
        png = driver.get_screenshot_as_png()

        driver.quit()
    except Exception:
        driver.quit()
        return 'Failed'
    # Instantiation of inherited class
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('notosanscjktc', '', 12)
    with tempfile.TemporaryDirectory() as tmp_dir:
        print(tmp_dir)
        for i in range(len(test)):
            im = Image.open(BytesIO(png))
            # defines crop points
            im = im.crop((test[i]['rect']['left'], test[i]['rect']['top'], test[i]['rect']['right'], test[i]['rect']['bottom']))
            im.save('{}/{}-{}.png'.format(tmp_dir, i, test[i]['title']))
            pdf.cell(0, 10, test[i]['title'], 0, 1)
            pdf.image('{}/{}-{}.png'.format(tmp_dir, i, test[i]['title']), w=190)
            pdf.ln(4)

    pdf_name = 'report_{}.pdf'.format(id_generator())
    pdf.output(dest='F', name=pdf_name)
    return pdf_name
