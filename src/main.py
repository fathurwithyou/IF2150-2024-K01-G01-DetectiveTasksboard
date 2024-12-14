import flet as ft
from sidebar import create_sidebar
from dashboard_page import dashboard_content
from cases_page import cases_content
from victims_page import victims_content
from suspects_page import suspects_content
from detectives_page import detectives_content

def main(page: ft.Page):
    page.title = "Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10

    # Function to handle navigation
    def on_navigate(page_name):
        page.controls.clear()  # Clear the current content
        sidebar = create_sidebar(on_navigate)
        if page_name == "dashboard":
            page.add(ft.Row([sidebar, ft.VerticalDivider(width=1), dashboard_content(page)], expand=True))
            page.update()
        elif page_name == "cases":
            page.add(ft.Row([sidebar, ft.VerticalDivider(width=1), cases_content(page)], expand=True))
            page.update()
        elif page_name == "victims":
            page.add(ft.Row([sidebar, ft.VerticalDivider(width=1), victims_content(page)], expand=True))
            page.update()
        elif page_name == "suspects":
            page.add(ft.Row([sidebar, ft.VerticalDivider(width=1), suspects_content(page)], expand=True))
            page.update()
        elif page_name == "detectives":
            page.add(ft.Row([sidebar, ft.VerticalDivider(width=1), detectives_content(page)], expand=True))
            page.update()

    # Initialize to Dashboard
    on_navigate("dashboard")

ft.app(target=main)