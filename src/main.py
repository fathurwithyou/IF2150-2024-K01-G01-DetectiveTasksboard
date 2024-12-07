import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject, pyqtSlot


class Bridge(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    @pyqtSlot(str, str)
    def navigate(self, html_path, css_path):
        """Navigate to a new page."""
        self.main_window.load_page(html_path, css_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HTML Viewer with Sidebar")
        self.setGeometry(100, 100, 800, 600)

        # Initialize the web engine view
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # Initialize the web channel and bridge
        self.channel = QWebChannel()
        self.bridge = Bridge(self)
        self.channel.registerObject("bridge", self.bridge)
        self.browser.page().setWebChannel(self.channel)

        # Load the initial page (Cases page)
        self.load_page("components/cases/index.html", "components/cases/style.css")

    def load_page(self, html_path, css_path=None):
        # Load the sidebar content
        with open("components/sidebar/index.html", "r", encoding="utf-8") as sidebar_file:
            sidebar_content = sidebar_file.read()

        # Load the main page content
        with open(html_path, "r", encoding="utf-8") as file:
            main_content = file.read()

        # Inject the sidebar into the main content
        final_content = main_content.replace(
            "<body>", f"<body>\n<div id='sidebar'>{sidebar_content}</div>"
        )

        # Inject CSS if provided
        if css_path:
            with open(css_path, "r", encoding="utf-8") as css_file:
                css_content = css_file.read()
            css_tag = f"<style>{css_content}</style>"
            final_content = final_content.replace("</head>", f"{css_tag}</head>")

        # First, include the QWebChannel JavaScript API
        final_content = final_content.replace(
            "</head>",
            '<script src="qrc:///qtwebchannel/qwebchannel.js"></script></head>'
        )

        # Modified JavaScript for navigation handling with proper WebChannel initialization
        js_script = """
            // Wait for the document to load
            document.addEventListener('DOMContentLoaded', () => {
                // Initialize the WebChannel
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    // Get the bridge object
                    const bridge = channel.objects.bridge;
                    
                    const links = {
                        "dashboard-link": ["components/dashboard/index.html", "components/dashboard/style.css"],
                        "cases-link": ["components/cases/index.html", "components/cases/style.css"],
                        "suspects-link": ["components/suspect/index.html", "components/suspects/style.css"],
                        "victims-link": ["components/victims/index.html", "components/victims/style.css"],
                        "detectives-link": ["components/detective/index.html", "components/detectives/style.css"],
                        "settings-link": ["components/settings/index.html", "components/settings/style.css"]
                    };

                    // Add click handlers once bridge is available
                    Object.keys(links).forEach(id => {
                        const link = document.getElementById(id);
                        if (link) {
                            link.addEventListener('click', () => {
                                const [htmlPath, cssPath] = links[id];
                                bridge.navigate(htmlPath, cssPath);
                            });
                        }
                    });
                });
            });
        """
        final_content += f"<script>{js_script}</script>"

        # Load the final content into the browser
        self.browser.setHtml(final_content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())