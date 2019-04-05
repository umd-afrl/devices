from flask import Flask, Response
import cv2

vc = cv2.VideoCapture(0)

app = Flask(__name__)

@app.route('/snakecam')
def get_snakecam():
	return Response(snakecam_fram_gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def snakecam_frame_gen():
	while True:
		rval, frame = vc.read()
		cv2.imwrite('snakecam.jpg', frame)
		yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + open('snakecam.jpg', 'rb').read() + b'\r\n')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, threaded=True)
