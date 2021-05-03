import time

class LicensePlatesRecognitionStats:
    def __init__(self):
        self.location_time = 0
        self.recognition_time = 0
        self.found_plates = 0
        self.all_plates = 0
        self.correctly_found_plates = 0
        self.average_recognition_accuracy = 0
        self.images_processed = 0
        self.images_to_process = 1
        self.all_process_time = time.time()

    def show(self, args):
        print("\n-----------------STATS-----------------")
        print("Processed images:", self.images_processed)
        if args["verify_locations"]:
            print("All available plates:", self.all_plates)
        print("Found plates:", self.found_plates)
        if args["verify_locations"]:
            print("Correctly found plates:", self.correctly_found_plates)
            print("Average location accuracy:", str(round(self.correctly_found_plates/self.found_plates * 100, 2)) + '%')
        if not args["verify_locations"] and args["verify_characters_recognition"]:
            print("Average recognition accuracy:", str(round(self.average_recognition_accuracy / self.images_processed, 2)) + '%')
        if args["verify_locations"] and args["verify_characters_recognition"]:
            print("Average recognition accuracy:", str(round(self.average_recognition_accuracy/self.correctly_found_plates, 2)) + '%')
        location_time = round(self.location_time * 1000)
        recognition_time = round(self.recognition_time * 1000)
        all_process_time = round((time.time() - self.all_process_time) * 1000)
        print("----------------TIMERS----------------")
        print("Location time:", location_time, "ms")
        print("Recognition time:", recognition_time, "ms")
        print("All process time:", all_process_time, "ms")
        print("Time for image:", all_process_time/self.images_processed, "ms")
        print(round((self.images_processed/all_process_time)*1000,2), "images/s")
