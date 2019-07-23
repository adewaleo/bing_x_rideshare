# Author: GRFLOWER
# Date: 7/23/19
# Description: This file contains two separate functions that receive "distance" and "time duration" as inputs and outputs a price estimate for Uber and Lyft.

class LyftEstimate:

    def __init__(self, distance, duration):
        self.base_fare = 1.42
        self.cancel_fee = 5.00
        self.cost_per_mile = 1.48
        self.cost_per_minute = 0.25
        self.max_fare = 400.00
        self.min_fare = 3.50
        self.schedule_ride_cancel_fee = 10.00
        self.service_fee = 2.00
        self.seattle_city_fee = 0.24
        self.distance = distance
        self.duration = duration

    def EstimateFare(self):
         total_cost_per_mile = self.distance * self.cost_per_mile
         total_cost_per_minute = (self.duration/60) * self.cost_per_minute
         fees = self.base_fare + self.service_fee + self.seattle_city_fee
         fare = total_cost_per_mile + total_cost_per_minute + fees
         return fare


class UberEstimate:
    def __init__(self, distance, duration):
        self.base_fare = 1.42
        self.cancel_fee = 5.00
        self.cost_per_mile = 1.48
        self.cost_per_minute = 0.25
        self.min_fare = 5.45
        self.booking_fee = 1.95
        self.distance = distance
        self.duration = duration

    def EstimateFare(self):
        # must calculate driver's distance from destination and include cost per minute/hour for pickup
        # must implement cancellations
        total_cost_per_mile = self.distance * self.cost_per_mile
        total_cost_per_minute = (self.duration / 60) * self.cost_per_minute
        fees = self.base_fare + self.booking_fee
        fare = total_cost_per_mile + total_cost_per_minute + fees
        return fare


if __name__ == '__main__':
    x = LyftEstimate(10, 3600)
    total_price_lyft = x.EstimateFare()
    print(total_price_lyft)

    y = UberEstimate(10, 3600)
    total_price_uber = y.EstimateFare()
    print(total_price_uber)