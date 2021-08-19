from flask import Flask, render_template, Response
import video_detection

app = Flask(__name__)

detect = video_detection.Detection("test2.mp4")


@app.route("/")
def homepage():
    return render_template("index.html")


"""
@app.route("/original_video")
def original_video():
    return Response(detect.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
"""


@app.route("/detected_video")
def detected_video():
    return Response(detect.tiny_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run()
