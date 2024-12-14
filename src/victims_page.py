import flet as ft
import math
from models.victims import Victims
from PIL import Image
import os
import time

COLORS = {
    "background_dark": "#111111",
    "primary_red": "#B22222",
    "secondary_red": "#8B0000",
    "text_light": "#E6E6E6",
    "divider": "#333333",
    "text_muted": "#999999",
    "status_gray": "#444444"
}

def victims_content(page: ft.Page):
    victims_model = Victims()
    filtered_data = victims_model.get_victims()
    rows_per_page = 10
    current_page = 0
    total_pages = math.ceil(len(filtered_data) / rows_per_page)
    sort_column = None
    sort_order = "asc"

    # Separate modals for adding and editing victims
    add_modal_dialog = ft.AlertDialog(modal=True, title=ft.Text("Add victim"))
    edit_modal_dialog = ft.AlertDialog(modal=True, title=ft.Text("Edit victim"))
    view_modal_dialog = ft.AlertDialog(
        modal=True, title=ft.Text("victim Detail", size=20, weight=ft.FontWeight.BOLD))

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
                                        icon_size=16,
                                        tooltip="Sort by ID",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                tight=True,
                                spacing=5 
                            ),
                            expand=True
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text("Name"),
                                    ft.IconButton(
                                        icon=ft.icons.ARROW_UPWARD if sort_column == "nama" and sort_order == "asc" else ft.icons.ARROW_DOWNWARD,
                                        on_click=lambda _: sort_data("nama"),
                                        icon_color="white",
                                        icon_size=16,
                                        tooltip="Sort by Name",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                tight=True,
                                spacing=5 
                            ),
                            expand=2
                        ),
                        ft.Container(
                            ft.Text("Photo"),
                            expand=1,
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text("NIK"),
                                    ft.IconButton(
                                        icon=ft.icons.ARROW_UPWARD if sort_column == "nik" and sort_order == "asc" else ft.icons.ARROW_DOWNWARD,
                                        on_click=lambda _: sort_data("nik"),
                                        icon_color="white",
                                        icon_size=16,
                                        tooltip="Sort by NIK",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                tight=True,
                                spacing=5 
                            ),
                            expand=True
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text("Age"),
                                    ft.IconButton(
                                        icon=ft.icons.ARROW_UPWARD if sort_column == "usia" and sort_order == "asc" else ft.icons.ARROW_DOWNWARD,
                                        on_click=lambda _: sort_data("usia"),
                                        icon_color="white",
                                        icon_size=16,
                                        tooltip="Sort by Age",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                tight=True,
                                spacing=5 
                            ),
                            expand=1
                        ),
                        ft.Container(
                            ft.Text("Gender"),
                            expand=1,
                        ),
                        ft.Container(
                            ft.Text("Forensic Results"),
                            expand=True,
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
                                        icon_size=16,
                                        tooltip="Sort by Case IDs",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                tight=True,
                                spacing=5,
                            ),
                            expand=True
                        ),
                        ft.Container(
                            ft.Text("Details"),
                            expand=1,
                            alignment=ft.alignment.center
                        ),
                    ],
                    spacing=10,  # No additional spacing inside the header row
                ),
                ft.Divider(thickness=1, color="text_muted"),  # Line under the header
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
                            ft.Text(str(row["id"]), overflow=ft.TextOverflow.ELLIPSIS), expand=True, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(str(row["nama"]), overflow=ft.TextOverflow.ELLIPSIS), expand=2, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(str(row["foto"]), overflow=ft.TextOverflow.ELLIPSIS), expand=1, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(str(row["nik"]), overflow=ft.TextOverflow.ELLIPSIS), expand=True, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(str(row["usia"]), overflow=ft.TextOverflow.ELLIPSIS), expand=1, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(str(row["jk"]), overflow=ft.TextOverflow.ELLIPSIS), expand=1, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(str(row["hasil_forensik"]), overflow=ft.TextOverflow.ELLIPSIS), expand=True, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(", ".join(map(lambda x: '-' if x ==
                                    0 else str(x), row["id_kasus"]))),
                            expand=True,
                            alignment=ft.alignment.top_left,
                        ),
                        ft.Container(
                            ft.IconButton(
                                icon=ft.icons.VISIBILITY,
                                icon_color="white",
                                tooltip="View",
                                icon_size=16,
                                on_click=lambda e, victim_id=row["id"]: open_view_victim_modal(
                                    victim_id),
                            ),
                            expand=1,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    spacing=10,  # Minimize space inside the row
                )
            )
            # Add a separator line after each row
            table_rows.append(ft.Divider(thickness=1, color="text_muted"))

        return ft.Column(
            table_rows,
            spacing=2,
            expand=True,
            scroll="auto",  # Explicitly set scroll here
        )

    def open_edit_victim_modal(victim_id):
        victim = victims_model.get_victims().loc[victims_model.get_victims()["id"] == victim_id].iloc[0]
    
        id_field = ft.TextField(label="ID", value=str(victim["id"]), read_only=True, visible=False, disabled=True, color="grey")
        name_field = ft.TextField(label="Name", value=victim["nama"])
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
                jpg_path = f"data/victims/{photo_field.value}"
    
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
    
                img.save(jpg_path, "JPEG")
    
                page.update()
                return jpg_path
    
        nik_field = ft.TextField(label="NIK", value=victim["nik"])
        age_field = ft.TextField(label="Age", value=victim["usia"])
        gender_field = ft.Dropdown(
            label="Gender",
            options=[
                ft.dropdown.Option("Laki-laki"),
                ft.dropdown.Option("Perempuan"),
            ],
            value=victim["jk"]
        )
        forensic_result_field = ft.TextField(label="Forensic Results", value=victim["hasil_forensik"])
    
        def save_updated_victim(e):
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
    
            if not forensic_result_field.value.strip():
                forensic_result_field.error_text = "Forensic Result is required"
                errors.append("forensic_result")
            else:
                forensic_result_field.error_text = None
    
            page.update()
    
            if errors:
                return
    
            updated_victim = {
                "id": int(id_field.value),
                "nama": name_field.value,
                "foto": photo_field.value,
                "nik": nik_field.value,
                "usia": int(age_field.value),
                "jk": gender_field.value,
                "hasil_forensik": forensic_result_field.value,
            }
            victims_model.update_victim(updated_victim)
            refresh_table()
            page.close(edit_modal_dialog)
    
        def delete_victim(e):
            victims_model.delete_victim(victim["id"])
            refresh_table()
            page.close(edit_modal_dialog)
    
        edit_modal_dialog = ft.AlertDialog(
            title=ft.Text(f"Edit victim #{victim['id']}", size=20, weight=ft.FontWeight.BOLD),
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
                        forensic_result_field,
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
                            on_click=delete_victim,
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.ERROR,
                                color=ft.colors.ON_ERROR,
                                shape=ft.RoundedRectangleBorder(radius=5),
                            )
                        ),
                        ft.ElevatedButton(
                            "Save",
                            on_click=save_updated_victim,
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
        filtered_data = filtered_data.sort_values(
            by=column, ascending=(sort_order == "asc"))
        current_page = 0
        update_content(current_page)
        # Rebuild the table header to update the sort icons
        table_header.content = build_table_header()
        table_header.update()  # Ensure the header updates to reflect the new sort order
        page.update()   # Ensure the page updates to reflect the new sort order

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
                jpg_path = f"data/victims/{photo_field.value}"
                
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                img.save(jpg_path, "JPEG")
                
                page.update()
                return jpg_path
            
        nik_field = ft.TextField(label="NIK")
        usia_field = ft.TextField(label="Age")
        gender_field = ft.Dropdown(
            label="Gender",
            options=[
                ft.dropdown.Option("Laki-laki"),
                ft.dropdown.Option("Perempuan"),
            ]
        )
        forensic_field = ft.TextField(label="Forensic Result")

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
                "foto": photo_field.value,
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
                photo_field,
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
                    ft.TextButton(
                        "Cancel", on_click=lambda _: page.close(add_modal_dialog)),
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        ]
        page.open(add_modal_dialog)

    def open_view_victim_modal(victim_id):
        print(f"Viewing victim with ID: {victim_id}")
        victim = victims_model.get_victims().loc[victims_model.get_victims()["id"] == victim_id].iloc[0]
    
        id_text = ft.Text(f"ID: {victim['id']}")
        name_text = ft.Text(f"Name: {victim['nama']}")
        photo_text = ft.Text(f"Photo: {victim['foto']}")
        nik_text = ft.Text(f"NIK: {victim['nik']}")
        age_text = ft.Text(f"Age: {victim['usia']}")
        gender_text = ft.Text(f"Gender: {victim['jk']}")
        forensic_result_text = ft.Text(f"Forensic Result: {victim['Hasil_forensik']}")
        case_id_text = ft.Text(f'Case ID: {", ".join(map(lambda x: "-" if x == 0 else str(x), victim["id_kasus"]))}')
    
        photo_path = os.path.join("data", "victims", victim["foto"])
        # Generate a unique file name by appending a timestamp
        unique_filename = f"resized_photo_{victim_id}_{int(time.time())}.jpg"
        tmp_path = os.path.join("data", "victims", unique_filename)
        
        def resize_image(image_path, width, height, output_path=None):
            try:
                with Image.open(image_path) as img:
                    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
                    if output_path:
                        img_resized.save(output_path)
            except FileNotFoundError:
                print(f"Error: File {image_path} not found.")
                return None
            except IOError as e:
                print(f"Error: Cannot open or read file {image_path}. {e}")
                return None
        
        resize_image(photo_path, 170, 220, tmp_path)
        
        photo_field = ft.Image(src=tmp_path, fit=ft.ImageFit.CONTAIN) if os.path.exists(tmp_path) else ft.Text("No photo available")
    
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
                            forensic_result_text,
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

    table_header = ft.Container(
        content=build_table_header(),
        bgcolor=COLORS["background_dark"],
    )

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

    def update_border_color(e):
        if e.data == "true":
            search_field.border_color = COLORS["secondary_red"]
            search_field.label_style = ft.TextStyle(
                color=COLORS["primary_red"])
        else:
            search_field.border_color = COLORS["background_dark"]

        search_field.update()

    search_field = ft.TextField(
        label="Search Detectives...",
        width=300,
        border_color=COLORS["background_dark"],
        focused_border_color=COLORS["secondary_red"],
        color=COLORS["text_light"],
        cursor_color=COLORS["text_light"],
        on_change=handle_search,
        on_focus=update_border_color,
        on_blur=update_border_color
    )

    container = ft.Container(
        content=ft.Column(
            [
                ft.ShaderMask(
                    content=ft.Text(
                        "Victims",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,  # Text color should be white for gradient
                    ),
                    shader=ft.LinearGradient(
                        colors=[COLORS["primary_red"],
                                COLORS["secondary_red"], COLORS["primary_red"]],
                        begin=ft.Alignment(-1, -1),
                        end=ft.Alignment(1, 1),
                    ),
                    blend_mode=ft.BlendMode.SRC_IN,  # Blend mode to apply gradient
                ),
                ft.Column(
                    [
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        search_field,
                                        ft.ElevatedButton(
                                            text="Add Victim",
                                            icon=ft.icons.ADD,
                                            bgcolor=COLORS["primary_red"],
                                            color=COLORS["text_light"],
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10),
                                                overlay_color={
                                                    ft.MaterialState.HOVERED: COLORS["secondary_red"]
                                                }
                                            ),
                                            on_click=lambda _: open_add_victim_modal(),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                table_header,
                            ],
                            spacing=20
                        ),
                        table_container,
                        ft.Container(
                            content=pagination_controls,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True
                ),
            ],
            expand=True
        ),
        bgcolor=COLORS["background_dark"],
        padding=10
    )

    return container
