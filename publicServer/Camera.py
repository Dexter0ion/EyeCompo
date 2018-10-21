class Camera():
    
    @staticmethod
    def get_frame():
        frames = [open('loaded.jpg', 'rb').read()]
        #print(frames[0])
        return frames[0]