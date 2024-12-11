# models/destination_model.py
from dummy_db import destinations

def get_all_destinations(filters=None):
    if filters:
        filtered_destinations = [destination for destination in destinations if all(destination.get(k) == v for k, v in filters.items())]
        return filtered_destinations
    return destinations

def get_destination_by_id(destination_id):
    for destination in destinations:
        if destination['destination_id'] == destination_id:
            return destination
    return None

def add_new_destination(destination_data):
    destination = {
        "destination_id": str(len(destinations) + 1),  # Simple way to generate a new ID
        "name": destination_data.get("name"),
        "region": destination_data.get("region"),
        "type": destination_data.get("type"),
        "description": destination_data.get("description"),
        "images": destination_data.get("images"),
        "highlights": destination_data.get("highlights"),
        "best_time_to_visit": destination_data.get("best_time_to_visit")
    }
    destinations.append(destination)
    return destination
