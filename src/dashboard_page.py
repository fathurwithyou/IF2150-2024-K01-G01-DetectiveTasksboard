import flet as ft

def dashboard_content():
    def create_case_tile(case_id, case_type, time, date):
        return ft.ListTile(
            leading=ft.Icon(ft.icons.BOOKMARK),
            title=ft.Text(f"Case #{case_id}"),
            subtitle=ft.Text(f"{case_type}, {time}, {date}"),
            trailing=ft.IconButton(ft.icons.MORE_VERT),
        )

    cases = [
        create_case_tile(123, "Robbery", "2pm", "23rd May"),
        create_case_tile(124, "Murder", "5am", "25th May"),
        create_case_tile(125, "Kidnapping", "3pm", "26th May"),
        create_case_tile(126, "Arson", "4pm", "27th May"),
    ]

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Ongoing Cases"),
                *cases,
            ],
        ),
        expand=True,
        padding=20,
    )
