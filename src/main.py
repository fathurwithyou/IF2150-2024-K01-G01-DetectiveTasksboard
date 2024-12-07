import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HTML Viewer with Sidebar")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        self.browser = QWebEngineView()
        self.browser.setZoomFactor(1.25)  
        self.setCentralWidget(self.browser)

        # Load the main HTML and inject the sidebar
        html_content = self.load_html_with_sidebar(
            "components/cases/index.html",
            "components/sidebar/index.html",
            "components/cases/style.css"
        )
        self.browser.setHtml(html_content)

    def load_html_with_sidebar(self, html_path, sidebar_path, css_path):
        # Read the main HTML content
        with open(html_path, 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()

        # Read the sidebar HTML content
        with open(sidebar_path, 'r', encoding='utf-8') as sidebar_file:
            sidebar_content = sidebar_file.read()

        # Read the CSS content
        with open(css_path, 'r', encoding='utf-8') as css_file:
            css_content = css_file.read()

        # Replace the placeholder for the sidebar with the actual sidebar content
        html_with_sidebar = html_content.replace(
            '<div id="sidebar"></div>',
            sidebar_content
        )

        # Inline the CSS in the HTML <style> tag
        inlined_html = html_with_sidebar.replace(
            "</head>", f"<style>{css_content}</style></head>"
        )

        return inlined_html


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
