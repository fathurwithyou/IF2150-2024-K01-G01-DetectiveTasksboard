import flet as ft
from victims_page import victims_content  # Reuse victims table

def detectives_content():
    data = [
        {"name": "Jane Doe", "case": "Case 1", "dob": "01/01/1990", "phone": "123-456-7890"},
        {"name": "John Doe", "case": "Case 2", "dob": "02/02/1990", "phone": "234-567-8901"},
        {"name": "Doe Jane", "case": "Case 3", "dob": "03/03/1990", "phone": "345-678-9012"},
        {"name": "Doe John", "case": "Case 4", "dob": "04/04/1990", "phone": "456-789-0123"},
        {"name": "J Doe", "case": "Case 5", "dob": "05/05/1990", "phone": "567-890-1234"},
    ]

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Case")),
            ft.DataColumn(ft.Text("Date of Birth")),
            ft.DataColumn(ft.Text("Phone Number")),
            ft.DataColumn(ft.Text("Actions")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item["name"])),
                    ft.DataCell(ft.Text(item["case"])),
                    ft.DataCell(ft.Text(item["dob"])),
                    ft.DataCell(ft.Text(item["phone"])),
                    ft.DataCell(ft.Text("Edit")),
                ]
            )
            for item in data
        ],
    )
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Detectives", size=30, weight=ft.FontWeight.BOLD),
                ft.TextField(label="Search Detectives...", width=300),
                table,
            ]
        ),
        expand=True,
        padding=20,
    )
