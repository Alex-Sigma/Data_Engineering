from lec02.bll.sales_pipeline import save_sales_to_local_disk

if __name__ == "__main__":
    save_sales_to_local_disk(
        date="2022-08-09",
        raw_dir="raw/sales/2022-08-09"
    )
