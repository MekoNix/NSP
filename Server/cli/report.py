from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from Server.cli.server_modules import *
from Scripts.modules import *



def create_pdf_report(host, date, key_value_pairs, filename):
    # Регистрация шрифта Consolas
    pdfmetrics.registerFont(TTFont('Consolas', filename=find_path("consolas.ttf")))
    addMapping('Consolas', 0, 0, 'Consolas')

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Установка заголовка
    c.setFont("Helvetica-Oblique", 18)
    c.drawCentredString(width / 2, height - 30, f"SCAN REPORT FOR {host}")

    # Установка шрифта Consolas для остального текста
    c.setFont("Consolas", 12)

    # Установка Host и Date
    c.drawString(50, height - 60, f"Host: {host}")
    c.drawString(400, height - 60, f"Date: {date}")

    # Начальная позиция Y для пар ключ-значение
    y_position = height - 120

    # Рисование полей ключ-значение
    for key, value in key_value_pairs.items():
        # Установка красного цвета для выделения
        c.setStrokeColor(colors.red)
        c.drawString(50, y_position, f"{key}:")
        text = c.beginText(50, y_position)
        text.setFont("Consolas", 12)
        text.textLines(f"{key}:\n{value}")
        c.drawText(text)

        y_position -= 100  # Регулировка позиции Y для следующей пары ключ-значение

    # Сохранение PDF файла
    c.save()





# Создание PDF отчета
create_pdf_report(host_name, current_date, key_value_data, output_filename)

print(f"PDF отчет успешно создан: {output_filename}")
