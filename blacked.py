import os
import sys
import json
import csv
import time
import socket
import argparse
from urllib.parse import urlparse
from datetime import datetime
from shodan import Shodan, APIError
from rich.console import Console
from rich.table import Table

console = Console()

API_FILE = "apikey.json"
JSON_OUT = "sendata.json"
CSV_OUT = "sendata.csv"

def print_banner():
    banner = r"""
[bold red]

 ▄▄▄▄    ██▓    ▄▄▄       ▄████▄   ██ ▄█▀▓█████ ▓█████▄      
▓█████▄ ▓██▒   ▒████▄    ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▒██▀ ██▌     
▒██▒ ▄██▒██░   ▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ▒███   ░██   █▌     
▒██░█▀  ▒██░   ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ░▓█▄   ▌     
░▓█  ▀█▓░██████▒▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░▒████▓  ██▓ 
░▒▓███▀▒░ ▒░▓  ░▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░ ▒▒▓  ▒  ▒▓▒ 
▒░▒   ░ ░ ░ ▒  ░ ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░ ░ ▒  ▒  ░▒  
 ░    ░   ░ ░    ░   ▒   ░        ░ ░░ ░    ░    ░ ░  ░  ░   
 ░          ░  ░     ░  ░░ ░      ░  ░      ░  ░   ░      ░  
      ░                  ░                       ░        ░  
 
[/bold red]
    [bold cyan]> Shodan Elite Scanner — 2025 Edition <[/bold cyan]
"""
    console.print(banner)

def load_api_key():
    if os.path.exists(API_FILE):
        with open(API_FILE, 'r') as f:
            return json.load(f).get("api_key")
    else:
        key = input("[+] Enter your Shodan API Key: ").strip()
        with open(API_FILE, 'w') as f:
            json.dump({"api_key": key}, f)
        return key

def save_json(results):
    with open(JSON_OUT, 'w') as f:
        json.dump(results, f, indent=4)

def save_csv(results):
    keys = ["ip", "port", "org", "hostnames", "location", "domains", "timestamp"]
    with open(CSV_OUT, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in results:
            row = {k: r.get(k) for k in keys}
            writer.writerow(row)

def display_results(results):
    table = Table(title="Shodan Results", show_lines=True)
    table.add_column("#", justify="right")
    table.add_column("IP")
    table.add_column("Port")
    table.add_column("Org")
    table.add_column("Hostnames")
    table.add_column("Location")
    for i, r in enumerate(results, start=1):
        table.add_row(
            str(i),
            str(r.get("ip")),
            str(r.get("port")),
            str(r.get("org", "N/A")),
            ", ".join(r.get("hostnames", [])),
            str(r.get("location", {}).get("country_name", "N/A"))
        )
    console.print(table)

def query_search(api, query, limit):
    console.print(f"[bold cyan]Searching for:[/bold cyan] {query}")
    results = []
    count = 0
    try:
        for banner in api.search_cursor(query):
            data = {
                "ip": banner.get("ip_str"),
                "port": banner.get("port"),
                "org": banner.get("org", "N/A"),
                "hostnames": banner.get("hostnames", []),
                "location": banner.get("location", {}),
                "domains": banner.get("domains", []),
                "data": banner.get("data", ""),
                "timestamp": datetime.now().isoformat()
            }
            results.append(data)
            count += 1
            if count >= limit:
                break
            time.sleep(0.2)
    except APIError as e:
        console.print(f"[bold red]API Error:[/bold red] {e}")
    return results

def ip_lookup(api, ip):
    console.print(f"[bold cyan]Looking up IP:[/bold cyan] {ip}")
    try:
        host = api.host(ip)
        data = {
            "ip": host.get("ip_str"),
            "port": host.get("port"),
            "org": host.get("org", "N/A"),
            "hostnames": host.get("hostnames", []),
            "location": host.get("location", {}),
            "domains": host.get("domains", []),
            "data": str(host),
            "timestamp": datetime.now().isoformat()
        }
        return [data]
    except APIError as e:
        console.print(f"[bold red]API Error:[/bold red] {e}")
        return []

def resolve_url_to_ip(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        ip = socket.gethostbyname(domain)
        console.print(f"[bold green]Resolved {domain} to {ip}[/bold green]")
        return ip
    except Exception as e:
        console.print(f"[bold red]Failed to resolve domain: {e}[/bold red]")
        return None

def main():
    parser = argparse.ArgumentParser(description="Shodan Elite Scanner — 2025 Edition")
    parser.add_argument("--query", help="Search Shodan with a keyword query")
    parser.add_argument("--ip", help="Search a specific IP address")
    parser.add_argument("--url", help="Provide a website URL to scan by IP")
    parser.add_argument("--limit", type=int, default=50, help="Limit number of results")
    parser.add_argument("--csv", action="store_true", help="Save results to sendata.csv")
    args = parser.parse_args()
    print_banner()

    if not args.query and not args.ip and not args.url:
        console.print("[bold yellow]Please provide --query, --ip or --url[/bold yellow]")
        sys.exit(1)

    api_key = load_api_key()
    api = Shodan(api_key)
    try:
        api.info()
    except APIError:
        console.print("[bold red]Invalid API key. Please check your apikey.json[/bold red]")
        sys.exit(1)

    results = []
    if args.query:
        results = query_search(api, args.query, args.limit)
    elif args.ip:
        results = ip_lookup(api, args.ip)
    elif args.url:
        resolved_ip = resolve_url_to_ip(args.url)
        if resolved_ip:
            results = ip_lookup(api, resolved_ip)

    if results:
        save_json(results)
        if args.csv:
            save_csv(results)
        display_results(results)
    else:
        console.print("[bold red]No results found.[/bold red]")

if __name__ == "__main__":
    main()
