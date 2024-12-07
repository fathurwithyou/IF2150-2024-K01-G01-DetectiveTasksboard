import flet as ft

def cases_content():
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Cases Page", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("This page contains details about cases."),
            ],
        ),
        expand=True,
        padding=20,
    )
