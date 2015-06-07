from tpe_parking import ParkingLotInfoProvider

def main():
    info_provider = ParkingLotInfoProvider()
    #for park in info_provider.find_parking_lot('信義區'):
    #    print(park['name'])
    my_location = (25.041340, 121.611751)

    for park in info_provider.find_parking_lot_by_coordinate(my_location, 1000):
        #print('[{0}] {1}, Entrance:{2}'.format(park['area'], park['name'], [x['Addresss'] for x in park['Entrancecoord']['EntrancecoordInfo']]))
        print('[{0}] {1}'.format(park['area'], park['name']))

if __name__ == '__main__':
    main()
