"""This Module is responsible for getting valid proxies"""
from queue import Queue

from logic.proxy.chcek_proxies import check_proxies
from logic.proxy.proxy_object import ProxyObjectDto
from logic.proxy.scrape_proxies import scrape_proxies_pipeline


def get_proxies_objects_list(url: str = 'https://free-proxy-list.net/', element_class: str = 'table table-striped table-bordered', proxy_validation_url="http://ipinfo.io/json"):
    proxies_queue: Queue[ProxyObjectDto] = scrape_proxies_pipeline(url=url, element_class=element_class)

    valid_proxies = check_proxies(proxies_queue, proxy_validation_url)

    return valid_proxies


def get_proxies_list(url: str = 'https://free-proxy-list.net/', element_class: str = 'table table-striped table-bordered', proxy_validation_url="http://ipinfo.io/json"):
    proxies_objects_list: list[ProxyObjectDto] = get_proxies_objects_list(url, element_class, proxy_validation_url)
    return [f"{proxy.ip_address}:{proxy.port}" for proxy in proxies_objects_list]


