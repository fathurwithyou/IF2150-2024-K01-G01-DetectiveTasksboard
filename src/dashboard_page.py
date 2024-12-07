import flet as ft
from models.dashboard import get_not_done_cases
import calendar

def create_calendar(year, month):
    month_name = calendar.month_name[month]
    month_days = calendar.monthcalendar(year, month)

    header = [
        ft.Container(
            content=ft.Text(day, size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            width=50,
            alignment=ft.alignment.center,
        )
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    ]

    body = []
    for week in month_days:
        week_row = [
            ft.Container(
                content=ft.Text(str(day) if day != 0 else "", size=14, text_align=ft.TextAlign.CENTER),
                width=50,
                alignment=ft.alignment.center,
            )
            for day in week
        ]
        body.append(ft.Row(week_row, alignment=ft.MainAxisAlignment.CENTER, spacing=2))

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(f"{month_name} {year}", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row(header, alignment=ft.MainAxisAlignment.CENTER, spacing=2),
                *body
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        ),
        width=400,
        padding=10,
        margin=20,
        bgcolor="#2c3e50",
        border_radius=10,
    )


def dashboard_content():
    cases = get_not_done_cases("data/cases.csv")
    rows_per_page = 5
    current_page = 0
    total_pages = (len(cases) + rows_per_page - 1) // rows_per_page

    def create_case_tile(case_id, case_type, time, date):
        return ft.ListTile(
            leading=ft.Icon(ft.icons.BOOKMARK),
            title=ft.Text(f"Case #{case_id}"),
            subtitle=ft.Text(f"{case_type}, {time}, {date}"),
            trailing=ft.IconButton(ft.icons.MORE_VERT),
        )

    def build_case_tiles(page):
        start_index = page * rows_per_page
        end_index = start_index + rows_per_page
        page_cases = cases[start_index:end_index]
        return [
            create_case_tile(
                case_id=case["id"],
                case_type=case["judul"],
                time=case["tanggal_mulai"],
                date=case["tanggal_selesai"],
            )
            for case in page_cases
        ]

    def update_content(page):
        nonlocal current_page
        current_page = page
        case_container.content.controls = build_case_tiles(page)
        pagination_controls.controls[1].value = f"Page {page + 1} of {total_pages}"
        pagination_controls.controls[0].disabled = current_page == 0
        pagination_controls.controls[2].disabled = current_page + 1 >= total_pages
        container.update()

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
                disabled=current_page + 1 >= total_pages,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        width=300,
    )

    case_container = ft.Container(
        content=ft.Column(build_case_tiles(current_page)),
    )

    calendar_container = create_calendar(2024, 12)

    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Ongoing Cases"),
                case_container,
                pagination_controls,
                ft.Text("Calendar", size=30, weight=ft.FontWeight.BOLD),
                calendar_container,
            ],
        ),
        expand=True,
        padding=20,
    )

    return container