import cv2
import os
def capture_photo():
    cap = cv2.VideoCapture(0)
    while (1):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        cv2.imshow("capture", frame)
        file_count = 0
        for dirpath, dirnames, filenames in os.walk('app/static/photo/capture_photo'):
            for file in filenames:
                file_count = file_count + 1
        file_name = "capture_photo{}.jpg".format(str(file_count))
        file_name = "app/static/photo/capture_photo/{}".format(file_name)
        if cv2.waitKey(1) & 0xFF == ord('Q'):
            cv2.imwrite(file_name, frame)
            break
    cap.release()
    cv2.destroyAllWindows()
    return file_name