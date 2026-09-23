def count_fingers(hand_landmarks):

    fingers = 0

    # -----------------------------
    # Thumb
    # -----------------------------

    # Thumb tip = 4
    # Thumb joint = 3

    if hand_landmarks[4].x > hand_landmarks[3].x:
        fingers += 1


    # -----------------------------
    # Index finger
    # -----------------------------

    # Tip = 8
    # Joint = 6

    if hand_landmarks[8].y < hand_landmarks[6].y:
        fingers += 1


    # -----------------------------
    # Middle finger
    # -----------------------------

    # Tip = 12
    # Joint = 10

    if hand_landmarks[12].y < hand_landmarks[10].y:
        fingers += 1


    # -----------------------------
    # Ring finger
    # -----------------------------

    # Tip = 16
    # Joint = 14

    if hand_landmarks[16].y < hand_landmarks[14].y:
        fingers += 1


    # -----------------------------
    # Little finger
    # -----------------------------

    # Tip = 20
    # Joint = 18

    if hand_landmarks[20].y < hand_landmarks[18].y:
        fingers += 1


    return fingers