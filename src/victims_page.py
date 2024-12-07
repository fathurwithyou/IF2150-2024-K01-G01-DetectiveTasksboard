import flet as ft
import csv


def victims_content():
    # Read data from the CSV file using the csv library
    data = []
    with open("data/victims.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)

    # Pagination variables
    rows_per_page = 10
    current_page = 0  # Start from page 0

    # Function to build the data table for the current page
    def build_table(page):
        start_index = page * rows_per_page
        end_index = start_index + rows_per_page
        page_data = data[start_index:end_index]

        table_rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(row["nama"])),
                    ft.DataCell(ft.Text(row["id_kasus"])),
                    ft.DataCell(ft.Text(row["hasil_forensik"])),
                    ft.DataCell(ft.Text(row["nik"])),
                    ft.DataCell(ft.Text("Edit")),
                ]
            )
            for row in page_data
        ]
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Case ID")),
                ft.DataColumn(ft.Text("Forensic Results")),
                ft.DataColumn(ft.Text("NIK")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=table_rows,
        )

    # Function to update the content when a page is changed
    def update_content(page):
        nonlocal current_page
        current_page = page  # Update the current page
        table_container.content = build_table(page)  # Update the table
        pagination_controls.controls[1].value = str(page + 1)  # Update the page number
        pagination_controls.controls[0].disabled = current_page == 0  # Disable previous button
        pagination_controls.controls[2].disabled = (current_page + 1) * rows_per_page >= len(data)  # Disable next button
        container.update()

    # Pagination controls
    pagination_controls = ft.Row(
        [
            ft.IconButton(
                ft.icons.CHEVRON_LEFT,
                on_click=lambda _: update_content(current_page - 1),
                disabled=current_page == 0,
            ),
            ft.Text(value="1", size=18),  # Current page number
            ft.IconButton(
                ft.icons.CHEVRON_RIGHT,
                on_click=lambda _: update_content(current_page + 1),
                disabled=(current_page + 1) * rows_per_page >= len(data),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Table container
    table_container = ft.Container(content=build_table(current_page))

    # Victims container
    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Victims", size=30, weight=ft.FontWeight.BOLD, color="white"),
                ft.TextField(label="Search Victims...", width=300),
                table_container,  # Initial table for page 0
                pagination_controls,  # Add pagination controls
            ]
        ),
        expand=True,
        padding=20,
    )

    return container
