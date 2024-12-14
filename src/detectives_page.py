import flet as ft
import math
from models.detectives import Detective
COLORS = {
    "background_dark": "#111111",
    "primary_red": "#B22222",
    "secondary_red": "#8B0000",
    "text_light": "#E6E6E6",
    "divider": "#333333",
    "text_muted": "#999999",
    "status_gray": "#444444"
}


def detectives_content(page: ft.Page):
    detective_model = Detective()
    filtered_data = detective_model.get_detectives()
    rows_per_page = 10
    current_page = 0
    total_pages = math.ceil(len(filtered_data) / rows_per_page)
    sort_column = None
    sort_order = "asc"

    # Separate modals for adding and editing detectives
    add_modal_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Add Detective", color=COLORS["text_light"], weight=ft.FontWeight.BOLD),
        bgcolor=COLORS["background_dark"],
        shape=ft.RoundedRectangleBorder(radius=5),
    )

    view_modal_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("View Detective", color=COLORS["text_light"]),
        bgcolor=COLORS["background_dark"],
        shape=ft.RoundedRectangleBorder(radius=5),
    )

    def build_table_header():
        nonlocal sort_column, sort_order
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
                                tight=True
                            ),
                            expand=1
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Text("Name"),
                                    ft.IconButton(
                                        icon=ft.icons.ARROW_UPWARD if (sort_column == "nama" and sort_order == "asc") else ft.icons.ARROW_DOWNWARD,
                                        on_click=lambda _: sort_data("nama"),
                                        icon_color="white",
                                        icon_size=16,
                                        tooltip="Sort by Name",
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
                                tight=True
                            ),
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
                                        icon_size=16,
                                        tooltip="Sort by Case IDs",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                tight=True
                            ),
                            expand=3
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
                            ft.Text(str(row["id"])), expand=1, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(str(row["nama"])), expand=2, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(str(row["nik"])), expand=2, alignment=ft.alignment.top_left),
                        ft.Container(
                            ft.Text(", ".join(map(lambda x: '-' if x ==
                                    0 else str(x), row["id_kasus"]))),
                            expand=3,
                            alignment=ft.alignment.top_left,
                        ),
                        ft.Container(
                            ft.IconButton(
                                icon=ft.icons.VISIBILITY,
                                icon_color="white",
                                tooltip="View",
                                icon_size=16,
                                on_click=lambda e, detective_id=row["id"]: open_view_detective_modal(
                                    detective_id),
                            ),
                            expand=1,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    spacing=0,  # Minimize space inside the row
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
        
        filtered_data = filtered_data.sort_values(
            by=column, ascending=(sort_order == "asc"))
        current_page = 0
        update_content(current_page)
        # Rebuild the table header to update the sort icons
        table_header.content = build_table_header()
        table_header.update()  # Ensure the header updates to reflect the new sort order
        page.update()  # Ensure the page updates to reflect the new sort order

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

            page.update()

            if errors:
                return

            new_detective = {
                "id": detective_model.get_last_detective_id() + 1,
                "nama": name_field.value,
                "nik": nik_field.value,
            }
            detective_model.add_detective(new_detective)
            refresh_table()
            page.close(add_modal_dialog)

        add_modal_dialog.content = ft.Column(
            [
                name_field,
                nik_field,
            ],
            tight=True,
        )
        add_modal_dialog.actions = [
            ft.Row(
                [
                    ft.TextButton(
                        "Cancel",
                        on_click=lambda _: page.close(add_modal_dialog),
                        style=ft.ButtonStyle(
                            color=COLORS["primary_red"],
                            shape=ft.RoundedRectangleBorder(radius=5),
                        )),
                    ft.ElevatedButton(
                        "Save",
                        on_click=save_new_detective,
                        style=ft.ButtonStyle(
                            bgcolor=COLORS["primary_red"],
                            color=COLORS["text_light"],
                            shape=ft.RoundedRectangleBorder(radius=5),
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        ]
        page.open(add_modal_dialog)

    def open_view_detective_modal(detective_id):
        detective = detective_model.get_detectives().loc[detective_model.get_detectives()[
            "id"] == detective_id].iloc[0]

        id_text = ft.Text(f"ID: {detective['id']}")
        name_text = ft.Text(f"Name: {detective['nama']}")
        nik_text = ft.Text(f"NIK: {detective['nik']}")
        case_id_text = ft.Text(
            f'Case ID: {", ".join(map(lambda x: "-" if x == 0 else str(x), detective["id_kasus"]))}')

        id_field = ft.TextField(label="ID", value=str(
            detective["id"]), read_only=True, visible=False, disabled=True, color="grey")
        name_field = ft.TextField(
            label="Name", value=detective["nama"], read_only=True, visible=False)
        nik_field = ft.TextField(label="NIK", value=str(
            detective["nik"]), read_only=True, visible=False)
        case_id_field = ft.TextField(
            label="Case ID",
            value=", ".join(
                map(lambda x: '-' if x == 0 else str(x), detective["id_kasus"])),
            read_only=True,
            visible=False,
            disabled=True,
            color="grey"
        )

        def open_edit_detective_modal(e):
            id_text.visible = False
            name_text.visible = False
            nik_text.visible = False
            case_id_text.visible = False

            id_field.visible = True
            name_field.visible = True
            nik_field.visible = True
            case_id_field.visible = True

            name_field.read_only = False
            nik_field.read_only = False

            view_modal_dialog.title = ft.Text("Edit Detective")
            view_modal_dialog.actions = [
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Save", on_click=save_updated_detective),
                        ft.ElevatedButton(
                            "Delete", bgcolor="red", color="white", on_click=delete_detective),
                        ft.TextButton("Cancel", on_click=cancel_edit),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                )
            ]
            page.update()

        def cancel_edit(e):
            id_text.visible = True
            name_text.visible = True
            nik_text.visible = True
            case_id_text.visible = True

            id_field.visible = False
            name_field.visible = False
            nik_field.visible = False
            case_id_field.visible = False

            name_field.read_only = True
            nik_field.read_only = True

            view_modal_dialog.title = ft.Text("View Detective")
            view_modal_dialog.actions = [
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Edit", on_click=open_edit_detective_modal),
                        ft.TextButton(
                            "Close", on_click=lambda _: page.close(view_modal_dialog)),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                )
            ]
            page.update()

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

            page.update()

            if errors:
                return

            updated_detective = {
                "id": int(id_field.value),
                "nama": name_field.value,
                "nik": nik_field.value,
            }
            detective_model.update_detective(updated_detective)
            refresh_table()
            page.close(view_modal_dialog)

        def delete_detective(e):
            detective_model.delete_detective(detective["id"])
            refresh_table()
            page.close(view_modal_dialog)

        view_modal_dialog.content = ft.Column(
            [
                id_text,
                name_text,
                nik_text,
                case_id_text,
                id_field,
                name_field,
                nik_field,
                case_id_field,
            ],
            tight=True,
        )
        view_modal_dialog.actions = [
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Edit", on_click=open_edit_detective_modal),
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
                        "Detectives",
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
                                            text="Add Detective",
                                            icon=ft.icons.ADD,
                                            bgcolor=COLORS["primary_red"],
                                            color=COLORS["text_light"],
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10),
                                                overlay_color={
                                                    ft.MaterialState.HOVERED: COLORS["secondary_red"]
                                                }
                                            ),
                                            on_click=lambda _: open_add_detective_modal(),
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
