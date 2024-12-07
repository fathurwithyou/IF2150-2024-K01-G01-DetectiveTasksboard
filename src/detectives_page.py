import flet as ft
from models.detectives import Detective


def detectives_content():
    # Create an instance of the Detective class and get the data
    detective_instance = Detective()
    data = detective_instance.get_detectives()

    # Convert the DataFrame to a list of dictionaries
    data_list = data.to_dict(orient='records')

    # Pagination variables
    items_per_page = 10
    current_page = 1
    total_pages = (len(data_list) + items_per_page - 1) // items_per_page

    def get_paginated_data(page):
        start = (page - 1) * items_per_page
        end = start + items_per_page
        return data_list[start:end]

    def update_table(page):
        paginated_data = get_paginated_data(page)
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(item["id"]))),
                    ft.DataCell(ft.Text(item["nama"])),
                    ft.DataCell(ft.Text(item["nik"])),
                    ft.DataCell(ft.Text(str(item["id_kasus"]))),
                    ft.DataCell(ft.Text("Edit")),
                ]
            )
            for item in paginated_data
        ]
        current_page_text.value = f"Page {page} of {total_pages}"
        page_container.update()

    # Initial table data
    paginated_data = get_paginated_data(current_page)

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("NIK")),
            ft.DataColumn(ft.Text("Case ID")),
            ft.DataColumn(ft.Text("Actions")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(item["id"]))),
                    ft.DataCell(ft.Text(item["nama"])),
                    ft.DataCell(ft.Text(item["nik"])),
                    ft.DataCell(ft.Text(str(item["id_kasus"]))),
                    ft.DataCell(ft.Text("Edit")),
                ]
            )
            for item in paginated_data
        ],
    )

    current_page_text = ft.Text(f"Page {current_page} of {total_pages}")

    def on_prev_click(e):
        nonlocal current_page
        if current_page > 1:
            current_page -= 1
            update_table(current_page)

    def on_next_click(e):
        nonlocal current_page
        if current_page < total_pages:
            current_page += 1
            update_table(current_page)

    pagination_controls = ft.Row(
        [
            ft.IconButton(ft.icons.CHEVRON_LEFT, on_click=on_prev_click),
            current_page_text,
            ft.IconButton(ft.icons.CHEVRON_RIGHT, on_click=on_next_click),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Detectives", size=30, weight=ft.FontWeight.BOLD),
                ft.TextField(label="Search Detectives...", width=300),
                table,
                pagination_controls,
            ]
        ),
        expand=True,
        padding=20,
    )

    return page_container
