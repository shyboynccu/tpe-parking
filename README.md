tpe-parking
===========
台北市停車場資料查詢

A python library to provide public parking lot information around Taipei area.

Requirement
-----------

geopy, twd97

To install the required dependencies, use pip.

    $ pip install geopy
    $ pip install twd97

Example
-------
可查詢座標點附近某一指定距離內的停車場

List all parking lots within 1000 meters of a specified location.

    info_provider = tpe_parking_lot.ParkingLotInfoProvider()
    my_location = (25.042722, 121.614563) #somewhere close to Academia Sinica TW

    for park in info_provider.find_parking_lot_by_coordinate(my_location, 1000):
        print('[{0}] {1}'.format(park['area'], park['name']))


Parking Lot
-----------

Parking lot information is provided by http://data.taipei/.

LICENSE
-------
MIT
