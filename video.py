import cv2
import numpy as np
from typing import Union, Optional

class VideoStreamer:
    
    def __init__(self,
                 video: Union[str,int],
                 stream_ext: str = 'jpg'):
        """CONSTRUCTOR

        Args:
            video (str): _description_
        """
        self.video = cv2.VideoCapture(video)
        self.stream_ext = stream_ext
        assert stream_ext in ('jpg','png'), f"extension {stream_ext} \
            is not supported"
    
    async def read(self) -> Optional[bytes]:
        """reading video

        Returns:
            bytes: byte stream
        """
        ret,frame = self.video.read()
        
        if not ret:
            return None
        
        return np.array(cv2.imencode(f'.{self.stream_ext}',frame)[1]).tobytes()

    async def release(self) -> None:
        """release
        """
        self.video.release() 
