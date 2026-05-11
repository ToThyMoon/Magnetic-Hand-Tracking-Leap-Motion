import leap
import numpy as np
import matplotlib.pyplot as plt
import time

class Listener(leap.Listener):
    hands = None
    def on_tracking_event(self, event):
        self.hands = event.hands

    def on_device_event(self, event):
        try:
            with event.device.open():
                info = event.device.get_info()
        except leap.LeapCannotOpenDeviceError:
            info = event.device.get_info()

        print(f"Found device {info.serial}")


def main():
    # Initialize connection
    connection = leap.Connection()
    listener = Listener()
    connection.add_listener(listener)
    connection.set_tracking_mode(leap.TrackingMode.Desktop)
    t0 = time.time_ns()
    prev_hand_pos = [0,0,0]
    maximum = 0
    minimum = 1e20
    try:
        with connection.open():

            while True:
                # time.sleep(0.01)

                if listener.hands is not None:
                    
                    for hand in listener.hands:
                        hand_type = "Left" if hand.type == leap.HandType.Left else "Right"
                        
                        if (np.round(prev_hand_pos, 3) != np.round(list(hand.palm.position), 3)).all():
                            prev_hand_pos = list(hand.palm.position)
                            print(f"{hand_type} hand at {list(hand.palm.position)} with {hand.confidence}")

                            dif = time.time_ns() - t0
                            print(dif)
                            maximum = max(maximum, dif)
                            minimum = min(minimum, dif)
                            t0 = time.time_ns()
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    finally:
        print(f"Max: {maximum}\nMin: {minimum}")

if __name__ == "__main__":
    main()