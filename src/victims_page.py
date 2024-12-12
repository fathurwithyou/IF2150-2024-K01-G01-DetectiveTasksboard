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

    # Separate modals for adding and editing victims
    add_modal_dialog = ft.AlertDialog(modal=True, title=ft.Text("Add Victim"))
    view_modal_dialog = ft.AlertDialog(modal=True, title=ft.Text("View Victim"))

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
                    ft.DataCell(ft.Text(", ".join(map(lambda x: '-' if x == 0 else str(x), row["id_kasus"])))),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.icons.VISIBILITY,
                            icon_color="white",
                            tooltip="View",
                            on_click=lambda e, victim_id=row["id"]: open_view_victim_modal(victim_id),
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
                            tooltip="Sort by Age",
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
                        ft.Text("Case IDs"),
                        ft.IconButton(
                            icon=ft.icons.ARROW_UPWARD if sort_column == "id_kasus" and sort_order == "asc" else ft.icons.ARROW_DOWNWARD,
                            on_click=lambda _: sort_data("id_kasus"),
                            icon_color="white",
                            tooltip="Sort by Case IDs",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            ),
            ft.DataColumn(ft.Text("Details")),
        ]
        return ft.DataTable(columns=columns, rows=table_rows)

    def refresh_table():
        nonlocal filtered_data, total_pages
        filtered_data = victims_model.get_victims()
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

    def open_add_victim_modal():
        name_field = ft.TextField(label="Name")
        nik_field = ft.TextField(label="NIK")
        usia_field = ft.TextField(label="Usia")
        gender_field = ft.TextField(label="Gender")
        forensic_field = ft.TextField(label="Forensic Results")

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
            }
            victims_model.add_victim(new_victim)
            refresh_table()
            page.close(add_modal_dialog)

        add_modal_dialog.content = ft.Column(
            [
                name_field,
                nik_field,
                usia_field,
                gender_field,
                forensic_field,
            ],
            tight=True,
        )
        add_modal_dialog.actions = [
            ft.Row(
                [
                    ft.ElevatedButton("Save", on_click=save_new_victim),
                    ft.TextButton("Cancel", on_click=lambda _: page.close(add_modal_dialog)),
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        ]
        page.open(add_modal_dialog)

    def open_view_victim_modal(victim_id):
        victim = victims_model.get_victims().loc[victims_model.get_victims()["id"] == victim_id].iloc[0]

        id_text = ft.Text(f"ID: {victim['id']}")
        name_text = ft.Text(f"Name: {victim['nama']}")
        photo_text = ft.Text(f"Photo: {victim['foto']}")
        nik_text = ft.Text(f"NIK: {victim['nik']}")
        age_text = ft.Text(f"Age: {victim['usia']}")
        gender_text = ft.Text(f"Gender: {victim['jk']}")
        forensic_text = ft.Text(f"Forensic Results: {victim['hasil_forensik']}")
        case_id_text = ft.Text(f'Case ID: {", ".join(map(lambda x: "-" if x == 0 else str(x), victim["id_kasus"]))}')

        id_field = ft.TextField(label="ID", value=str(victim["id"]), read_only=True, visible=False, disabled=True, color="grey")
        name_field = ft.TextField(label="Name", value=victim["nama"], read_only=True, visible=False)
        nik_field = ft.TextField(label="NIK", value=str(victim["nik"]), read_only=True, visible=False)
        usia_field = ft.TextField(label="Usia", value=str(victim["usia"]), read_only=True, visible=False)
        gender_field = ft.TextField(label="Gender", value=victim["jk"], read_only=True, visible=False)
        forensic_field = ft.TextField(label="Forensic Results", value=victim["hasil_forensik"], read_only=True, visible=False)
        case_id_field = ft.TextField(label="Case IDs (comma separated)", value=", ".join(map(str, victim["id_kasus"])), read_only=True, visible=False, disabled=True, color="grey")

        def open_edit_victim_modal(e):
            id_text.visible = False
            name_text.visible = False
            photo_text.visible = False
            nik_text.visible = False
            age_text.visible = False
            gender_text.visible = False
            forensic_text.visible = False
            case_id_text.visible = False

            id_field.visible = True
            name_field.visible = True
            nik_field.visible = True
            usia_field.visible = True
            gender_field.visible = True
            forensic_field.visible = True
            case_id_field.visible = True

            name_field.read_only = False
            nik_field.read_only = False
            usia_field.read_only = False
            gender_field.read_only = False
            forensic_field.read_only = False

            view_modal_dialog.title = ft.Text("Edit Victim")
            view_modal_dialog.actions = [
                ft.Row(
                    [
                        ft.ElevatedButton("Save", on_click=save_updated_victim),
                        ft.ElevatedButton("Delete", bgcolor="red", color="white", on_click=delete_victim),
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
            forensic_text.visible = True
            case_id_text.visible = True

            id_field.visible = False
            name_field.visible = False
            nik_field.visible = False
            usia_field.visible = False
            gender_field.visible = False
            forensic_field.visible = False
            case_id_field.visible = False

            name_field.read_only = True
            nik_field.read_only = True
            usia_field.read_only = True
            gender_field.read_only = True
            forensic_field.read_only = True

            view_modal_dialog.title = ft.Text("View Victim")
            view_modal_dialog.actions = [
                ft.Row(
                    [
                        ft.ElevatedButton("Edit", on_click=open_edit_victim_modal),
                        ft.TextButton("Close", on_click=lambda _: page.close(view_modal_dialog)),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                )
            ]
            page.update()

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
            }
            victims_model.update_victim(updated_victim)
            refresh_table()
            page.close(view_modal_dialog)

        def delete_victim(e):
            victims_model.delete_victim(victim["id"])
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
                forensic_text,
                case_id_text,
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
        view_modal_dialog.actions = [
            ft.Row(
                [
                    ft.ElevatedButton("Edit", on_click=open_edit_victim_modal),
                    ft.TextButton("Close", on_click=lambda _: page.close(view_modal_dialog)),
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        ]
        page.open(view_modal_dialog)

    def handle_search(e):
        nonlocal filtered_data, current_page
        search_term = e.control.value.lower()
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
                            bgcolor="white",
                            color="black",
                            on_click=lambda _: open_add_victim_modal(),
                        ),
                    ],
                ),
                table_container,
                pagination_controls,
            ]
        )
    )

    return container