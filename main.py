import cv2
import mediapipe as mp
import serial
import time

from gesture import detect_fingers

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# MediaPipe Hand Landmarker
model_path = "hand_landmarker.task"

base_options = python.BaseOptions(
    model_asset_path=model_path
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2
)

detector = vision.HandLandmarker.create_from_options(
    options
)


# Open Laptop Camera
camera = cv2.VideoCapture(0)

frame_timestamp = 0


# Connect Arduino
arduino = serial.Serial(
    "/dev/ttyACM0",
    9600
)

# Wait for Arduino to reset
time.sleep(2)


# Main Loop
while True:

    success, frame = camera.read()

    if not success:
        print("Could not access camera")
        break


    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # Convert to MediaPipe Image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )


    # Detect Hands
    result = detector.detect_for_video(
        mp_image,
        frame_timestamp
    )

    frame_timestamp += 1


    # Process Detected Hands
    if result.hand_landmarks:

        for i, hand in enumerate(result.hand_landmarks):


            # Get Hand Name
            hand_label = (
                result.handedness[i][0].category_name
            )


            # Detect Individual Fingers
            fingers = detect_fingers(
                hand,
                hand_label
            )


            # Display Hand Name
            text_y = 40 + (i * 100)

            cv2.putText(
                frame,
                f"{hand_label} Hand",
                (20, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )


            # Display Detected Fingers
            finger_text = ", ".join(fingers)

            if not finger_text:
                finger_text = "NONE"

            cv2.putText(
                frame,
                f"Fingers: {finger_text}",
                (20, text_y + 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )


            # Send Finger Data to Arduino
            if fingers:

                finger_data = ",".join(fingers)

                arduino.write(
                    (finger_data + "\n").encode()
                )

            else:

                arduino.write(
                    b"NONE\n"
                )


            # Draw Hand Landmarks
            for landmark in hand:

                x = int(
                    landmark.x * frame.shape[1]
                )

                y = int(
                    landmark.y * frame.shape[0]
                )

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )


    # Show Camera
    cv2.imshow(
        "Hand Gesture Recognition",
        frame
    )


    # Press Q to Quit

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Cleanup
camera.release()

arduino.close()

cv2.destroyAllWindows()