import cv2
import mediapipe as mp

from gesture import count_fingers

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# -----------------------------
# MediaPipe Hand Landmarker
# -----------------------------

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


# -----------------------------
# Open Laptop Camera
# -----------------------------

camera = cv2.VideoCapture(0)

frame_timestamp = 0


# -----------------------------
# Main Loop
# -----------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("Could not access camera")
        break

    # OpenCV uses BGR
    # MediaPipe expects RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Convert frame to MediaPipe image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    # Detect hands
    result = detector.detect_for_video(
        mp_image,
        frame_timestamp
    )

    frame_timestamp += 1


    # -----------------------------
    # Process detected hands
    # -----------------------------

    if result.hand_landmarks:

        for hand in result.hand_landmarks:

            # Count raised fingers
            finger_count = count_fingers(hand)


            # Display finger count
            cv2.putText(
                frame,
                f"Fingers: {finger_count}",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )


            # Draw hand landmarks
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


    # -----------------------------
    # Show camera
    # -----------------------------

    cv2.imshow(
        "Hand Gesture Recognition",
        frame
    )


    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# -----------------------------
# Cleanup
# -----------------------------

camera.release()

cv2.destroyAllWindows()