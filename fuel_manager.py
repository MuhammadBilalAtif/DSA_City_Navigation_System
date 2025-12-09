# fuel_manager.py

import math
from typing import Any, Dict, List, Optional, Tuple, Union

from data_points import GAS_STATIONS
from db_utils import get_point_by_name


StopType = Union[str, Dict[str, Any]]  # string name or {lat, lon, name}


def get_lat_lon(stop: StopType) -> Optional[Tuple[float, float]]:
    """
    Given a stop which might be:
      - dict with 'lat'/'lon'
      - string name (lookup via DB / dictionaries)
    return (lat, lon) or None.
    """
    if isinstance(stop, dict):
        return stop.get("lat"), stop.get("lon")
    return get_point_by_name(stop)


def estimate_total_distance_km(stops: List[StopType]) -> float:
    """
    Roughly estimate total distance between consecutive stops using
    straight-line * 1.3 as a road factor.
    """
    total_est_dist = 0.0
    for i in range(len(stops) - 1):
        p1 = get_lat_lon(stops[i])
        p2 = get_lat_lon(stops[i + 1])
        if p1 is None or p2 is None:
            continue
        # lat/lon distance in degrees -> km
        dist_km = math.dist(p1, p2) * 111.0 * 1.3
        total_est_dist += dist_km
    return total_est_dist


def choose_fuel_stop(
    stops: List[StopType],
    fuel_params: Optional[Dict[str, Any]],
) -> Tuple[List[StopType], bool, Optional[str]]:
    """
    Decide if a fuel stop is needed, and if so, insert the nearest gas station
    after the start stop.

    Returns:
        (updated_stops, fuel_alert_bool, fuel_stop_name_or_None)
    """
    fuel_alert = False
    stop_added: Optional[str] = None

    if fuel_params is None:
        return stops, fuel_alert, stop_added

    try:
        avg_raw = str(fuel_params.get("avg", "")).strip()
        curr_raw = str(fuel_params.get("curr", "")).strip()

        if avg_raw == "" or curr_raw == "":
            return stops, fuel_alert, stop_added

        avg_kpl = float(avg_raw)
        curr_liters = float(curr_raw)

        if avg_kpl <= 0 or curr_liters < 0:
            return stops, fuel_alert, stop_added

        max_range_km = avg_kpl * curr_liters
        total_est_dist = estimate_total_distance_km(stops)

        if total_est_dist > max_range_km:
            fuel_alert = True
            s_lat, s_lon = get_lat_lon(stops[0])

            if GAS_STATIONS and s_lat is not None and s_lon is not None:
                # find nearest station to starting point
                best_st_name = min(
                    GAS_STATIONS.keys(),
                    key=lambda k: math.dist((s_lat, s_lon), GAS_STATIONS[k]),
                )
                stops.insert(1, best_st_name)  # insert after start
                stop_added = best_st_name
                print(f"⛽ Low Fuel! Rerouting via {best_st_name}")
            else:
                print("⚠️ Gas stations dict is empty or start coords invalid.")
    except Exception as e:
        print(f"Fuel Logic Error: {e}")

    return stops, fuel_alert, stop_added
