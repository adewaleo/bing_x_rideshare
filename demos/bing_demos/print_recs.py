
import requests
import datetime

url = "http://127.0.0.1:5000/recommendations"

def get_input():
    source = input("Enter the source address (default to alki beach): ").strip() or "alki beach"
    destination = input("Enter the destination address (default to University of Washington): ").strip() or "university of washington"

    return source, destination


def get_recommendations(source, dest):
    params = {
        "start": source,
        "dest": dest,
        "optimise_for": "time"
    }

    resp = requests.post(url=url, json=params)

    return resp.json()

def get_duration_from_secs(duration):
    return datetime.timedelta(seconds=duration)

def print_recommendation_item(rec):
    trip_type = "hybrid" if rec["type"] == "complex" else rec["type"]
    print("Type: " + trip_type)
    print("Trip Start: {} - {}".format(rec["start_time"], rec["start"]["address"]))
    print("Trip Stop: {} - {}".format(rec["end_time"], rec["dest"]["address"]))
    print("Estimated Trip Time: {}".format(get_duration_from_secs(rec["duration"])))
    print("Estimated Trip Cost: {:.2f}".format(rec["cost"]))

    if trip_type == "hybrid":
        print("Itinerary:")
        for segment in rec["segments"]:
            print_segments(segment)
    print("\n")


def print_segments(seg):
    start_address = seg["start"]["address"] if seg["start"] else ""
    end_address = seg["dest"]["address"] if seg["dest"] else ""

    seg_str = "    Type: " + seg["mode"]
    seg_str += "    Trip Start: {} - {}".format(seg["start_time"], start_address)
    seg_str += "\nTrip Stop: {} - {}".format(seg["end_time"], end_address)
    seg_str += "\nInstruction: {}\n".format(seg["description"])
    seg_str += "    Duration: {}".format(get_duration_from_secs(seg["duration"]))
    seg_str += "    Cost: {}".format(seg["cost"] or "")
    seg_str += "\n"

    print(seg_str)


def main():

    while True:
        source, dest = get_input()
        recommendations = get_recommendations(source, dest)

        num_transit = 0
        num_hybrid = 0

        new_recs = []
        for rec in recommendations:
            if rec["type"] == "transit":
                if num_transit < 3:
                    new_recs.append(rec)
                    num_transit += 1
            elif rec["type"] == "complex":
                if num_hybrid < 3:
                    new_recs.append(rec)
                    num_hybrid += 1
            else:
                new_recs.append(rec)

        print("\n")
        for rec in new_recs:
            print_recommendation_item(rec)


if __name__ == '__main__':
    main()