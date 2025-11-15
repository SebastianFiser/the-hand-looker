import cv2
import mediapipe as mp
import threading
import time

# --- Inicializace kamery ---
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 360)   # vyšší rozlišení, stále přijatelné
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


# --- Mediapipe ---
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)

# --- Proměnné sdílené mezi vlákny ---
frame_lock = threading.Lock()
shared_frame = None
shared_landmarks = None

def capture_and_process():
    global shared_frame, shared_landmarks
    while True:
        success, frame = cap.read()
        if not success:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        # Zpracování landmarks
        landmarks_copy = []
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                landmarks_copy.append(hand_landmarks)

        # Uzamknout a uložit frame + landmarks
        with frame_lock:
            shared_frame = frame.copy()
            shared_landmarks = landmarks_copy

# --- Spustíme vlákno ---
thread = threading.Thread(target=capture_and_process, daemon=True)
thread.start()

prev_time = 0

while True:
    display_frame = None
    with frame_lock:
        if shared_frame is not None:
            display_frame = shared_frame.copy()
            if shared_landmarks:
                for hand_landmarks in shared_landmarks:
                    mp_drawing.draw_landmarks(
                        display_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

    if display_frame is not None:
        # --- FPS ---
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
        prev_time = curr_time
        cv2.putText(display_frame, f"FPS: {int(fps)}", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        cv2.imshow("Hand Tracking", display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
