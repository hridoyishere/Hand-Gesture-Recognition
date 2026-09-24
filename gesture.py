def detect_fingers(hand_landmarks, hand_label):

    fingers = []

    # Thumb
    if hand_label == "Right":
        if hand_landmarks[4].x < hand_landmarks[3].x:
            fingers.append("THUMB")

    elif hand_label == "Left":
        if hand_landmarks[4].x > hand_landmarks[3].x:
            fingers.append("THUMB")


    # Index
    if hand_landmarks[8].y < hand_landmarks[6].y:
        fingers.append("INDEX")


    # Middle
    if hand_landmarks[12].y < hand_landmarks[10].y:
        fingers.append("MIDDLE")


    # Ring
    if hand_landmarks[16].y < hand_landmarks[14].y:
        fingers.append("RING")


    # Little
    if hand_landmarks[20].y < hand_landmarks[18].y:
        fingers.append("LITTLE")


    return fingers