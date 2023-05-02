import yappi
# Время выводится в секундах. Измеряем wall time, а не cpu time, так как в программе используются функции библиотеки dlib, которые выполняются на gpu.
yappi.set_clock_type("wall")
# Запускает профилирование всех потоков в текущем экземпляре интерпретатора.
yappi.start(builtins=False)

# код программы
db_connector = DBConnector()
db_connector.connect_to_postgresql()
print("[INFO] loading CNN face detector...")
detector = FaceDetector()
recognizer = FaceRecognizer(db_connector)
print('done')
door_controller = DoorController()

cam = cv2.VideoCapture(path)
DOOR_IS_OPEN = False

for counter in range(10):
    ret, image = cam.read()
    if not DOOR_IS_OPEN:
        boxes = detector.detect(image)
        if boxes:
            visitor_name, visitor_id = recognizer.recognize(image, boxes[0])
            print("Name: ", visitor_name)
            if visitor_name != 'Unknown':
                DOOR_IS_OPEN = True
        
        # loop over the bounding boxes
        for (x, y, w, h) in boxes:
            # draw the bounding box on our image
            sp = 50
            cv2.rectangle(image, (x-sp, y-sp), (x + w +sp, y + h +sp), (0, 255, 0), 2)

    cv2.imshow('Cam', image)
    cv2.moveWindow('Cam', 0, 0)

db_connector.disconnect_from_db()
cam.release()
cv2.destroyAllWindows()
# Останавливает профилирование. Его можно продолжить, снова вызвав start().
yappi.stop()
ypstats = yappi.get_func_stats()
ypstats.sort(sort_type='ttot', sort_order="desc")
ver = 'test'
# Сохранение результата профилирования в файл
# Текущий внутренний формат yappi 
ypstats.save(f"stats_{ver}.ys")
# Формат для подачи в gprof2dot
ypstats.save(f"stats_{ver}.stats", type="pstat")
