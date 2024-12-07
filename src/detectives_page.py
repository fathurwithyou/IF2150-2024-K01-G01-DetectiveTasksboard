import flet as ft
import math
from models.detectives import Detective

def detectives_content(page: ft.Page):
    detective_model = Detective()
    filtered_data = detective_model.get_detectives()
    rows_per_page = 10
    current_page = 0
    total_pages = math.ceil(len(filtered_data) / rows_per_page)
    sort_column = None
    sort_order = "asc"

    # Separate modals for adding and editing detectives
    add_modal_dialog = ft.AlertDialog(modal=True, title=ft.Text("Add Detective"))
    edit_modal_dialog = ft.AlertDialog(modal=True, title=ft.Text("Edit Detective"))

    def build_table(page_index):
        start_index = page_index * rows_per_page
        end_index = start_index + rows_per_page
        page_data = filtered_data.iloc[start_index:end_index]

        table_rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(row["id"]))),
                    ft.DataCell(ft.Text(str(row["nama"]))),
                    ft.DataCell(ft.Text(str(row["nik"]))),
                    ft.DataCell(ft.Text(str(row["id_kasus"]))),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            icon_color="white",
                            tooltip="Edit",
                            on_click=lambda e, detective_id=row["id"]: open_edit_detective_modal(detective_id),
                        )
                    ),
                ]
            )
            for _, row in page_data.iterrows()
        ]

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
            ft.DataColumn(
                ft.Row(
                    [
                        ft.Text("Name"),
                        ft.IconButton(
                            icon=ft.icons.ARROW_UPWARD if sort_column == "nama" and sort_order == "asc" else ft.icons.ARROW_DOWNWARD,
                            on_click=lambda _: sort_data("nama"),
                            icon_color="white",
                            tooltip="Sort by Name",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            ),
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
            ft.DataColumn(ft.Text("Actions")),
        ]
        return ft.DataTable(columns=columns, rows=table_rows)

    def refresh_table():
        nonlocal filtered_data, total_pages
        filtered_data = detective_model.get_detectives()
        total_pages = math.ceil(len(filtered_data) / rows_per_page)
        update_content(current_page)
        
    def sort_data(column):
        nonlocal filtered_data, sort_column, sort_order, current_page
        if sort_column == column:
            sort_order = "desc" if sort_order == "asc" else "asc"
        else:
            sort_column = column
            sort_order = "asc"
        filtered_data = filtered_data.sort_values(by=column, ascending=(sort_order == "asc"))
        current_page = 0
        update_content(current_page)

    def update_content(page_index):
        nonlocal current_page, total_pages
        current_page = page_index
        table_container.content = build_table(page_index)
        pagination_controls.controls[1].value = f"Page {page_index + 1} of {total_pages}"
        pagination_controls.controls[0].disabled = current_page == 0
        pagination_controls.controls[2].disabled = current_page == total_pages - 1
        page.update()

    def open_add_detective_modal():
        name_field = ft.TextField(label="Name")
        nik_field = ft.TextField(label="NIK")
        case_id_field = ft.TextField(label="Case ID")

        def save_new_detective(e):
            errors = []
            if not name_field.value.strip():
                name_field.error_text = "Name is required"
                errors.append("name")
            else:
                name_field.error_text = None

            if not nik_field.value.strip():
                nik_field.error_text = "NIK is required"
                errors.append("nik")
            else:
                nik_field.error_text = None

            if not case_id_field.value.strip() or not case_id_field.value.isdigit():
                case_id_field.error_text = "Valid Case ID is required"
                errors.append("case_id")
            else:
                case_id_field.error_text = None

            page.update()

            if errors:
                return
            
            new_detective = {
                "id": detective_model.get_last_detective_id() + 1,
                "nama": name_field.value,
                "nik": nik_field.value,
                "id_kasus": int(case_id_field.value),
            }
            detective_model.add_detective(new_detective)
            refresh_table()
            page.close(add_modal_dialog)

        add_modal_dialog.content = ft.Column(
            [
                name_field,
                nik_field,
                case_id_field,
            ],
            tight=True,
        )
        add_modal_dialog.actions = [
            ft.Row(
                [
                    ft.ElevatedButton("Save", on_click=save_new_detective),
                    ft.TextButton("Cancel", on_click=lambda _: page.close(add_modal_dialog)),
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        ]
        page.open(add_modal_dialog)

    def open_edit_detective_modal(detective_id):
        detective = detective_model.get_detectives().loc[detective_model.get_detectives()["id"] == detective_id].iloc[0]

        id_field = ft.TextField(label="ID", value=str(detective["id"]), read_only=True)
        name_field = ft.TextField(label="Name", value=detective["nama"])
        nik_field = ft.TextField(label="NIK", value=str(detective["nik"]))
        case_id_field = ft.TextField(label="Case ID", value=str(detective["id_kasus"]))

        def save_updated_detective(e):
            errors = []
            if not name_field.value.strip():
                name_field.error_text = "Name is required"
                errors.append("name")
            else:
                name_field.error_text = None

            if not nik_field.value.strip():
                nik_field.error_text = "NIK is required"
                errors.append("nik")
            else:
                nik_field.error_text = None

            if not case_id_field.value.strip() or not case_id_field.value.isdigit():
                case_id_field.error_text = "Valid Case ID is required"
                errors.append("case_id")
            else:
                case_id_field.error_text = None

            page.update()

            if errors:
                return
            
            updated_detective = {
                "id": int(id_field.value),
                "nama": name_field.value,
                "nik": nik_field.value,
                "id_kasus": int(case_id_field.value),
            }
            detective_model.update_detective(updated_detective)
            refresh_table()
            page.close(edit_modal_dialog)

        def delete_detective(e):
            detective_model.delete_detective(detective["id"])
            refresh_table()
            page.close(edit_modal_dialog)

        edit_modal_dialog.content = ft.Column(
            [
                id_field,
                name_field,
                nik_field,
                case_id_field,
            ],
            tight=True,
        )
        edit_modal_dialog.actions = [
            ft.Row(
                [
                    ft.ElevatedButton("Save", on_click=save_updated_detective),
                    ft.ElevatedButton("Delete", bgcolor="red", color="white", on_click=delete_detective),
                    ft.TextButton("Cancel", on_click=lambda _: page.close(edit_modal_dialog)),
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        ]
        page.open(edit_modal_dialog)

    def handle_search(e):
        nonlocal filtered_data, current_page
        search_term = e.control.value.lower()
        filtered_data = detective_model.search_detectives(search_term)
        current_page = 0
        update_content(current_page)

    pagination_controls = ft.Row(
        [
            ft.IconButton(
                ft.icons.CHEVRON_LEFT,
                on_click=lambda _: update_content(current_page - 1),
                disabled=current_page == 0,
            ),
            ft.Text(value=f"Page {current_page + 1} of {total_pages}", size=18),
            ft.IconButton(
                ft.icons.CHEVRON_RIGHT,
                on_click=lambda _: update_content(current_page + 1),
                disabled=current_page == total_pages - 1,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    table_container = ft.Container(content=build_table(current_page))

    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Detectives", size=30, weight=ft.FontWeight.BOLD, color="white"),
                ft.Row(
                    [
                        ft.TextField(
                            label="Search Detectives...",
                            width=300,
                            on_change=handle_search,
                        ),
                        ft.ElevatedButton(
                            text="Add Detective",
                            icon=ft.icons.ADD,
                            bgcolor="white",
                            color="black",
                            on_click=lambda _: open_add_detective_modal(),
                        ),
                    ],
                ),
                table_container,
                pagination_controls,
            ]
        )
    )

    return container