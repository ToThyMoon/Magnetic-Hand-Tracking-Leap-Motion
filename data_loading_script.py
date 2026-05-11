import numpy as np

from utils_modified import *
from sklearn import preprocessing, linear_model, neural_network, metrics, pipeline


def main():
    model = train_generic_hand_model()
    time_series_file = open("./magnetic_tracking_values.txt","r")

    while True:
        realtime_values_str = time_series_file.readline()
        print(realtime_values_str)
        if realtime_values_str == "":
            break
        realtime_values = np.fromstring(realtime_values_str, sep=",")
        # print(realtime_values)
        realtime_values_magnet = realtime_values[:data_num]
        realtime_values_angles = realtime_values[data_num:]     # expected angles from the model
        # print(realtime_values_magnet)
        predicted_angles = model.predict(realtime_values_magnet.reshape([1,-1])).flatten() * rad2deg
        # print(predicted_angles)

        print(f"\tMCP\tPIP\tDIP")
        for finger in ["index","middle","ring","pinky"]:
            print(f"{finger}:\t{predicted_angles[finger_angle_indices[f'{finger}_mcp']]:.2f}\t{predicted_angles[finger_angle_indices[f'{finger}_pip']]:.2f}\t{predicted_angles[finger_angle_indices[f'{finger}_pip']]:.2f}\t")
        print(f"\tTM\tMCP\tIP")
        for finger in ["thumb"]:
            print(f"{finger}:\t{predicted_angles[finger_angle_indices[f'{finger}_mcp']]:.2f}\t{predicted_angles[finger_angle_indices[f'{finger}_pip']]:.2f}\t{predicted_angles[finger_angle_indices[f'{finger}_pip']]:.2f}\t")
            

        time.sleep(0.05)        # this is the delay I set for the realtime recording

    return


def train_generic_hand_model():
    # thumb_dataset = 0
    models = {
        "thumb":    pipeline.Pipeline([("scaling", preprocessing.MinMaxScaler()),("clf", neural_network.MLPRegressor([200, 200, 200], activation='relu', learning_rate_init=0.01, max_iter=1000))]),
        "index":    pipeline.Pipeline([("scaling", preprocessing.MinMaxScaler()),("clf", neural_network.MLPRegressor([200, 200, 200], activation='relu', learning_rate_init=0.01, max_iter=1000))]),
        "middle":   pipeline.Pipeline([("scaling", preprocessing.MinMaxScaler()),("clf", neural_network.MLPRegressor([200, 200, 200], activation='relu', learning_rate_init=0.01, max_iter=1000))]),
        "ring":     pipeline.Pipeline([("scaling", preprocessing.MinMaxScaler()),("clf", neural_network.MLPRegressor([200, 200, 200], activation='relu', learning_rate_init=0.01, max_iter=1000))]),
        "pinky":    pipeline.Pipeline([("scaling", preprocessing.MinMaxScaler()),("clf", neural_network.MLPRegressor([200, 200, 200], activation='relu', learning_rate_init=0.01, max_iter=1000))]),
        "wrist":    None,
    }
    thumb_dataset = np.genfromtxt("./datasets/thumb2.txt", delimiter=',')
    finger_dataset = np.genfromtxt("./datasets/fingers_adjusted.txt", delimiter=',')
    # wrist_dataset = np.genfromtxt("./datasets/wrist.txt", delimiter=',')
    x_finger = finger_dataset[:,:24]
    y_finger = finger_dataset[:,24:]
    y_finger = np.radians(y_finger)

    model = Generic_Hand_Model(models)


    # not using wrist for now, though we may need to display it in the future
    # model.fit_finger(wrist_dataset[:,:data_num], np.radians(wrist_dataset[:,data_num:]), "wrist")
    # model.models["wrist"] = load_model(f"wrist")

    # this is for creating a new model     
    # model.fit_finger(x_finger, y_finger, "index")
    # model.fit_finger(x_finger, y_finger, "middle")
    # model.fit_finger(x_finger, y_finger, "ring")
    # model.fit_finger(x_finger, y_finger, "pinky")
    # model.fit_finger(thumb_dataset[:,:data_num], np.radians(thumb_dataset[:,data_num:]), "thumb")
    
    # this is for using a preexisting model
    # if you make a model that works better, rename it avoid replacing it
    model.models["index"] = load_model(f"index2")
    model.models["middle"] = load_model(f"middle2")
    model.models["ring"] = load_model(f"ring2")
    model.models["pinky"] = load_model(f"pinky2")
    model.models["thumb"] = load_model(f"thumb2")
    return model

if __name__ == "__main__":
    main()