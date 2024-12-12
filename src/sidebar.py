import flet as ft

def create_sidebar(on_navigate):
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Detective Tasksboard", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.DASHBOARD),
                    title=ft.Text("Dashboard"),
                    on_click=lambda _: on_navigate("dashboard"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.CASES),
                    title=ft.Text("Cases"),
                    on_click=lambda _: on_navigate("cases"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.PERSON_SEARCH),
                    title=ft.Text("Suspects"),
                    on_click=lambda _: on_navigate("suspects"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.GROUP),
                    title=ft.Text("Victims"),
                    on_click=lambda _: on_navigate("victims"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.BADGE),
                    title=ft.Text("Detectives"),
                    on_click=lambda _: on_navigate("detectives"),
                ),
            ]
        ),
        width=200,
        bgcolor=ft.colors.SURFACE_VARIANT,
        padding=10,
    )
