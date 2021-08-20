from flask import Flask, render_template, Response, request
import video_detection
import time
import os
from pytube import YouTube

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/answer", methods=["POST", "GET"])
def answer():
    if request.method == "POST":
        video_url = request.form.get("user_url")
        global user_video, detect
        user_video = YouTube(video_url)
        os.chdir("../deneme-z/videos")
        user_video.streams.filter(
            progressive=True, file_extension='mp4', res="360p").first().download()
        detect = video_detection.Detection(user_video.title+"mp4")
        return render_template("answer.html", answer=user_video.title)

    else:
        return render_template("answer.html")


time.sleep(4)


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
