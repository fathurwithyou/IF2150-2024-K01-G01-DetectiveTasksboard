import flet as ft

# Daredevil-inspired color palette
COLORS = {
    "background_dark": "#111111",     # Almost black, like Daredevil's nighttime backdrop
    "primary_red": "#B22222",         # Dark red, reminiscent of Daredevil's costume
    "secondary_red": "#8B0000",       # Deeper red for accents
    "text_light": "#E6E6E6",          # Light gray for text
    "divider": "#333333",             # Dark gray for dividers
}

def create_sidebar(on_navigate):
    def create_list_tile(icon, title, page_name):
        tile_container = ft.Container(
            content=ft.ListTile(
                leading=ft.Icon(icon, color=COLORS["text_light"]),
                title=ft.Text(title, color=COLORS["text_light"]),
                bgcolor=COLORS["background_dark"],
                on_click=lambda _: on_click_handler(page_name)
            ),
            bgcolor=COLORS["background_dark"],
            border_radius=10,
            padding=ft.Padding(5, 5, 5, 5),
            border=ft.border.all(1, COLORS["divider"])
        )

        def hover_handler(e):
            tile_container.bgcolor = COLORS["secondary_red"] if e.data == "true" else COLORS["background_dark"]
            tile_container.update()

        def on_click_handler(page_name):
            tile_container.border = ft.border.all(1, COLORS["primary_red"])
            tile_container.update()
            on_navigate(page_name)

        tile_container.on_hover = hover_handler
        return tile_container

    return ft.Container(
        content=ft.Column(
            [
                ft.Image(
                    src="../image.png",
                    width=200,
                    height=50,
                    fit=ft.ImageFit.CONTAIN
                ),
                ft.Divider(color=COLORS["divider"]),
                create_list_tile(
                    ft.icons.DASHBOARD, 
                    "Dashboard", 
                    "dashboard"
                ),
                create_list_tile(
                    ft.icons.CASES, 
                    "Cases", 
                    "cases"
                ),
                create_list_tile(
                    ft.icons.PERSON_SEARCH, 
                    "Suspects", 
                    "suspects"
                ),
                create_list_tile(
                    ft.icons.GROUP, 
                    "Victims", 
                    "victims"
                ),
                create_list_tile(
                    ft.icons.BADGE, 
                    "Detectives", 
                    "detectives"
                ),
            ],
            spacing=5,
        ),
        width=250,  # Slightly wider for better readability
        bgcolor=COLORS["background_dark"],
        padding=15,
        border_radius=15,  # Rounded corners for a modern look
        border=ft.border.all(1, COLORS["divider"])  # Subtle border
    )