import flet as ft
from sidebar import create_sidebar
from dashboard_page import dashboard_content
from cases_page import cases_content
from victims_page import victims_content
from suspects_page import suspects_content
from detectives_page import detectives_content

# Daredevil-inspired color palette
COLORS = {
    # Almost black, like Daredevil's nighttime backdrop
    "background_dark": "#111111",
    "primary_red": "#B22222",         # Dark red, reminiscent of Daredevil's costume
    "secondary_red": "#8B0000",       # Deeper red for accents
    "text_light": "#E6E6E6",          # Light gray for text
    "divider": "#333333",             # Dark gray for dividers
}


def main(page: ft.Page):
    page.title = "Detective Tasksboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = COLORS["background_dark"]
    page.padding = 10

    # Custom theme to match Daredevil palette
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=COLORS["primary_red"],
            secondary=COLORS["secondary_red"],
            surface=COLORS["background_dark"],
            background=COLORS["background_dark"],
        )
    )

    # Function to handle navigation
    def on_navigate(page_name):
        page.controls.clear()  # Clear the current content

        # Create sidebar
        sidebar = create_sidebar(on_navigate)

        # Create vertical divider with custom color
        divider = ft.VerticalDivider(
            width=1,
            color=COLORS["divider"]
        )

        # Dynamic content selection
        content = None
        if page_name == "dashboard":
            content = dashboard_content(page)
        elif page_name == "cases":
            content = cases_content(page)
        elif page_name == "victims":
            content = victims_content(page)
        elif page_name == "suspects":
            content = suspects_content(page)
        elif page_name == "detectives":
            content = detectives_content(page)

        # Add content with dark, gritty layout
        page.add(
            ft.Row(
                [
                    sidebar,
                    ft.Container(
                        content=content,
                        bgcolor=COLORS["background_dark"],
                        padding=15,
                        border_radius=15,  # Rounded corners for a modern look
                        border=ft.border.all(
                            1, COLORS["divider"]),  # Subtle border
                        expand=True
                    )
                ],
                expand=True
            )
        )
        page.update()

    # Initialize to Dashboard
    on_navigate("dashboard")


ft.app(target=main)
