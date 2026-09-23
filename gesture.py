def count_fingers(hand_landmarks):

    fingers = 0

    # Thumb
    if hand_landmarks[4].x > hand_landmarks[3].x:
        fingers += 1

    # Index
    if hand_landmarks[8].y < hand_landmarks[6].y:
        fingers += 1

    # Middle
    if hand_landmarks[12].y < hand_landmarks[10].y:
        fingers += 1

    # Ring
    if hand_landmarks[16].y < hand_landmarks[14].y:
        fingers += 1

    # Little
    if hand_landmarks[20].y < hand_landmarks[18].y:
        fingers += 1

    return fingers


def recognize_gesture(finger_count):

    gestures = {
        0: "FIST",
        1: "ONE",
        2: "TWO",
        3: "THREE",
        4: "FOUR",
        5: "OPEN HAND"
    }

    return gestures.get(
        finger_count,
        "UNKNOWN"
    )