import flet as ft
from models.cases import Cases
from datetime import datetime


def cases_content(page: ft.Page):
    case_model = Cases()
    all_cases = case_model.get_cases()
    filtered_cases = all_cases.copy()
    search_query = ""

    def create_case_tile(id_kasus):
        """Create a case tile with expandable details."""
        is_expanded = False  # Initial state for dropdown

        def toggle_expand(e):
            """Toggle the expanded state of the tile."""
            nonlocal is_expanded
            is_expanded = not is_expanded
            update_tile()  # Refresh the tile content

        def update_tile():
            """Update the content of the tile based on the expanded state."""
            details_container.visible = is_expanded  # Show or hide details
            toggle_button.icon = ft.icons.KEYBOARD_ARROW_UP if is_expanded else ft.icons.KEYBOARD_ARROW_DOWN
            case_tile.update()

        print("id_kasus:", id_kasus)
        case, suspects, victims, detectives = case_model.get_cases_info(
            id_kasus)
        details_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        f"Description: {case.get('catatan', 'Tidak ada catatan')}", size=14),
                    ft.Text(
                        f"Progress: {case.get('perkembangan_kasus', 'Tidak ada perkembangan')}", size=14),
                    ft.Text(
                        f"Assigned Detective: {', '.join(detectives)}", size=14),
                    ft.Text(f"Victims: {', '.join(victims)}", size=14),
                    ft.Text(f"Suspects: {', '.join(suspects)}", size=14),
                ],
                spacing=5,
            ),
            padding=ft.Padding(10, 10, 10, 10),
            visible=False,  # Hidden by default
        )

        toggle_button = ft.IconButton(
            icon=ft.icons.KEYBOARD_ARROW_DOWN,
            icon_color="white",
            tooltip="Expand/Collapse",
            on_click=toggle_expand,
        )

        case_tile = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            f"Case #{id_kasus}: {case['judul']}",
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            f"{case['status']}, {case['tanggal_mulai']}",
                                            size=16,
                                            color="gray",
                                        ),
                                    ]
                                ),
                                expand=True,
                            ),
                            toggle_button,  # Use the toggle_button here
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    details_container,  # The hidden container for detailed information
                ],
            ),
            padding=ft.Padding(10, 10, 10, 10),
            border=ft.Border(
                top=ft.BorderSide(width=2, color=ft.colors.SURFACE_VARIANT),
                left=ft.BorderSide(width=2, color=ft.colors.SURFACE_VARIANT),
                right=ft.BorderSide(width=2, color=ft.colors.SURFACE_VARIANT),
                bottom=ft.BorderSide(width=2, color=ft.colors.SURFACE_VARIANT),
            ),
            border_radius=ft.border_radius.all(5),
        )

        return case_tile

    def refresh_list():
        """Refresh the displayed list of cases based on the current search query."""
        nonlocal filtered_cases
        if search_query.strip():
            filtered_cases = all_cases[
                all_cases.apply(
                    lambda row: search_query.lower() in str(row.values).lower(),
                    axis=1,
                )
            ]
        else:
            filtered_cases = all_cases

        list_container.content = ft.Column(
            [create_case_tile(idx) for idx, case in filtered_cases.iterrows()]
        )
        page.update()

    def handle_search(e):
        """Handle the search input."""
        nonlocal search_query
        search_query = e.control.value
        refresh_list()

    def edit_case_modal(case):
        """Open a modal to edit the selected case."""
        edit_modal = ft.AlertDialog(
            title=ft.Text(f"Edit Case #{case['id']}"),
            content=ft.Column(
                [
                    ft.TextField(label="Status", value=case["status"]),
                    ft.TextField(label="Start Date (YYYY-MM-DD)",
                                 value=case["tanggal_mulai"]),
                ]
            ),
            actions=[
                ft.Row(
                    [
                        ft.ElevatedButton(
                            text="Save",
                            on_click=lambda _: save_case_changes(None),
                        ),
                        ft.TextButton(
                            text="Cancel",
                            on_click=lambda _: page.close(edit_modal),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
        )
        status_field = ft.TextField(label="Status", value=case["status"])
        date_field = ft.TextField(
            label="Start Date (YYYY-MM-DD)", value=case["tanggal_mulai"])

        def save_case_changes(e):
            nonlocal all_cases
            if not status_field.value.strip() or not date_field.value.strip():
                status_field.error_text = "Required" if not status_field.value.strip() else None
                date_field.error_text = "Required" if not date_field.value.strip() else None
                page.update()
                return

            case_model.update_case(
                case["id"], status_field.value, date_field.value)
            all_cases = case_model.get_cases()

    def open_case_actions_modal(case):
        """Open a modal with options for the selected case."""
        modal_dialog = ft.AlertDialog(
            # add style
            title=ft.Text(f"Actions for Case #{case['id']}"),
            content=ft.Text(
                f"Status: {case['status']}\nStart Date: {case['tanggal_mulai']}"),
            actions=[
                ft.ElevatedButton(
                    text="Edit",
                    icon=ft.icons.EDIT,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(
                            radius=10),  # Adjust radius as needed
                    ),
                    on_click=lambda _: edit_case_modal(case),
                ),
                ft.ElevatedButton(
                    text="Delete",
                    icon=ft.icons.DELETE,
                    bgcolor="red",
                    color="white",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(
                            radius=10),  # Adjust radius as needed
                    ),
                    on_click=lambda _: page.close(modal_dialog),
                ),
                ft.TextButton(
                    text="Close",
                    on_click=lambda _: page.close(modal_dialog),
                ),
            ],
        )
        page.open(modal_dialog)

    # Search bar and add case button
    header_controls = ft.Row(
        [
            ft.TextField(
                label="Search Cases...",
                width=300,
                on_change=handle_search,
            ),
            ft.ElevatedButton(
                text="Add Case",
                icon=ft.icons.ADD,
                bgcolor="white",
                color="black",
                style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(
                            radius=10),  # Adjust radius as needed
                ),
                on_click=lambda _: open_add_case_modal(),
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # List container for displaying cases
    list_container = ft.Container(
        content=ft.Column([create_case_tile(idx)
                          for idx, case in filtered_cases.iterrows()],
                          scroll="auto"), height=200, expand=True
    )

    # Main container layout
    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Cases", size=30, weight=ft.FontWeight.BOLD),
                header_controls,
                list_container,
            ]
        ),
        expand=True,
    )

    def open_add_case_modal():
        """Open a modal to add a new case with improved validation and UI."""
        nonlocal all_cases

        def validate_inputs():
            """Validate all input fields before saving."""
            is_valid = True

            # Validate name field
            if not name_field.value or not name_field.value.strip():
                name_field.error_text = "Case name is required"
                is_valid = False
            else:
                name_field.error_text = None

            # Validate status field
            if not status_field.value:
                status_field.error_text = "Status is required"
                is_valid = False
            else:
                status_field.error_text = None

            # Validate date field
            if not date_field.value:
                date_field.error_text = "Start date is required"
                is_valid = False
            else:
                date_field.error_text = None

            return is_valid

        def on_date_pick(e):
            """Handle date selection."""
            selected_date = e.control.value
            date_field.value = selected_date.strftime("%Y-%m-%d")
            date_field.error_text = None
            page.update()

        def save_new_case(e):
            """Save the new case after validation."""
            nonlocal all_cases
            if not validate_inputs():
                page.update()
                return

            new_case = {
                "judul": name_field.value.strip(),
                "status": status_field.value,
                "tanggal_mulai": date_field.value,
                "tanggal_selesai": None,
                "perkembangan_kasus": "Tidak ada perkembangan",
                "catatan": desc_field.value.strip() if desc_field.value else "Tidak ada catatan",
            }

            case_model.add_case(new_case)
            all_cases = case_model.get_cases()  # Reload cases
            refresh_list()
            page.close(add_case_modal)

        # Input fields with improved styling and validation
        name_field = ft.TextField(
            label="Case Name",
            hint_text="Enter case name",
        )

        desc_field = ft.TextField(
            label="Description",
            multiline=True,
            max_lines=5,
            hint_text="Optional description",
        )

        status_field = ft.Dropdown(
            label="Status",
            hint_text="Select case status",
            options=[
                ft.dropdown.Option("Selesai"),
                ft.dropdown.Option("Belum Selesai"),
                ft.dropdown.Option("On-going"),
            ],
        )

        # Date input with picker
        date_field = ft.TextField(
            label="Start Date",
            read_only=True,
            hint_text="Select start date",
            expand=True,
        )

        # Date picker configuration
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        date_picker = ft.DatePicker(
            first_date=datetime(2021, 1, 1),
            last_date=datetime(year, month, day),
            date_picker_mode=ft.DatePickerMode.DAY,
            on_change=on_date_pick,
        )
        
     
        date_button = ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,
            icon_color=ft.colors.WHITE,
            on_click=lambda _: page.open(date_picker),
        )
        
        date_field.suffix = ft.Container(
            content=date_button,
            on_click=lambda _: page.open(date_picker),
        )

        # Modal dialog
        add_case_modal = ft.AlertDialog(
            title=ft.Text("Add New Case", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        name_field,
                        status_field,
                        ft.Row(
                            controls=[date_field],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            spacing=10,
                        ),
                        desc_field,
                    ],
                    spacing=10,
                ),
                width=500,
                height=300,
            ),
            actions=[
                ft.Row(
                    controls=[
                        ft.TextButton(
                            "Cancel",
                            on_click=lambda _: page.close(add_case_modal),
                            style=ft.ButtonStyle(
                                color=ft.colors.ERROR,
                                shape=ft.RoundedRectangleBorder(radius=5),
                            )
                        ),
                        ft.ElevatedButton(
                            "Save",
                            on_click=save_new_case,
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.PRIMARY,
                                color=ft.colors.ON_PRIMARY,
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

        page.open(add_case_modal)

    return container
