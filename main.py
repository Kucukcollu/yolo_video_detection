from flask import Flask, render_template, Response, request
import video_detection
import time
from pytube import YouTube
import os

app = Flask(__name__)


# homepage
@app.route("/")
def index():
    return render_template("index.html")


# original video should be here
@app.route("/video", methods=["GET", "POST"])
def video():
    global video
    if request.method == "POST":
        video_url = request.form.get("user_url")
        video = YouTube(video_url)
        os.chdir("../yolo_video_detection/videos")
        video.streams.filter(
            progressive=True, file_extension='mp4', res="360p").first().download()
#        time.sleep(8)
        return render_template("video.html", answer=video.title)
    else:
        return render_template("video.html")


"""
# open video in here
@app.route("/open")
def open():
    detect = video_detection.Detection(video.title+".mp4")
    return Response(detect.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
"""


# detected video should be here
@app.route("/detected")
def detected():
    detect = video_detection.Detection(video.title+".mp4")
#    time.sleep(8)
    return Response(detect.tiny_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
