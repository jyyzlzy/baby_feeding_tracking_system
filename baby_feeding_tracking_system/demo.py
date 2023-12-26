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
    config = {
        'data_filepath': filepath,
        'datetime_format': "%m/%d/%y %H:%M:%S",
        'width': 1000,
        'height': 800,
        'primary_font_size': 60,
        'secondary_font_size': 30,
        'primary_text_location_x': 200,
        'primary_text_location_y': 150,
        'secondary_text_location_x': 250,
        'secondary_text_location_y': 500,
        'warning_text_location_x': 100,
        'warning_text_location_y': 100,
    }
    fts = LiamLocalFeedingTrackingSystem(config)
    fts.run()

if __name__ == "__main__":
    main()