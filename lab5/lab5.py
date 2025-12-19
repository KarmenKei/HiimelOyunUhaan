from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")


cap = cv2.VideoCapture("cars.mp4")


counted_ids = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break


    results = model.track(frame, persist=True)


    if results[0].boxes is not None:
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            class_name = results[0].names[class_id]

            track_id = int(box.id[0]) if box.id is not None else None

            if class_name == "car" and track_id is not None:
                if track_id not in counted_ids:
                    counted_ids.add(track_id)


    annotated = results[0].plot()
    cv2.imshow("Car Tracking", annotated)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

print(" CARS COUNTED:", len(counted_ids))