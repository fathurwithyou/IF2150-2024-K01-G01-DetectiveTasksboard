import flet as ft
import math
from models.suspects import Suspects
import os
from PIL import Image

def suspects_content(page: ft.Page):
    suspects_model = Suspects()
    filtered_data = suspects_model.get_suspects()
    rows_per_page = 10
    current_page = 0
    total_pages = math.ceil(len(filtered_data) / rows_per_page)
    sort_column = None
    sort_order = "asc"

    # Separate modals for adding and editing suspects
    add_modal_dialog = ft.AlertDialog(modal=True, title=ft.Text("Add Suspect"))
    edit_modal_dialog = ft.AlertDialog(modal=True, title=ft.Text("Edit Suspect"))
    view_modal_dialog = ft.AlertDialog(
        modal=True, title=ft.Text("Suspect Detail", size=20, weight=ft.FontWeight.BOLD))

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
                                        on_click=lambda _: sort_data(
                                            "id_kasus"),
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
                            ft.Text("Actions"),
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
                        ft.Container(
                            ft.Text(str(row["id"])), expand=1, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(str(row["nama"])), expand=2, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(str(row["foto"])), expand=2, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(str(row["nik"])), expand=2, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(str(row["usia"])), expand=1, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(str(row["jk"])), expand=1, alignment=ft.alignment.top_left),
                        ft.Container(ft.Text(
                            str(row["catatan_kriminal"])), expand=2, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(", ".join(map(lambda x: '-' if x ==
                                    0 else str(x), row["id_kasus"]))),
                            expand=2,
                            alignment=ft.alignment.top_left,
                        ),
                        ft.Container(
                            ft.Row([
                                ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color="white",
                                tooltip="View",
                                on_click=lambda e, suspect_id=row["id"]: open_edit_suspect_modal(
                                    suspect_id),
                            ),
                                ft.IconButton(
                                icon=ft.icons.VISIBILITY,
                                icon_color="white",
                                tooltip="View",
                                on_click=lambda e, suspect_id=row["id"]: open_view_suspect_modal(
                                    suspect_id),
                            ),
                            ]),
                            
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

    def open_edit_suspect_modal(suspect_id):
        suspect = suspects_model.get_suspects().loc[suspects_model.get_suspects()["id"] == suspect_id].iloc[0]
    
        id_field = ft.TextField(label="ID", value=str(suspect["id"]), read_only=True, visible=False, disabled=True, color="grey")
        name_field = ft.TextField(label="Name", value=suspect["nama"])
        result_text = ft.Text()
        result_text.visible = False
    
        def handle_file_picker_result(e: ft.FilePickerResultEvent):
            if e.files:
                photo_path = convert_to_jpg(e.files[0])  # Convert uploaded file to JPG
                if photo_path:
                    result_text.value = f"Image saved at: {photo_path}"
                else:
                    result_text.value = "Failed to convert image."
            else:
                result_text.value = "No file selected."
            result_text.visible = True
            page.update()
    
        file_picker = ft.FilePicker(on_result=handle_file_picker_result)
        photo_field = ft.ElevatedButton("Upload Photo", on_click=lambda _: file_picker.pick_files())
        page.overlay.append(file_picker)
    
        def convert_to_jpg(file):
            if file:
                # ensure filename always unique using hash
                img = Image.open(file.path)
                photo_field.value = f"{hash(file.path)}.jpg"
                jpg_path = f"data/suspects/{photo_field.value}"
    
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
    
                img.save(jpg_path, "JPEG")
    
                page.update()
                return jpg_path
    
        nik_field = ft.TextField(label="NIK", value=suspect["nik"])
        age_field = ft.TextField(label="Age", value=suspect["usia"])
        gender_field = ft.Dropdown(
            label="Gender",
            options=[
                ft.dropdown.Option("Laki-laki"),
                ft.dropdown.Option("Perempuan"),
            ],
            value=suspect["jk"]
        )
        criminal_record_field = ft.TextField(label="Criminal Record", value=suspect["catatan_kriminal"])
    
        def save_updated_suspect(e):
            errors = []
            if not name_field.value.strip():
                name_field.error_text = "Name is required"
                errors.append("name")
            else:
                name_field.error_text = None
    
            if not nik_field:
                nik_field.error_text = "NIK is required"
                errors.append("nik")
            else:
                nik_field.error_text = None
    
            if not age_field.value:
                age_field.error_text = "Valid age is required"
                errors.append("age")
            else:
                age_field.error_text = None
    
            if not gender_field.value:
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
            page.close(edit_modal_dialog)
    
        def delete_suspect(e):
            suspects_model.delete_suspect(suspect["id"])
            refresh_table()
            page.close(edit_modal_dialog)
    
        edit_modal_dialog = ft.AlertDialog(
            title=ft.Text(f"Edit Suspect #{suspect['id']}", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        id_field,
                        name_field,
                        photo_field,
                        result_text,
                        nik_field,
                        age_field,
                        gender_field,
                        criminal_record_field,
                    ],
                    tight=True,
                    scroll="auto"
                ),
                width=500,
                height=300,
            ),
            actions=[
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Delete",
                            on_click=delete_suspect,
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.ERROR,
                                color=ft.colors.ON_ERROR,
                                shape=ft.RoundedRectangleBorder(radius=5),
                            )
                        ),
                        ft.ElevatedButton(
                            "Save",
                            on_click=save_updated_suspect,
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.PRIMARY,
                                color=ft.colors.ON_PRIMARY,
                                shape=ft.RoundedRectangleBorder(radius=5),
                            )
                        ),
                        ft.TextButton(
                            "Cancel",
                            on_click=lambda _: page.close(edit_modal_dialog),
                            style=ft.ButtonStyle(
                                color=ft.colors.ERROR,
                                shape=ft.RoundedRectangleBorder(radius=5),
                            )
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    spacing=10,
                )
            ],
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=5),
        )
    
        page.open(edit_modal_dialog)

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
        result_text = ft.Text()
        result_text.visible = False
        def handle_file_picker_result(e: ft.FilePickerResultEvent):
            if e.files:
                photo_path = convert_to_jpg(e.files[0])  # Convert uploaded file to JPG
                if photo_path:
                    result_text.value = f"Image saved at: {photo_path}"
                else:
                    result_text.value = "Failed to convert image."
            else:
                result_text.value = "No file selected."
            result_text.visible = True
            page.update()
            
        file_picker = ft.FilePicker(on_result=handle_file_picker_result)
        photo_field = ft.ElevatedButton("Upload Photo", on_click=lambda _: file_picker.pick_files())
        page.overlay.append(file_picker)
        
        def convert_to_jpg(file):
            if file:
                # ensure filename always unique using hash
                img = Image.open(file.path)
                photo_field.value = f"{hash(file.path)}.jpg"
                jpg_path = f"data/suspects/{photo_field.value}"
                
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                img.save(jpg_path, "JPEG")
                
                page.update()
                return jpg_path
            
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
                result_text,
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
                    ft.TextButton(
                        "Cancel", on_click=lambda _: page.close(add_modal_dialog)),
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        ]
        page.open(add_modal_dialog)

    def open_view_suspect_modal(suspect_id):
        print(f"Viewing suspect with ID: {suspect_id}")
        suspect = suspects_model.get_suspects().loc[suspects_model.get_suspects()["id"] == suspect_id].iloc[0]
    
        id_text = ft.Text(f"ID: {suspect['id']}")
        name_text = ft.Text(f"Name: {suspect['nama']}")
        photo_text = ft.Text(f"Photo: {suspect['foto']}")
        nik_text = ft.Text(f"NIK: {suspect['nik']}")
        age_text = ft.Text(f"Age: {suspect['usia']}")
        gender_text = ft.Text(f"Gender: {suspect['jk']}")
        criminal_record_text = ft.Text(f"Criminal Record: {suspect['catatan_kriminal']}")
        case_id_text = ft.Text(f'Case ID: {", ".join(map(lambda x: "-" if x == 0 else str(x), suspect["id_kasus"]))}')
    
        photo_path = os.path.join("data", "suspects", suspect["foto"])
        tmp_path = f"data/suspects/resized_photo_{suspect_id}.jpg"
    
        def resize_image(image_path, width, height, output_path=None):
            with Image.open(image_path) as img:
                img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
                if output_path:
                    img_resized.save(output_path)
    
        resize_image(photo_path, 170, 220, tmp_path)
        photo_field = ft.Image(src=f'{tmp_path}', fit=ft.ImageFit.CONTAIN)
    
        view_modal_dialog.content = ft.Container(
            content=ft.Row(
                [
                    photo_field if os.path.exists(photo_path) else ft.Text("No photo available"),
                    ft.Column(
                        [
                            id_text,
                            name_text,
                            photo_text,
                            nik_text,
                            age_text,
                            gender_text,
                            criminal_record_text,
                            case_id_text,
                        ],
                        tight=True,
                    ),
                ]
            ),
            border_radius=ft.border_radius.all(5),
        )
    
        view_modal_dialog.actions = [
            ft.Row(
                [
                    ft.TextButton(
                        "Close", on_click=lambda _: page.close(view_modal_dialog)),
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
            ft.Text(
                value=f"Page {current_page + 1} of {total_pages}", size=18),
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

    table_container = ft.Container(content=build_table(current_page))

    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Suspects", size=30,
                        weight=ft.FontWeight.BOLD, color="white"),
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