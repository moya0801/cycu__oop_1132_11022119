def filter_bus_stops(bus_stops_gdf, bus_stops_df):
    """
    根據站牌資訊篩選公車站牌。
    """
    # 列出 SHP 檔案的所有欄位
    print("Available columns in SHP file:", bus_stops_gdf.columns)

    # 動態選擇站牌名稱欄位
    stop_name_column = None
    for column in bus_stops_gdf.columns:
        if column.lower() in ["bsm_chines", "stopname", "name", "站名", "站牌名稱"]:  # 假設可能的欄位名稱
            stop_name_column = column
            break

    if not stop_name_column:
        raise ValueError("The shapefile must contain a column for stop names (e.g., 'BSM_CHINES', 'STOPNAME', 'NAME').")

    print(f"Using column '{stop_name_column}' as the stop name column.")

    # 列出 BSM_CHINES 欄位的所有值
    print("Values in stop name column (BSM_CHINES):", bus_stops_gdf[stop_name_column].unique())

    # 清理資料：去除空格並轉換為小寫
    bus_stops_gdf[stop_name_column] = bus_stops_gdf[stop_name_column].str.strip().str.lower()
    bus_stops_df["stop_name"] = bus_stops_df["stop_name"].str.strip().str.lower()

    # 篩選公車站牌
    filtered_gdf = bus_stops_gdf[bus_stops_gdf[stop_name_column].isin(bus_stops_df["stop_name"])]
    if filtered_gdf.empty:
        print("Warning: No matching bus stops found in the shapefile for the given data.")
    return filtered_gdf