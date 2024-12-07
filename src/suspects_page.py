
import flet as ft
from victims_page import victims_content  # Reuse victims table

def suspects_content():
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Suspects", size=30, weight=ft.FontWeight.BOLD),
                ft.TextField(label="Search Suspects...", width=300),
                victims_content().content,  # Reuse Victims table
            ]
        ),
        expand=True,
        padding=20,
    )
