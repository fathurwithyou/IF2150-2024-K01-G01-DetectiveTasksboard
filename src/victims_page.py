import flet as ft
import csv
import math


def victims_content():
    # Read data from the CSV file using the csv library
    data = []
    with open("data/victims.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)

    # Variables for pagination and search
    rows_per_page = 10
    current_page = 0  # Start from page 0
    total_pages = math.ceil(len(data) / rows_per_page)  # Calculate total pages
    filtered_data = data  # Holds the filtered data based on search

    # Function to build the data table for the current page
    def build_table(page):
        start_index = page * rows_per_page
        end_index = start_index + rows_per_page
        page_data = filtered_data[start_index:end_index]

        table_rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(row["id"])),               # ID
                    ft.DataCell(ft.Text(row["nama"])),             # Name
                    ft.DataCell(ft.Text(row["foto"])),             # Photo
                    ft.DataCell(ft.Text(row["nik"])),              # NIK
                    ft.DataCell(ft.Text(row["usia"])),             # Usia
                    ft.DataCell(ft.Text(row["jk"])),               # Gender
                    ft.DataCell(ft.Text(row["hasil_forensik"])),   # Forensic Results
                    ft.DataCell(ft.Text(row["id_kasus"])),         # Case ID
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            icon_color="white",
                            tooltip="Edit",
                            on_click=lambda e, r=row: print(f"Edit clicked for {r['nama']}"),
                        )
                    ),                                             # Edit Button
                ]
            )
            for row in page_data
        ]
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Photo")),
                ft.DataColumn(ft.Text("NIK")),
                ft.DataColumn(ft.Text("Usia")),
                ft.DataColumn(ft.Text("Gender")),
                ft.DataColumn(ft.Text("Forensic Results")),
                ft.DataColumn(ft.Text("Case ID")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=table_rows,
        )

    # Function to update the content when a page is changed
    def update_content(page):
        nonlocal current_page, total_pages
        current_page = page  # Update the current page
        total_pages = math.ceil(len(filtered_data) / rows_per_page)  # Recalculate total pages for filtered data
        table_container.content = build_table(page)  # Update the table
        pagination_controls.controls[1].value = f"Page {page + 1} of {total_pages}"  # Update the page display
        pagination_controls.controls[0].disabled = current_page == 0  # Disable previous button
        pagination_controls.controls[2].disabled = current_page == total_pages - 1  # Disable next button
        container.update()

    # Function to handle search input so that the table is updated with the filtered data
    def handle_search(e):
        nonlocal filtered_data, current_page
        search_term = e.control.value.lower()
        # Exclude "foto" from search
        filtered_data = [
            row for row in data
            if any(
                search_term in str(value).lower()
                for key, value in row.items()
                if key != "foto"
            )
        ]
        current_page = 0  # Reset to first page after search
        update_content(current_page)

    # Pagination controls
    pagination_controls = ft.Row(
        [
            ft.IconButton(
                ft.icons.CHEVRON_LEFT,
                on_click=lambda _: update_content(current_page - 1),
                disabled=current_page == 0,
            ),
            ft.Text(value=f"Page 1 of {total_pages}", size=18),  # Page X of Y display
            ft.IconButton(
                ft.icons.CHEVRON_RIGHT,
                on_click=lambda _: update_content(current_page + 1),
                disabled=current_page == total_pages - 1,
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
                # "Victims" title
                ft.Text("Victims", size=30, weight=ft.FontWeight.BOLD, color="white"),
                # Row containing the search field and the button
                ft.Row(
                    [
                        ft.TextField(
                            label="Search Victims...",
                            width=300,
                            on_change=handle_search,  # Triggered when search input changes
                        ),
                        ft.ElevatedButton(
                            text="Add Victim",
                            icon=ft.icons.ADD,
                            on_click=lambda _: print("Add Victim button clicked"),
                            bgcolor="white",
                            color="black",
                        ),  # Add Victim button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                table_container,  # Initial table for page 0
                pagination_controls,  # Add pagination controls
            ]
        ),
        expand=True,
        padding=20,
    )

    return container
