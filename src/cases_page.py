import flet as ft
from models.cases import Cases
from models.victims import Victims
from models.suspects import Suspects
from models.detectives import Detective
from datetime import datetime


def cases_content(page: ft.Page):
    case_model = Cases()
    victim_model = Victims()
    suspect_model = Suspects()
    detective_model = Detective()

    all_cases = case_model.get_cases()
    filtered_cases = all_cases.copy()
    search_query = ""

    def create_case_tile(id_kasus):
        """Create a case tile with expandable details."""
        case, suspects, victims, detectives = case_model.get_cases_info(
            id_kasus)
        suspects = case_model.get_name_list(suspects)
        victims = case_model.get_name_list(victims)
        detectives = case_model.get_name_list(detectives)

        case["id"] = id_kasus
        is_expanded = False  # Initial state for dropdown

        def toggle_expand(e):
            """Toggle the expanded state of the tile."""
            nonlocal is_expanded
            is_expanded = not is_expanded
            update_tile()  # Refresh the tile content

        def update_tile():
            """Update the content of the tile based on the expanded state."""
            details_container.visible = is_expanded  # Show or hide details
            edit_button.visible = is_expanded  # Show or hide edit button
            toggle_button.icon = ft.icons.KEYBOARD_ARROW_UP if is_expanded else ft.icons.KEYBOARD_ARROW_DOWN
            case_tile.update()

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

        edit_button = ft.IconButton(
            icon=ft.icons.EDIT,
            icon_color="white",
            tooltip="Edit Case",
            on_click=lambda _: edit_case_modal(case),
            visible=False,
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
                                            f"Case #{case['id']}: {case['judul']}",
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
                            edit_button,  # Use the edit_button here
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
            [create_case_tile(idx) for idx, case in filtered_cases.iterrows()],
            scroll="auto",  
        )
        page.update()

    def handle_search(e):
        """Handle the search input."""
        nonlocal search_query
        search_query = e.control.value
        refresh_list()

    def edit_case_modal(case):
        """Open a modal to edit the selected case."""
        nonlocal all_cases
        
        suspect_id_df = case_model.get_all_suspects_id()
        victim_id_df = case_model.get_all_victims_id()
        detective_id_df = case_model.get_all_detectives_id()

        # include by id_kasus is same as case id in this case
        all_suspects = set(suspect_id_df['id_suspect'].tolist())
        set_suspect = set(
            suspect_id_df[suspect_id_df['id_kasus'] == case['id']]['id_suspect'].tolist())

        all_victims = set(victim_id_df['id_victim'].tolist())
        set_victim = set(
            victim_id_df[victim_id_df['id_kasus'] == case['id']]['id_victim'].tolist())
        
        all_detectives = set(detective_id_df['id_detective'].tolist())
        set_detective = set(
            detective_id_df[detective_id_df['id_kasus'] == case['id']]['id_detective'].tolist())

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
            page.close(edit_case_modal)

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
        
        progress_field = ft.TextField(
            label="Progress",
            multiline=True,
            max_lines=5,
            hint_text="Optional progress",
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

        name_field.value = case["judul"]
        status_field.value = case["status"]
        status_field.label = case["status"]
        date_field.value = case["tanggal_mulai"]
        desc_field.value = case["catatan"]

        date_picker = ft.DatePicker(
            first_date=datetime(2021, 1, 1),
            last_date=datetime(datetime.now().year,
                               datetime.now().month, datetime.now().day),
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

        # add all_victims - set_victim
        victim_field = ft.Dropdown(
            label="Add Victim",
            hint_text="Select victim",
            options=[
                ft.dropdown.Option(victim_model.get_victim_by_id(
                    id_victim).get('nama', 'Tidak ada nama'), on_click=lambda e, id_victim=id_victim:
                        (set_victim.add(id_victim),
                         update_victim_list(),
                         page.update()))
                for id_victim in all_victims - set_victim
            ],
        )

        suspect_field = ft.Dropdown(
            label="Add Suspect",
            hint_text="Select suspect",
            options=[
                ft.dropdown.Option(suspect_model.get_suspect_by_id(
                    id_suspect).get('nama', 'Tidak ada nama'), on_click=lambda e, id_suspect=id_suspect:
                        (set_suspect.add(id_suspect),
                         update_suspect_list(),
                         page.update()))
                for id_suspect in all_suspects - set_suspect
            ],
        )

        detective_field = ft.Dropdown(
            label="Add Detective",
            hint_text="Select detective",
            options=[
                ft.dropdown.Option(detective_model.get_detective_by_id(
                    id_detective).get('nama', 'Tidak ada nama'), on_click=lambda e, id_detective=id_detective:
                        (set_detective.add(id_detective),
                         update_detective_list(),
                         page.update()))
                for id_detective in all_detectives - set_detective
            ],
        )
        
        def update_detective_list():
            detective_field.options = [
                ft.dropdown.Option(detective_model.get_detective_by_id(
                    id_detective).get('nama', 'Tidak ada nama'), on_click=lambda e, id_detective=id_detective:
                        (set_detective.add(id_detective),
                         update_detective_list(),
                         page.update()))
                for id_detective in all_detectives - set_detective
            ]

            detective_list.controls = [
                ft.TextButton(
                    detective_model.get_detective_by_id(
                        id_detective).get('nama', 'Tidak ada nama'),
                    icon=ft.icons.REMOVE,
                    expand=True,
                    icon_color="white",
                    style=ft.ButtonStyle(
                        color="white"
                    ),
                    on_click=lambda e, id_detective=id_detective: detective_remove(
                        id_detective),
                )
                for id_detective in set_detective
            ]
            
        def detective_remove(id_detective):
            """Remove a detective from the list."""
            set_detective.remove(id_detective)
            update_detective_list()
            page.update()

        def update_victim_list() -> None:
            victim_field.options = [
                ft.dropdown.Option(victim_model.get_victim_by_id(
                    id_victim).get('nama', 'Tidak ada nama'), on_click=lambda e, id_victim=id_victim:
                        (set_victim.add(id_victim),
                         update_victim_list(),
                         page.update()))
                for id_victim in all_victims - set_victim
            ]

            victim_list.controls = [
                ft.TextButton(
                    victim_model.get_victim_by_id(
                        id_victim).get('nama', 'Tidak ada nama'),
                    icon=ft.icons.REMOVE,
                    expand=True,
                    icon_color="white",
                    style=ft.ButtonStyle(
                        color="white"  # Set text color to white
                    ),
                    on_click=lambda e, id_victim=id_victim: victim_remove(
                        id_victim),
                )
                for id_victim in set_victim
            ]

        def victim_remove(id_victim):
            """Remove a victim from the list."""
            set_victim.remove(id_victim)  # Remove the victim from the set
            update_victim_list()  # Update the displayed list
            page.update()                 # Refresh the page to reflect changes

        def update_suspect_list():
            suspect_field.options = [
                ft.dropdown.Option(suspect_model.get_suspect_by_id(
                    id_suspect).get('nama', 'Tidak ada nama'), on_click=lambda e, id_suspect=id_suspect:
                        (set_suspect.add(id_suspect),
                         update_suspect_list(),
                         page.update()))
                for id_suspect in all_suspects - set_suspect
            ]

            suspect_list.controls = [
                ft.TextButton(
                    suspect_model.get_suspect_by_id(
                        id_suspect).get('nama', 'Tidak ada nama'),
                    icon=ft.icons.REMOVE,
                    expand=True,
                    icon_color="white",
                    style=ft.ButtonStyle(
                        color="white"
                    ),
                    on_click=lambda e, id_suspect=id_suspect: suspect_remove(
                        id_suspect),
                )
                for id_suspect in set_suspect
            ]

        def suspect_remove(id_suspect):
            """Remove a suspect from the list."""
            set_suspect.remove(id_suspect)
            update_suspect_list()
            page.update()

        victim_list = ft.Column(
            controls=[
                ft.TextButton(
                    victim_model.get_victim_by_id(
                        id_victim).get('nama', 'Tidak ada nama'),
                    icon=ft.icons.REMOVE,
                    expand=True,
                    icon_color="white",
                    style=ft.ButtonStyle(
                        color="white"
                    ),
                    on_click=lambda e, id_victim=id_victim: victim_remove(
                        id_victim),
                )
                for id_victim in set_victim
            ],
            spacing=5,
        )

        suspect_list = ft.Column(
            controls=[
                ft.TextButton(
                    suspect_model.get_suspect_by_id(
                        id_suspect).get('nama', 'Tidak ada nama'),
                    icon=ft.icons.REMOVE,
                    expand=True,
                    icon_color="white",
                    style=ft.ButtonStyle(
                        color="white"
                    ),
                    on_click=lambda e, id_suspect=id_suspect: suspect_remove(
                        id_suspect),
                )
                for id_suspect in set_suspect
            ],
            spacing=5,
        )
        
        detective_list = ft.Column(
            controls=[
                ft.TextButton(
                    detective_model.get_detective_by_id(
                        id_detective).get('nama', 'Tidak ada nama'),
                    icon=ft.icons.REMOVE,
                    expand=True,
                    icon_color="white",
                    style=ft.ButtonStyle(
                        color="white"
                    ),
                    on_click=lambda e, id_detective=id_detective: detective_remove(
                        id_detective),
                )
                for id_detective in set_detective
            ],
            spacing=5,
        )

        def update_case_modal(e):
            """Update the case details after editing."""
            nonlocal all_cases
            if not validate_inputs():
                page.update()
                return

            updated_case = {
                "judul": name_field.value.strip(),
                "status": status_field.value,
                "tanggal_mulai": date_field.value,
                "tanggal_selesai": None,
                "perkembangan_kasus": progress_field.value.strip() if progress_field.value else "Tidak ada perkembangan",
                "catatan": desc_field.value.strip() if desc_field.value else "Tidak ada catatan",
            }

            case_model.update_case(case['id'], updated_case, set_suspect, set_victim, set_detective)
            all_cases = case_model.get_cases()
            refresh_list()
            page.close(edit_case_modal)
        
        edit_case_modal = ft.AlertDialog(
            title=ft.Text(
                f"Edit Case #{case['id']}", size=20, weight=ft.FontWeight.BOLD),
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
                        progress_field,
                        desc_field,
                        victim_field,
                        victim_list,
                        suspect_field,
                        suspect_list,
                        detective_field,
                        detective_list,
                    ],
                    spacing=10,
                    scroll="auto",
                ),
                width=500,
                height=300,
            ),
            actions=[
                ft.Row(
                    controls=[
                        ft.TextButton(
                            "Cancel",
                            on_click=lambda _: page.close(edit_case_modal),
                            style=ft.ButtonStyle(
                                color=ft.colors.ERROR,
                                shape=ft.RoundedRectangleBorder(radius=5),
                            )
                        ),
                        ft.ElevatedButton(
                            "Save",
                            on_click=update_case_modal,
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

        page.open(edit_case_modal)

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
