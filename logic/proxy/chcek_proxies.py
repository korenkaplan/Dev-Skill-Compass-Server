import concurrent.futures
import requests
from queue import Queue
from logic.proxy.proxy_object import ProxyObjectDto
from logic.proxy.scrape_proxies import scrape_proxies_pipeline


def check_proxy(proxy: ProxyObjectDto, proxy_validation_url: str, timeout: int = 5) -> bool:
    proxy_protocol = "https" if proxy.https else "http"
    full_proxy_address = f"{proxy.ip_address}:{proxy.port}"
    try:
        res = requests.get(proxy_validation_url, proxies={proxy_protocol: full_proxy_address}, timeout=timeout)
        return res.status_code == 200
    except Exception as e:
        print(f"Error checking proxy {full_proxy_address}: {e}")
        return False


def check_proxies(proxies_queue: Queue[ProxyObjectDto], proxy_validation_url: str, timeout: int = 5):
    valid_proxies = []

    def worker(proxy):
        if check_proxy(proxy, proxy_validation_url, timeout):
            valid_proxies.append(proxy)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        while not proxies_queue.empty():
            proxy = proxies_queue.get()
            futures.append(executor.submit(worker, proxy))

        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()  # Will raise exceptions if any occurred in the worker function

    return valid_proxies


def main():
    proxies_queue = scrape_proxies_pipeline()
    proxy_validation_url = "http://ipinfo.io/json"
    valid_proxies = check_proxies(proxies_queue, proxy_validation_url)
    for proxy in valid_proxies:
        print(f"ip_address='{proxy.ip_address}' port={proxy.port} https={proxy.https}")


if __name__ == "__main__":
    main()
