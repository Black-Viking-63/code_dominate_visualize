import face_recognition
import cv2
#print(cv2.__version__)
import time
from DBConnector import DBConnector

class FaceRecognizer:
    def __init__(self, db_connector):
        # load white list
        white_list = db_connector.get_whitelist()
        self.wl_ids = [p[0].person_id for p in white_list]
        self.names = [p[0].person_name for p in white_list]
        self.photos = [p[0].person_photo_link for p in white_list]
        self.Encodings = []
        # generate face encodings
        for photo in self.photos:
            if photo is not None:
                face = face_recognition.load_image_file(photo)
                encoding = face_recognition.face_encodings(face)[0]
                self.Encodings.append(encoding)

        print("names= ", self.names)
        print("photos= ", self.photos)
        # igorFace = face_recognition.load_image_file(
        #     '/home/julianir/Julia/NIR/white_list/Kilbas_Igor_Alexandrovich_2.png')
        # igorEncode = face_recognition.face_encodings(igorFace)[0]
        # self.Encodings.append(igorEncode)
        #self.Encodings = [juliaEncode, igorEncode]
        #self.Names = ['Julia', 'Igor']


    def __select_roi(self, image, box):
        (x,y,w,h) = box
        image_roi = image[y:y+h, x:x+w]
        return image_roi

    #@yappi.profile(clock_type='wall', profile_builtins=False)
    def recognize(self, image, box):
        image = self.__select_roi(image, box)
        facePositions = face_recognition.face_locations(image)

        # we compare known encodings from above with these unknown test encodings
        # we look at each box from positions and get its encoding from testImage
        allEncodings = face_recognition.face_encodings(image, facePositions)

        # convert this to something cv2 will like
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        visitor_name = 'Unknown'
        visitor_id = 0
        for (top, right, bottom, left), face_encoding in zip(facePositions, allEncodings):
            matches = face_recognition.compare_faces(self.Encodings, face_encoding)
            # if anywhere in matches there is a true
            if True in matches:
                first_match_index = matches.index(True)
                visitor_name = self.names[first_match_index]
                visitor_id = self.wl_ids[first_match_index]
                
        #back to original color space
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return visitor_name, visitor_id