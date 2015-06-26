#!/usr/bin/env python3
import tpe_parking_lot

def main():
    info_provider = tpe_parking_lot.ParkingLotInfoProvider()
    my_location = (25.042722, 121.614563) #somewhere close to Academia Sinica TW

    for park in info_provider.find_parking_lot_by_coordinate(my_location, 1000):
        print('[{0}] {1}'.format(park['area'], park['name']))

if __name__ == '__main__':
    main()