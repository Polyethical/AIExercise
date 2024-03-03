import random

import cv2
import mediapipe as mp
import time

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

accuracy = 0
cap = cv2.VideoCapture(0)

start_time = time.time()
elapsed_time = 0
exercise_count = 0
correct_exercise_count = 0
total_points = 0
exercise = ["situps", "pullups", "jumping jacks"]
new_exercise = "situps"
while cap.isOpened()==True:
    ret, frame = cap.read()
    if not ret:
        break

    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Extract detected landmarks from the results
    if results.pose_landmarks:
        left_shoulder = results.pose_landmarks.landmark[11]
        right_shoulder = results.pose_landmarks.landmark[12]

        sit_up_condition = left_shoulder.y > right_shoulder.y
        pull_up_condition = left_shoulder.y < right_shoulder.y  # Placeholder, customize based on squat pose
        jumping_jack_condition = left_shoulder.y < right_shoulder.y

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        elapsed_time = time.time() - start_time
        cv2.putText(frame, f"Elapsed Time: {time.time() - start_time:.2f} seconds", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 156, 168), 2, cv2.LINE_AA)

        cv2.putText(frame,
                    f"Current exercise: {new_exercise}",
                    (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (168, 50, 152), 2, cv2.LINE_AA)

        cv2.putText(frame,
                    f"Exercise count {exercise_count}",
                    (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (168, 130, 152), 2, cv2.LINE_AA)

        cv2.putText(frame,
                    f""
                    f"Points: {accuracy}",
                    (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (70, 50, 168), 2, cv2.LINE_AA)

        if new_exercise == "situps":
            if sit_up_condition:
                correct_exercise_count += 1
                cv2.putText(frame, "Sit-up Correct", (10, 180),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, "Sit-up Incorrect", (10, 210),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        if new_exercise == "pullups":
            if pull_up_condition:
                correct_exercise_count += 1
                cv2.putText(frame, "pull up is correct", (10, 180),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, "pull up is incorrect", (10, 210),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        if new_exercise == "jumping jacks":
            if jumping_jack_condition:
                correct_exercise_count += 1
                cv2.putText(frame, "jumping jack is correct", (10, 180),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, "jumping jack is incorrect", (10, 210),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow("AIExercise", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if elapsed_time >= 20:
        exercise_count += 10
        new_exercise = exercise[random.randint(0, 2)]
        total_points += correct_exercise_count / exercise_count * 100
        accuracy = correct_exercise_count / exercise_count * 100
        start_time = time.time()
        print(f"Exercise {exercise_count} - Accuracy: {correct_exercise_count / exercise_count * 100:.2f}%")


cap.release()
cv2.destroyAllWindows()




