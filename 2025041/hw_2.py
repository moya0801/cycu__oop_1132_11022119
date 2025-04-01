import requests
import html
import pandas as pd
from bs4 import BeautifulSoup

def get_stop_info(stop_link: str) -> dict:
    """
    Retrieve real-time information for a specific bus stop.

    Args:
        stop_link (str): The relative URL of the bus stop.

    Returns:
        dict: A dictionary containing real-time information for the bus stop.
    """
    url = f'https://pda5284.gov.taipei/MQS/{stop_link}'
    stop_id = stop_link.split("=")[1]  # Extract stop ID from the link

    # Send GET request
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract real-time information (e.g., arrival times, vehicle status)
        real_time_info = []
        table = soup.find("table", class_="realTimeTable")  # Adjust class name based on actual HTML
        if table:
            for tr in table.find_all("tr")[1:]:  # Skip the header row
                tds = tr.find_all("td")
                if len(tds) >= 2:
                    bus_number = tds[0].text.strip()
                    arrival_time = tds[1].text.strip()
                    real_time_info.append({"bus_number": bus_number, "arrival_time": arrival_time})

        return {"stop_id": stop_id, "real_time_info": real_time_info}
    else:
        print(f"無法下載網頁，HTTP 狀態碼: {response.status_code}")
        return {"stop_id": stop_id, "real_time_info": []}


def get_bus_route(rid: str):
    """
    Retrieve two DataFrames containing bus stop names and their corresponding URLs based on the route ID (rid).

    Args:
        rid (str): Bus route ID.

    Returns:
        tuple: Two Pandas DataFrames, each corresponding to one direction of the bus route.
    """
    url = f'https://pda5284.gov.taipei/MQS/route.jsp?rid={rid}'

    # Send GET request
    response = requests.get(url)
    if response.status_code == 200:
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all tables
        tables = soup.find_all("table")

        # Initialize DataFrame list
        dataframes = []

        # Iterate through tables
        for table in tables:
            rows = []
            # Find all tr tags with the specified classes
            for tr in table.find_all("tr", class_=["ttego1", "ttego2"]):
                # Extract stop name and link
                td = tr.find("td")
                if td:
                    stop_name = html.unescape(td.text.strip())  # Decode stop name
                    stop_link = td.find("a")["href"] if td.find("a") else None

                    if stop_link:
                        # Call get_stop_info function to get stop information
                        stop_info = get_stop_info(stop_link)
                        print(f"站點: {stop_name}, 即時資訊: {stop_info['real_time_info']}")

                    # Append to rows
                    rows.append({"stop_name": stop_name, "stop_link": stop_link})
            # If data exists, convert to DataFrame
            if rows:
                df = pd.DataFrame(rows)
                dataframes.append(df)

        # Return two DataFrames
        if len(dataframes) >= 2:
            return dataframes[0], dataframes[1]
        else:
            raise ValueError("Insufficient table data found.")
    else:
        raise ValueError(f"Failed to download webpage. HTTP status code: {response.status_code}")


def get_all_routes():
    """
    Retrieve all bus routes from the main route list page and fetch real-time information for each route.

    Returns:
        None
    """
    url = 'https://pda5284.gov.taipei/MQS/routelist.jsp'

    # Send GET request
    response = requests.get(url)
    if response.status_code == 200:
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all route links
        route_links = soup.find_all("a", href=True)
        all_routes_data = []

        for link in route_links:
            if "route.jsp?rid=" in link["href"]:
                rid = link["href"].split("=")[1]
                route_name = link.text.strip()
                print(f"\n正在處理路線: {route_name} (ID: {rid})")

                try:
                    df1, df2 = get_bus_route(rid)
                    df1["route_name"] = route_name
                    df1["direction"] = "去程"
                    df2["route_name"] = route_name
                    df2["direction"] = "回程"

                    # Append data to the list
                    all_routes_data.append(df1)
                    all_routes_data.append(df2)
                except ValueError as e:
                    print(f"Error processing route {route_name}: {e}")

        # Combine all data and save to CSV
        if all_routes_data:
            final_df = pd.concat(all_routes_data, ignore_index=True)
            final_df.to_csv("all_routes_real_time_info.csv", index=False, encoding="utf-8-sig")
            print("\n所有路線的即時資訊已儲存至 all_routes_real_time_info.csv")
    else:
        print(f"無法下載路線列表，HTTP 狀態碼: {response.status_code}")


# Test function
if __name__ == "__main__":
    get_all_routes()