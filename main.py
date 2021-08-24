from flask import Flask, render_template, Response, request
import video_detection
from pytube import YouTube
import os

app = Flask(__name__)


# homepage
@app.route("/")
def index():
    return render_template("index.html")


# get user input and install related video
@app.route("/video", methods=["GET", "POST"])
def video():
    global video
    if request.method == "POST":
        video_url = request.form.get("user_url")
        video = YouTube(video_url)
        os.remove("/home/robot/projects/yolo_video_detection/videos/test.mp4")
        os.chdir("../yolo_video_detection/videos")
        video.streams.filter(
            progressive=True, file_extension='mp4', res="360p").first().download()
        os.chdir("/home/robot/projects/yolo_video_detection/videos/")
        for file in os.listdir("/home/robot/projects/yolo_video_detection/videos/"):
            old_name = file
            new_name = "test.mp4"
        os.rename(old_name, new_name)
        return render_template("video.html", answer=video.title)
    else:
        return render_template("video.html")


# detected video response function
@app.route("/detected")
def detected():
    detect = video_detection.Detection("test.mp4")
    return Response(detect.tiny_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
