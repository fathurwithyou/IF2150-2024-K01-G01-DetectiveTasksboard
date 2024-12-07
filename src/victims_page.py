import flet as ft
import math
from models.victims import Victims


def victims_content(page: ft.Page):
    victims_model = Victims()
    filtered_data = victims_model.get_victims() 
    rows_per_page = 10
    current_page = 0 
    total_pages = math.ceil(len(filtered_data) / rows_per_page)
    sort_column = None 
    sort_order = "asc"  

    # Modal for adding or editing victims
    modal_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(""),
        content=None,
        actions=None,
    )


    def build_table(page_index):
        start_index = page_index * rows_per_page
        end_index = start_index + rows_per_page
        page_data = filtered_data.iloc[start_index:end_index]  

        table_rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(row["id"]))),              
                    ft.DataCell(ft.Text(str(row["nama"]))),             
                    ft.DataCell(ft.Text(str(row["foto"]))),             
                    ft.DataCell(ft.Text(str(row["nik"]))),              
                    ft.DataCell(ft.Text(str(row["usia"]))),            
                    ft.DataCell(ft.Text(str(row["jk"]))),               
                    ft.DataCell(ft.Text(str(row["hasil_forensik"]))),   
                    ft.DataCell(ft.Text(str(row["id_kasus"]))),         
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            icon_color="white",
                            tooltip="Edit",
                            on_click=lambda e, r=row: open_edit_victim_modal(row),
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

    def close_modal():
        modal_dialog.open = False
        modal_dialog.actions = None  
        modal_dialog.content = None  
        page.update()


    def refresh_table():
        nonlocal filtered_data, total_pages
        filtered_data = victims_model.get_victims()
        total_pages = math.ceil(len(filtered_data) / rows_per_page)
        update_content(current_page)

    def open_add_victim_modal():
        name_field = ft.TextField(label="Name")
        nik_field = ft.TextField(label="NIK")
        usia_field = ft.TextField(label="Usia")
        gender_field = ft.TextField(label="Gender")
        forensic_field = ft.TextField(label="Forensic Results")
        case_id_field = ft.TextField(label="Case ID")

        def save_new_victim(e):
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

            if not usia_field.value.strip() or not usia_field.value.isdigit():
                usia_field.error_text = "Valid age is required"
                errors.append("usia")
            else:
                usia_field.error_text = None

            if not gender_field.value.strip():
                gender_field.error_text = "Gender is required"
                errors.append("gender")
            else:
                gender_field.error_text = None

            if not forensic_field.value.strip():
                forensic_field.error_text = "Forensic Results are required"
                errors.append("forensic")
            else:
                forensic_field.error_text = None

            if not case_id_field.value.strip() or not case_id_field.value.isdigit():
                case_id_field.error_text = "Valid Case ID is required"
                errors.append("case_id")
            else:
                case_id_field.error_text = None

            page.update()

            if errors:
                return
            
            new_victim = {
                "id": victims_model.get_last_victim_id() + 1,
                "nama": name_field.value,
                "foto": "", 
                "nik": nik_field.value,
                "usia": int(usia_field.value),
                "jk": gender_field.value,
                "hasil_forensik": forensic_field.value,
                "id_kasus": int(case_id_field.value),
            }
            # Add the new victim
            victims_model.add_victim(new_victim)
            refresh_table()  
            close_modal()

        modal_dialog.title = ft.Text("Add Victim")
        modal_dialog.content = ft.Column(
            [
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

    def open_edit_victim_modal(victim):
        id_field = ft.TextField(label="ID", value=str(victim["id"]), read_only=True)
        name_field = ft.TextField(label="Name", value=victim["nama"])
        nik_field = ft.TextField(label="NIK", value=victim["nik"])
        usia_field = ft.TextField(label="Usia", value=str(victim["usia"]))
        gender_field = ft.TextField(label="Gender", value=victim["jk"])
        forensic_field = ft.TextField(label="Forensic Results", value=victim["hasil_forensik"])
        case_id_field = ft.TextField(label="Case ID", value=str(victim["id_kasus"]))

        def save_updated_victim(e):
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

            if not usia_field.value.strip() or not usia_field.value.isdigit():
                usia_field.error_text = "Valid age is required"
                errors.append("usia")
            else:
                usia_field.error_text = None

            if not gender_field.value.strip():
                gender_field.error_text = "Gender is required"
                errors.append("gender")
            else:
                gender_field.error_text = None

            if not forensic_field.value.strip():
                forensic_field.error_text = "Forensic Results are required"
                errors.append("forensic")
            else:
                forensic_field.error_text = None

            if not case_id_field.value.strip() or not case_id_field.value.isdigit():
                case_id_field.error_text = "Valid Case ID is required"
                errors.append("case_id")
            else:
                case_id_field.error_text = None

            page.update()

            if errors:
                return
            
            updated_victim = {
                "id": int(id_field.value),
                "nama": name_field.value,
                "foto": victim["foto"],  
                "nik": nik_field.value,
                "usia": int(usia_field.value),
                "jk": gender_field.value,
                "hasil_forensik": forensic_field.value,
                "id_kasus": int(case_id_field.value),
            }
            victims_model.update_victim(updated_victim)
            refresh_table()
            close_modal()

        def delete_victim(e):
            victims_model.delete_victim(victim["id"])
            refresh_table()
            close_modal()

        modal_dialog.title = ft.Text(f"Edit Victim - {victim['nama']}")
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
                    ft.ElevatedButton("Save", on_click=save_updated_victim),
                    ft.ElevatedButton("Delete", bgcolor="red", color="white", on_click=delete_victim),
                    ft.TextButton("Cancel", on_click=lambda _: close_modal()),
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        ]
        modal_dialog.open = True
        page.dialog = modal_dialog
        page.update()

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

    def handle_search(e):
        nonlocal filtered_data, current_page
        search_term = e.control.value
        filtered_data = victims_model.search_victims(search_term)
        current_page = 0
        update_content(current_page)

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

    table_container = ft.Container(content=build_table(current_page))

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
