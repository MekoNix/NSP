import os
from datetime import datetime

# Пример использования:
# Создание и сохранение HTML-страницы
# page = HTMLPageModifier("My Web Page")
# page.add_text_block("This is a small text block.",font_weight="bold")
# page.add_large_center_text("This is a large text centered on the page.")
# page.save_to_file(find_path("app",ndir=1)+"/test.html")

# Очистка содержимого класса для создания новой страницы
# page.clear_content()



class HTMLPageModifier:
    def __init__(self, title, background_color="#808080"):
        self.title = title
        self.body_content = []
        self.background_color = background_color

    def create_base_page(self):
        base_style = (
            "<style>"
            "body {"
            f"  background-color: {self.background_color};"
            "  font-family: 'Consolas', monospace;"
            "  color: #333333;"
            "}"
            ".center-text {"
            "  text-align: center;"
            "  margin: 20px;"
            "}"
            "hr {"
            "  border: none;"
            "  height: 2px;"
            "  background-color: #333;"
            "}"
            "</style>"
        )
        return f"""<!DOCTYPE html>
        <html>
        <head>
            <title>{self.title}</title>
            {base_style}
        </head>
        <body>
        {''.join(self.body_content)}
        </body>
        </html>"""

    def add_text_block(self, text, text_color="#D3D3D3",font_weight="normal"):
        self.body_content.append(f'<p style="color: {text_color}; font-weight: {font_weight}">{text}</p>')

    def add_large_center_text(self, text, text_color="#D3D3D3"):
        self.body_content.append(f'<div class="center-text"><p style="color: {text_color};">{text}</p></div>')

    def add_header(self, scan_host, created_by, color="#D3D3D3"):
        scan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header_content = (
            f"Scan date: {scan_date}<br>Scan host: {scan_host}<br>"
            f"Created by: {created_by}"
        )
        self.body_content.insert(0, f'<div class="scan-header" style="color: {color};">{header_content}<hr></div>')

    def save_to_file(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        html_content = self.create_base_page()
        with open(filepath, 'w',encoding='utf-8') as f:
            f.write(html_content)

    def clear_content(self):
        self.body_content = []

    def add_download_link(self, pdf_file_path, link_text="Download PDF"):
        download_link = f'<a href="{pdf_file_path}" download="{link_text}">{link_text}</a>'
        self.body_content.append(download_link)





