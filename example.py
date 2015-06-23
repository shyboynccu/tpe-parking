from tpe_parking import ParkingLotInfoProvider

def main():
    info_provider = ParkingLotInfoProvider()
    #info_provider.update_db()

    my_location = (25.041340, 121.611751)

    parks = info_provider.find_parking_lot_by_coordinate(my_location, 1000)
    parks = info_provider.find_parking_lot('信義區')
    for park in parks:
        #print('[{0}] {1}, Entrance:{2}'.format(park['area'], park['name'], [x['Addresss'] for x in park['Entrancecoord']['EntrancecoordInfo']]))
        park_available_space = info_provider.find_available_parking_space(park['id'])

        if park_available_space:
            print('[{0}] {1}(park_id: {2}) | Spaces available: {3}'.format(park['area'], park['name'], park['id'], park_available_space['availablecar']))
        else:
            print('[{0}] {1}(park_id: {2})'.format(park['area'], park['name'], park['id']))
            

if __name__ == '__main__':
    main()
