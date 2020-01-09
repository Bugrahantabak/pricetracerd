import db
import scraper
import time

URL = "https://www.amazon.in/gp/product/B00IJRV2D0?pf_rd_p=f2b20090-067d-415f-953d-b8dcecc9109f&pf_rd_r=VFJ98F93X80YWYQNR3GN"


def run():
    details = scraper.get_product_details(URL)

    result = ""
    if details is None:
        result = "not done NONE"
    else:
        inserted = db.add_product_detail(details)
        if inserted:
            result = "done"
        else:
            result = "not done"
    return result


while True:
    print(run())
    time.sleep(60)
