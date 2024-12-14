import flet as ft
import math
from models.suspects import Suspects

def suspects_content(page: ft.Page):
    suspects_model = Suspects()
    filtered_data = suspects_model.get_suspects()
    rows_per_page = 10
    current_page = 0
    total_pages = math.ceil(len(filtered_data) / rows_per_page)
    sort_column = None
    sort_order = "asc"

    # Separate modals for adding and viewing suspects
    add_modal_dialog = ft.AlertDialog(modal=True, title=ft.Text("Add Suspect"))
    view_modal_dialog = ft.AlertDialog(modal=True, title=ft.Text("View Suspect"))

    def build_table_header():
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
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
                                tight=True
                            ),
                            expand=1
                        ),
                        ft.Container(
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
                                tight=True
                            ),
                            expand=2
                        ),
                        ft.Container(
                            ft.Text("Photo"),
                            expand=2
                        ),
                        ft.Container(
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
                                tight=True
                            ),
                            expand=2
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text("Age"),
                                    ft.IconButton(
                                        icon=ft.icons.ARROW_UPWARD if sort_column == "usia" and sort_order == "asc" else ft.icons.ARROW_DOWNWARD,
                                        on_click=lambda _: sort_data("usia"),
                                        icon_color="white",
                                        tooltip="Sort by Age",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                tight=True
                            ),
                            expand=1
                        ),
                        ft.Container(
                            ft.Text("Gender"),
                            expand=1
                        ),
                        ft.Container(
                            ft.Text("Criminal Record"),
                            expand=2
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text("Case IDs"),
                                    ft.IconButton(
                                        icon=ft.icons.ARROW_UPWARD if sort_column == "id_kasus" and sort_order == "asc" else ft.icons.ARROW_DOWNWARD,
                                        on_click=lambda _: sort_data("id_kasus"),
                                        icon_color="white",
                                        tooltip="Sort by Case IDs",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                tight=True
                            ),
                            expand=2
                        ),
                        ft.Container(
                            ft.Text("Details"),
                            expand=1,
                            alignment=ft.alignment.center
                        ),
                    ],
                    spacing=0,  # No additional spacing inside the header row
                ),
                ft.Divider(thickness=1, color="grey"),  # Line under the header
            ],
            spacing=0,  # Minimize space between header elements
        )

    def build_table(page_index):
        start_index = page_index * rows_per_page    
        end_index = start_index + rows_per_page 
        page_data = filtered_data.iloc[start_index:end_index]

        # Table rows with reduced gap
        table_rows = []
        for _, row in page_data.iterrows():
            # Add the data row
            table_rows.append(
                ft.Row(
                    [
                        ft.Container(ft.Text(str(row["id"])), expand=1, alignment=ft.alignment.top_left),
                        ft.Container(ft.Text(str(row["nama"])), expand=2, alignment=ft.alignment.top_left),
                        ft.Container(ft.Text(str(row["foto"])), expand=2, alignment=ft.alignment.top_left),
                        ft.Container(ft.Text(str(row["nik"])), expand=2, alignment=ft.alignment.top_left),
                        ft.Container(ft.Text(str(row["usia"])), expand=1, alignment=ft.alignment.top_left),
                        ft.Container(ft.Text(str(row["jk"])), expand=1, alignment=ft.alignment.top_left),
                        ft.Container(ft.Text(str(row["catatan_kriminal"])), expand=2, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(", ".join(map(lambda x: '-' if x == 0 else str(x), row["id_kasus"]))),
                            expand=2,
                            alignment=ft.alignment.top_left,
                        ),
                        ft.Container(
                            ft.IconButton(
                                icon=ft.icons.VISIBILITY,
                                icon_color="white",
                                tooltip="View",
                                on_click=lambda e, suspect_id=row["id"]: open_view_suspect_modal(suspect_id),
                            ),
                            expand=1,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    spacing=0,  # Minimize space inside the row
                )
            )   
            # Add a separator line after each row   
            table_rows.append(ft.Divider(thickness=1, color="grey"))

        return ft.Column(
            table_rows,
            spacing=2,
            expand=True,
            scroll="auto",  # Explicitly set scroll here
        )

    def refresh_table():
        nonlocal filtered_data, total_pages
        filtered_data = suspects_model.get_suspects()
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
        table_header.content = build_table_header()  # Rebuild the table header to update the sort icons
        page.update()  # Ensure the page updates to reflect the new sort order

    def update_content(page_index):
        nonlocal current_page, total_pages
        current_page = page_index
        table_container.content = build_table(page_index)
        pagination_controls.controls[1].value = f"Page {page_index + 1} of {total_pages}"
        pagination_controls.controls[0].disabled = current_page == 0
        pagination_controls.controls[2].disabled = current_page == total_pages - 1
        page.update()

    def open_add_suspect_modal():
        name_field = ft.TextField(label="Name")
        photo_field = ft.TextField(label="Photo")
        nik_field = ft.TextField(label="NIK")
        age_field = ft.TextField(label="Age")
        gender_field = ft.TextField(label="Gender")
        criminal_record_field = ft.TextField(label="Criminal Record")

        def save_new_suspect(e):
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

            if not age_field.value.strip() or not age_field.value.isdigit():
                age_field.error_text = "Valid age is required"
                errors.append("age")
            else:
                age_field.error_text = None

            if not gender_field.value.strip():
                gender_field.error_text = "Gender is required"
                errors.append("gender")
            else:
                gender_field.error_text = None

            if not criminal_record_field.value.strip():
                criminal_record_field.error_text = "Criminal Record is required"
                errors.append("criminal_record")
            else:
                criminal_record_field.error_text = None

            page.update()

            if errors:
                return
            
            new_suspect = {
                "id": suspects_model.get_last_suspect_id() + 1,
                "nama": name_field.value,
                "foto": photo_field.value,
                "nik": nik_field.value,
                "usia": int(age_field.value),
                "jk": gender_field.value,
                "catatan_kriminal": criminal_record_field.value,
            }
            suspects_model.add_suspect(new_suspect)
            refresh_table()
            page.close(add_modal_dialog)

        add_modal_dialog.content = ft.Column(
            [
                name_field,
                photo_field,
                nik_field,
                age_field,
                gender_field,
                criminal_record_field,
            ],
            tight=True,
        )
        add_modal_dialog.actions = [
            ft.Row(
                [
                    ft.ElevatedButton("Save", on_click=save_new_suspect),
                    ft.TextButton("Cancel", on_click=lambda _: page.close(add_modal_dialog)),
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        ]
        page.open(add_modal_dialog)

    def open_view_suspect_modal(suspect_id):
        suspect = suspects_model.get_suspects().loc[suspects_model.get_suspects()["id"] == suspect_id].iloc[0]

        id_text = ft.Text(f"ID: {suspect['id']}")
        name_text = ft.Text(f"Name: {suspect['nama']}")
        photo_text = ft.Text(f"Photo: {suspect['foto']}")
        nik_text = ft.Text(f"NIK: {suspect['nik']}")
        age_text = ft.Text(f"Age: {suspect['usia']}")
        gender_text = ft.Text(f"Gender: {suspect['jk']}")
        criminal_record_text = ft.Text(f"Criminal Record: {suspect['catatan_kriminal']}")
        case_id_text = ft.Text(f'Case ID: {", ".join(map(lambda x: "-" if x == 0 else str(x), suspect["id_kasus"]))}')

        id_field = ft.TextField(label="ID", value=str(suspect["id"]), read_only=True, visible=False, disabled=True, color="grey")
        name_field = ft.TextField(label="Name", value=suspect["nama"], read_only=True, visible=False)
        photo_field = ft.TextField(label="Photo", value=suspect["foto"], read_only=True, visible=False)
        nik_field = ft.TextField(label="NIK", value=str(suspect["nik"]), read_only=True, visible=False)
        age_field = ft.TextField(label="Age", value=str(suspect["usia"]), read_only=True, visible=False)
        gender_field = ft.TextField(label="Gender", value=suspect["jk"], read_only=True, visible=False)
        criminal_record_field = ft.TextField(label="Criminal Record", value=suspect["catatan_kriminal"], read_only=True, visible=False)
        case_id_field = ft.TextField(
            label="Case ID",
            value=", ".join(map(lambda x: '-' if x == 0 else str(x), suspect["id_kasus"])),
            read_only=True,
            visible=False,
            disabled=True,
            color="grey"
        )

        def open_edit_suspect_modal(e):
            id_text.visible = False
            name_text.visible = False
            photo_text.visible = False
            nik_text.visible = False
            age_text.visible = False
            gender_text.visible = False
            criminal_record_text.visible = False
            case_id_text.visible = False

            id_field.visible = True
            name_field.visible = True
            photo_field.visible = True
            nik_field.visible = True
            age_field.visible = True
            gender_field.visible = True
            criminal_record_field.visible = True
            case_id_field.visible = True

            name_field.read_only = False
            photo_field.read_only = False
            nik_field.read_only = False
            age_field.read_only = False
            gender_field.read_only = False
            criminal_record_field.read_only = False

            view_modal_dialog.title = ft.Text("Edit Suspect")
            view_modal_dialog.actions = [
                ft.Row(
                    [
                        ft.ElevatedButton("Save", on_click=save_updated_suspect),
                        ft.ElevatedButton("Delete", bgcolor="red", color="white", on_click=delete_suspect),
                        ft.TextButton("Cancel", on_click=cancel_edit),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                )
            ]
            page.update()

        def cancel_edit(e):
            id_text.visible = True
            name_text.visible = True
            photo_text.visible = True
            nik_text.visible = True
            age_text.visible = True
            gender_text.visible = True
            criminal_record_text.visible = True
            case_id_text.visible = True

            id_field.visible = False
            name_field.visible = False
            photo_field.visible = False
            nik_field.visible = False
            age_field.visible = False
            gender_field.visible = False
            criminal_record_field.visible = False
            case_id_field.visible = False

            name_field.read_only = True
            photo_field.read_only = True
            nik_field.read_only = True
            age_field.read_only = True
            gender_field.read_only = True
            criminal_record_field.read_only = True

            view_modal_dialog.title = ft.Text("View Suspect")
            view_modal_dialog.actions = [
                ft.Row(
                    [
                        ft.ElevatedButton("Edit", on_click=open_edit_suspect_modal),
                        ft.TextButton("Close", on_click=lambda _: page.close(view_modal_dialog)),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                )
            ]
            page.update()

        def save_updated_suspect(e):
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

            if not age_field.value.strip() or not age_field.value.isdigit():
                age_field.error_text = "Valid age is required"
                errors.append("age")
            else:
                age_field.error_text = None

            if not gender_field.value.strip():
                gender_field.error_text = "Gender is required"
                errors.append("gender")
            else:
                gender_field.error_text = None

            if not criminal_record_field.value.strip():
                criminal_record_field.error_text = "Criminal Record is required"
                errors.append("criminal_record")
            else:
                criminal_record_field.error_text = None

            page.update()

            if errors:
                return
            
            updated_suspect = {
                "id": int(id_field.value),
                "nama": name_field.value,
                "foto": photo_field.value,
                "nik": nik_field.value,
                "usia": int(age_field.value),
                "jk": gender_field.value,
                "catatan_kriminal": criminal_record_field.value,
            }
            suspects_model.update_suspect(updated_suspect)
            refresh_table()
            page.close(view_modal_dialog)

        def delete_suspect(e):
            suspects_model.delete_suspect(suspect["id"])
            refresh_table()
            page.close(view_modal_dialog)

        view_modal_dialog.content = ft.Column(
            [
                id_text,
                name_text,
                photo_text,
                nik_text,
                age_text,
                gender_text,
                criminal_record_text,
                case_id_text,
                id_field,
                name_field,
                photo_field,
                nik_field,
                age_field,
                gender_field,
                criminal_record_field,
                case_id_field,
            ],
            tight=True,
        )
        view_modal_dialog.actions = [
            ft.Row(
                [
                    ft.ElevatedButton("Edit", on_click=open_edit_suspect_modal),
                    ft.TextButton("Close", on_click=lambda _: page.close(view_modal_dialog)),
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        ]
        page.open(view_modal_dialog)

    def handle_search(e):
        nonlocal filtered_data, current_page
        search_term = e.control.value.lower()
        filtered_data = suspects_model.search_suspects(search_term)
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

    table_header = build_table_header()

    table_container = ft.Container(
        content=ft.Column(
            [
                build_table(current_page)
            ],
            expand=True,
            scroll="auto"  # Ensure scroll is applied to the entire container
        ),
        expand=True,
        height=450,  # Adjust the height as needed
    )

    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Suspects", size=30, weight=ft.FontWeight.BOLD, color="white"),
                ft.Row(
                    [
                        ft.TextField(
                            label="Search Suspects...",
                            width=300,
                            on_change=handle_search,
                        ),
                        ft.ElevatedButton(
                            text="Add Suspect",
                            icon=ft.icons.ADD,
                            bgcolor="white",
                            color="black",
                            style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(
                                        radius=10),
                            ),
                            on_click=lambda _: open_add_suspect_modal(),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                table_header,
                table_container,
                ft.Container(
                    content=pagination_controls,
                    alignment=ft.alignment.center,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True
        ),
        expand=True,
        padding=10,
    )

    return container