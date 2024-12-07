import flet as ft
import math
from models.victims import Victims


def victims_content(page: ft.Page):
    # Initialize the Victims class
    victims_model = Victims()
    filtered_data = victims_model.get_victims()  # Initialize with all data
    rows_per_page = 10
    current_page = 0  # Start from page 0
    total_pages = math.ceil(len(filtered_data) / rows_per_page)
    sort_column = None  # Column to sort by
    sort_order = "asc"  # Sorting order: 'asc' or 'desc'

    # Modal for adding victims
    modal_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Add Victim"),
        content=None,
        actions=None,
    )

    # Function to build the data table for the current page
    def build_table(page_index):
        start_index = page_index * rows_per_page
        end_index = start_index + rows_per_page
        page_data = filtered_data.iloc[start_index:end_index]  # Use pandas for slicing

        table_rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(row["id"]))),               # ID
                    ft.DataCell(ft.Text(str(row["nama"]))),             # Name
                    ft.DataCell(ft.Text(str(row["foto"]))),             # Photo
                    ft.DataCell(ft.Text(str(row["nik"]))),              # NIK
                    ft.DataCell(ft.Text(str(row["usia"]))),             # Usia
                    ft.DataCell(ft.Text(str(row["jk"]))),               # Gender
                    ft.DataCell(ft.Text(str(row["hasil_forensik"]))),   # Forensic Results
                    ft.DataCell(ft.Text(str(row["id_kasus"]))),         # Case ID
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            icon_color="white",
                            tooltip="Edit",
                            on_click=lambda e, r=row: print(f"Edit clicked for {r['nama']}"),
                        )
                    ),                                                 # Edit Button
                ]
            )
            for _, row in page_data.iterrows()  # Use pandas iterrows for looping
        ]

        # Build table columns with sort buttons
        columns = [
            ft.DataColumn(
                ft.Row(
                    [
                        ft.Text("ID"),
                        ft.IconButton(
                            icon=ft.icons.ARROW_UPWARD if sort_column == "id" and sort_order == "asc" else ft.icons.ARROW_DOWNWARD,
                            on_click=lambda _: sort_data("id"),
                            icon_color="white",
                            tooltip="Sort by ID",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            ),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Photo")),
            ft.DataColumn(
                ft.Row(
                    [
                        ft.Text("NIK"),
                        ft.IconButton(
                            icon=ft.icons.ARROW_UPWARD if sort_column == "nik" and sort_order == "asc" else ft.icons.ARROW_DOWNWARD,
                            on_click=lambda _: sort_data("nik"),
                            icon_color="white",
                            tooltip="Sort by NIK",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            ),
            ft.DataColumn(
                ft.Row(
                    [
                        ft.Text("Usia"),
                        ft.IconButton(
                            icon=ft.icons.ARROW_UPWARD if sort_column == "usia" and sort_order == "asc" else ft.icons.ARROW_DOWNWARD,
                            on_click=lambda _: sort_data("usia"),
                            icon_color="white",
                            tooltip="Sort by Usia",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            ),
            ft.DataColumn(ft.Text("Gender")),
            ft.DataColumn(ft.Text("Forensic Results")),
            ft.DataColumn(
                ft.Row(
                    [
                        ft.Text("Case ID"),
                        ft.IconButton(
                            icon=ft.icons.ARROW_UPWARD if sort_column == "id_kasus" and sort_order == "asc" else ft.icons.ARROW_DOWNWARD,
                            on_click=lambda _: sort_data("id_kasus"),
                            icon_color="white",
                            tooltip="Sort by Case ID",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            ),
            ft.DataColumn(ft.Text("Edit")),
        ]
        return ft.DataTable(columns=columns, rows=table_rows)

    # Function to close the modal
    def close_modal():
        modal_dialog.open = False
        page.update()

    # Function to refresh the table
    def refresh_table():
        nonlocal filtered_data, total_pages
        filtered_data = victims_model.get_victims()
        total_pages = math.ceil(len(filtered_data) / rows_per_page)
        update_content(current_page)

    # Function to open the add victim modal
    def open_add_victim_modal():
        # Fields for adding a new victim
        id_field = ft.TextField(label="ID")
        name_field = ft.TextField(label="Name")
        nik_field = ft.TextField(label="NIK")
        usia_field = ft.TextField(label="Usia")
        gender_field = ft.TextField(label="Gender")
        forensic_field = ft.TextField(label="Forensic Results")
        case_id_field = ft.TextField(label="Case ID")

        # Function to save the new victim
        def save_new_victim(e):
            # Collect values from the fields
            new_victim = {
                "id": int(id_field.value),
                "nama": name_field.value,
                "foto": "",  # Photo is not required
                "nik": nik_field.value,
                "usia": int(usia_field.value),
                "jk": gender_field.value,
                "hasil_forensik": forensic_field.value,
                "id_kasus": int(case_id_field.value),
            }
            # Add the new victim
            victims_model.add_victim(new_victim)
            refresh_table()  # Refresh the table
            close_modal()

        # Add content and actions to the modal
        modal_dialog.content = ft.Column(
            [
                id_field,
                name_field,
                nik_field,
                usia_field,
                gender_field,
                forensic_field,
                case_id_field,
            ],
            tight=True,
        )
        modal_dialog.actions = [
            ft.Row(
                [
                    ft.ElevatedButton("Save", on_click=save_new_victim),
                    ft.TextButton("Cancel", on_click=lambda _: close_modal()),
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        ]
        modal_dialog.open = True
        page.dialog = modal_dialog
        page.update()

    # Function to sort data
    def sort_data(column):
        nonlocal filtered_data, sort_column, sort_order, current_page
        if sort_column == column:
            sort_order = "desc" if sort_order == "asc" else "asc"
        else:
            sort_column = column
            sort_order = "asc"
        filtered_data = filtered_data.sort_values(by=column, ascending=(sort_order == "asc"))
        current_page = 0  # Reset to first page after sorting
        update_content(current_page)

    # Function to update the content when a page is changed
    def update_content(page_index):
        nonlocal current_page, total_pages
        current_page = page_index
        table_container.content = build_table(page_index)
        pagination_controls.controls[1].value = f"Page {page_index + 1} of {total_pages}"
        pagination_controls.controls[0].disabled = current_page == 0
        pagination_controls.controls[2].disabled = current_page == total_pages - 1
        page.update()

    # Function to handle search input
    def handle_search(e):
        nonlocal filtered_data, current_page
        search_term = e.control.value
        filtered_data = victims_model.search_victims(search_term)
        current_page = 0
        update_content(current_page)

    # Pagination controls
    pagination_controls = ft.Row(
        [
            ft.IconButton(
                ft.icons.CHEVRON_LEFT,
                on_click=lambda _: update_content(current_page - 1),
                disabled=current_page == 0,
            ),
            ft.Text(value=f"Page 1 of {total_pages}", size=18),
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
                ft.Text("Victims", size=30, weight=ft.FontWeight.BOLD, color="white"),
                ft.Row(
                    [
                        ft.TextField(
                            label="Search Victims...",
                            width=300,
                            on_change=handle_search,
                        ),
                        ft.ElevatedButton(
                            text="Add Victim",
                            icon=ft.icons.ADD,
                            on_click=lambda _: open_add_victim_modal(),
                            bgcolor="white",
                            color="black",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                table_container,
                pagination_controls,
            ]
        ),
        expand=True,
        padding=20,
    )

    return container
