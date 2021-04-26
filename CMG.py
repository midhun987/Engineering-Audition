import math
class Recording:

    def __init__(self):
        self.recorded_values = []
        self.recording_type:str = ""
        self.recording_name:str = ""
    
    def sensor_details(self, line):
        self.recording_name = line.split()[1]
        self.recording_type = line.split()[0]
    
    def record_sensor_readings(self,line):
        self.recorded_values.append(float(line.split()[1]))

    def mean(self):
        n = len(self.recorded_values)
        mean = sum(self.recorded_values) / n
        return mean
    
    def variance(self):
        n = len(self.recorded_values)
        mean = sum(self.recorded_values) / n
        deviations = [(x - mean) ** 2 for x in self.recorded_values]
        variance = sum(deviations) / n
        return variance

    def standarad_deviation(self): 
        var = self.variance()
        std_dev = math.sqrt(var)
        return std_dev

class SensorEvaulation:

    def __init__(self):
        self.ideal_humidity = 0
        self.ideal_humidity = 0

    def read_ideal_recordings(self,ideal_recording):
        inputs= ideal_recording.split()
        self.ideal_temparature = float(inputs[1])
        self.ideal_humidity = float(inputs[2])

    def check_sensor_temparature(self,recording):
        recorded_temparature = recording.mean()
        recorded_standard_deviation = recording.standarad_deviation()
        if (abs(recorded_temparature - self.ideal_temparature)) <= 0.5 and (recorded_standard_deviation <= 3):
            return "ultra precise"
        elif (abs(recorded_temparature - self.ideal_temparature)) <= 0.5 and (recorded_standard_deviation <= 5):
            return "very precise"
        else:
            return "precise"
    
    def check_sensor_humidity(self,recording):
        for val in recording.recorded_values:
            if (abs(val- self.ideal_humidity)) >= 1:
                return( "discard")
        return("keep")

    def determine_sensor_type(self,recording):
        if (recording.recording_type == "thermometer"):
            return recording.recording_name, self.check_sensor_temparature(recording)
        else:
            return recording.recording_name,self.check_sensor_humidity(recording)
           

    def evaluate(self,filename):
        output = {} #output dict
        fp = open(filename, "r") #file pointer 
        ideal_recordings = fp.readline() #reading ideal recordings in the text file
        self.read_ideal_recordings(ideal_recordings) # intialize in the SensorEvaulation class to respective variables
        # initiating the first recording evaulation
        recording = Recording()
        recording.sensor_details(fp.readline())
        # reading recorded values in the log
        lines = fp.readlines()
        for line in lines:
            # to init new recording and assign the previous record evaluation result to output var
            if "thermometer" in line or "humidity" in line:
                reading_name,evaluation = self.determine_sensor_type(recording)
                output[reading_name] = evaluation
                # creating object for new recording
                recording = Recording()
                recording.sensor_details(line)
            else:    
                # assign record values to respective object
                recording.record_sensor_readings(line)
        # reading the last recording evaluation
        reading_name,evaluation = self.determine_sensor_type(recording)
        output[reading_name] = evaluation
        # returing the all evaluations
        return(output)  

if __name__ == "__main__":
    sensors_evaluation = SensorEvaulation()
    evaluations = sensors_evaluation.evaluate("CMG_data.txt")
    print(evaluations)







     

