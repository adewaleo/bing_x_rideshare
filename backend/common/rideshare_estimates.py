# Author: GRFLOWER
# Date: 7/23/19
# Description: This file contains two separate functions that receive "distance" and "time duration" as inputs and outputs a price estimate for Uber and Lyft.

class LyftEstimate(object):

    base_fare = 1.42
    cancel_fee = 5.00
    cost_per_mile = 1.48
    cost_per_minute = 0.25
    max_fare = 400.00
    min_fare = 3.50
    schedule_ride_cancel_fee = 10.00
    service_fee = 2.00
    seattle_city_fee = 0.24

    @classmethod
    def estimate_fare(cls, distance, duration):
         total_cost_per_mile = distance * cls.cost_per_mile
         total_cost_per_minute = (duration/60) * cls.cost_per_minute
         fees = cls.base_fare + cls.service_fee + cls.seattle_city_fee
         fare = total_cost_per_mile + total_cost_per_minute + fees
         return fare


class UberEstimate(object):

    base_fare = 1.42
    cancel_fee = 5.00
    cost_per_mile = 1.48
    cost_per_minute = 0.25
    min_fare = 5.45
    booking_fee = 1.95

    @classmethod
    def estimate_fare(cls, distance, duration):
        # must calculate driver's distance from destination and include cost per minute/hour for pickup
        # must implement cancellations
        total_cost_per_mile = distance * cls.cost_per_mile
        total_cost_per_minute = (duration / 60) * cls.cost_per_minute
        fees = cls.base_fare + cls.booking_fee
        fare = total_cost_per_mile + total_cost_per_minute + fees
        return fare


if __name__ == '__main__':
    total_price_lyft = LyftEstimate.estimate_fare(10, 3600)
    print(total_price_lyft)

    total_price_uber = UberEstimate.estimate_fare(10, 3600)
    print(total_price_uber)