from baby_feeding_tracking_system import LiamLocalFeedingTrackingSystem

def get_filepath():
    return '/tmp/LiamLocalFeedingTrackingSystemDemo.tmp.txt'

def generate_data(): 
    past_feeding_times = [
        '12/25/23 13:55:26',
        '12/25/23 14:55:26',
        '12/25/23 15:55:26',
    ]
    filepath = get_filepath()
    with open(filepath, 'w') as f:
        for feeding_time_str in past_feeding_times:
            f.write(feeding_time_str)
            f.write('\n')

def main():
    generate_data()
    filepath = get_filepath()
    fts = LiamLocalFeedingTrackingSystem(filepath)
    fts.run()

if __name__ == "__main__":
    main()