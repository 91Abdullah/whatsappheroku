
from flask_cors import cross_origin
from heyoo import WhatsApp
# messenger = WhatsApp('EAAJVc3j40G8BAO30KsKwZBRDifNf7I9mxfyOIy7GISIEjoF7QZCBJfPexPHGL3eRoOUvLiWInTrmMh32ZBt2GE8IJqWjMZABNSZCf0TFR3y9BBNBH1y0x1rbLNLPHslznC9ZAyZChSWKJaPcUFuzQ2Mmvm3ZAdMOOd4CwIjFMfw7IdmSaQLb5qZAZBWTyfPWuzkbvSzGwKmsLYvgZDZD',  phone_number_id='110829038490956')
# messenger.send_message('Your message ', '923462901820')
import os
import json

from heyoo import WhatsApp
from os import environ
from flask import Flask, request, make_response, jsonify, redirect, url_for, flash, render_template
from os import environ
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy# from flask_sqlalchemy import SQLAlchemy
import logging

from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'static/images/'
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
from flask_cors import CORS, cross_origin
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://japiosmuawoeif:5fb7865a30ccd9848356a018582cee7186472ddafe35b23aa61cbe6fa969a357@ec2-54-86-106-48.compute-1.amazonaws.com:5432/d4e37uperu0jod'
db = SQLAlchemy(app)
messenger = WhatsApp(environ.get("TOKEN"), phone_number_id=environ.get("PHONE_NUMBER_ID"))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','wav','mpeg','mp3','mp4'])

app.secret_key = "super secret key"


@app.route('/')
def upload_form():
    return render_template('template.html')
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


VERIFY_TOKEN = 'umer' #application secret here


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@app.route("/webhook", methods=["GET", "POST"])
def hook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            logging.info("Verified webhook")
            response = make_response(request.args.get("hub.challenge"), 200)
            response.mimetype = "text/plain"
            return response
        logging.error("Webhook Verification failed")
        return "Invalid verification token"

    # Handle Webhook Subscriptions
    global data
    data = request.get_json()
    logging.info("Received webhook data: %s", data)
    # pet = Sender(sender_response=data)
    # db.session.add(pet)
    # db.session.commit()
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        print(new_message)
        if new_message:
            mobile = messenger.get_mobile(data)
            name = messenger.get_name(data)
            # pet = Sender(sender_name=name, sender_number=mobile)
            # db.session.add(pet)
            # db.session.commit()

            message_type = messenger.get_message_type(data)
            # logging.info(
            #     f"New Message; sender:{mobile} name:{name} type:{message_type}"
            # )
            if message_type == "text":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                message = messenger.get_message(data)
                # logging.info("Message: %s", message,'mobile',mobile,'name',name)
                # pet = Sender(sender_name=name, sender_number=mobile, sender_message_type=type,sender_message=message)

                # messenger.send_message(f"Hi {name}, nice to connect with you", mobile)

            elif message_type == "interactive":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                message_response = messenger.get_interactive_response(data)
                print('message_response',message_response)
                intractive_type = message_response.get("type")
                message_id = message_response[intractive_type]["id"]
                message_text = message_response[intractive_type]["title"]
                print('intractive_type',intractive_type,'message_id',message_id,'message_text',message_text)
                # logging.info(f"Interactive Message; {message_id}: {message_text}")

            elif message_type == "location":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                message_location = messenger.get_location(data)
                print('message_location',message_location)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                # pet = Sender(sender_name=name, sender_number=mobile, sender_message_type=type, sender_message=message)
                print('message_latitude',message_latitude,'message_longitude',message_longitude)
                # logging.info("Location: %s, %s", message_latitude, message_longitude)

            elif message_type == "image":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                image = messenger.get_image(data)
                print(image)
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = messenger.query_media_url(image_id)
                print(f"image_url {image_url}")
                # logging.info(f"{mobile} image_url {image_url}")
                image_filename = messenger.download_media(image_url, mime_type)
                print('image_filenamge',image_filename)
                # print(f"{mobile} sent image {image_filename}")
                # logging.info('image_filename',image_filename)


            elif message_type == "video":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                video = messenger.get_video(data)
                video_id, mime_type = video["id"], video["mime_type"]
                video_url = messenger.query_media_url(video_id)
                print(f"{mobile} video_url {video_url}")
                # logging.info(f"{mobile} video_url {video_url}")
                video_filename = messenger.download_media(video_url, mime_type)
                print('video_filename', video_filename)
                # print(f"{mobile} sent video {video_filename}")
                # logging.info('video_filename', video_filename)

            elif message_type == "audio":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                audio = messenger.get_audio(data)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = messenger.query_media_url(audio_id)
                print(f" audio_url {audio_url}")
                # logging.info(f"{mobile} audio_url {audio_url}")
                audio_filename = messenger.download_media(audio_url, mime_type)
                print('audio_filename', audio_filename)
                # print(f" sent audio {audio_filename}")
                # logging.info('audio_filename', audio_filename)

            elif message_type == "file":
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                file = messenger.get_file(data)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = messenger.query_media_url(file_id)
                print(f" file_url {file_url}")
                # logging.info(f"{mobile} file_url {file_url}")
                file_filename = messenger.download_media(file_url, mime_type)
                print('file_filename', file_filename)
                # print(f"{mobile} sent file {file_filename}")
                # logging.info('file_filename', file_filename)
            else:
                print(f"{mobile} sent {message_type} ")
                print(data)
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")
    return "ok"
class User(db.Model):
    __tablename__ = "users1"
    id = db.Column(db.Integer, primary_key=True)
    reciever_response = db.Column(db.JSON)

    def __init__(self, reciever_response):
        self.reciever_response = reciever_response

    def __repr__(self):
        return '<reciever_response %r>' % self.reciever_response

# Set "homepage" to index.html

@cross_origin()
@app.route('/prereg', methods=['POST'])
def prereg():
    hook()
    logging.info("Received webhook data: %s", data)
    print("my save data",data)
    pet_data = request.get_json()
    if request.method == 'POST':
        reciever_response = pet_data['reciever_response']
        reg = User(reciever_response=reciever_response)
        db.session.add(reg)
        db.session.commit()
        print('hello bhai')
        return jsonify({"success": True, "response": "sender response recieved"})

        # Check that email does not already exist (not a great query, but works)
@cross_origin()
@app.route('/getpets', methods = ['GET'])
def getpets():
     all_pets = []
     pets = User.query.all()
     for pet in pets:
          results = {
                    "pet_id":pet.id,
                    "reciever_response":pet.reciever_response,
        }
          all_pets.append(results)

     return jsonify(
            {
                "success": True,
                "pets": all_pets,
                "total_pets": len(pets),
            }
        )
@cross_origin()
@app.route('/message', methods=['POST'])
def create_pet():
    pet_data = request.json

    name = pet_data['name']
    print(name)
    messenger = WhatsApp(environ.get("TOKEN"),phone_number_id=environ.get("PHONE_NUMBER_ID"))  # this should be writen as

    # For sending  images
    # response = messenger.send_image(image=l,recipient_id="923462901820",)
    # response = messenger.send_audio(audio=l,recipient_id="923462901820")
    # response = messenger.send_video(video=l,recipient_id="923462901820",)
    # response = messenger.send_document(document=l, recipient_id="923462901820", )
    messenger.send_message(name, recipient_id="923462901820")


    return jsonify({"success": True, "response": "Pet addedh" })
@app.route('/sendimage', methods=['POST'])
def upload_image1():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # file.save(secure_filename(file.filename))
        # usersave = User( profile_pic=file.filename)
        # usersave.save()
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        o=url_for('static', filename='uploads/' + filename)
        l = 'https://whatsapptestflask.herokuapp.com'+url_for('static', filename='images/' + filename)
        messenger = WhatsApp(environ.get("TOKEN"), phone_number_id=environ.get("PHONE_NUMBER_ID")) #this should be writen as

        # For sending  images
        response = messenger.send_image(image=l,recipient_id="923462901820",)
        # response = messenger.send_audio(audio=l,recipient_id="923462901820")
        # response = messenger.send_video(video=l,recipient_id="923462901820",)
        # response = messenger.send_document(document=l,recipient_id="923462901820",)
        # For sending an Image
        # messenger.send_image(
        #         image="https://i.imgur.com/YSJayCb.jpeg",
        #         recipient_id="91989155xxxx",
        #     )
        print(response)
        print('url is',l)

        return redirect(url_for('static', filename='images/' + filename), code=301)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

    return jsonify({"success": True, "response": "Pet added"})
@app.route('/sendimage', methods=['POST'])
def upload_image2():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # file.save(secure_filename(file.filename))
        # usersave = User( profile_pic=file.filename)
        # usersave.save()
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        o=url_for('static', filename='uploads/' + filename)
        l = 'https://whatsapptestflask.herokuapp.com'+url_for('static', filename='images/' + filename)
        messenger = WhatsApp(environ.get("TOKEN"), phone_number_id=environ.get("PHONE_NUMBER_ID")) #this should be writen as

        # For sending  images
        response = messenger.send_image(image=l,recipient_id="923462901820",)
        # response = messenger.send_audio(audio=l,recipient_id="923462901820")
        # response = messenger.send_video(video=l,recipient_id="923462901820",)
        # response = messenger.send_document(document=l,recipient_id="923462901820",)
        # For sending an Image
        # messenger.send_image(
        #         image="https://i.imgur.com/YSJayCb.jpeg",
        #         recipient_id="91989155xxxx",
        #     )
        print(response)
        print('url is',l)

        return redirect(url_for('static', filename='images/' + filename), code=301)

    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

    return jsonify({"success": True, "response": "Pet added"})
@app.route('/senddoc', methods=['POST'])
def upload_image3():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # file.save(secure_filename(file.filename))
        # usersave = User( profile_pic=file.filename)
        # usersave.save()
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        o=url_for('static', filename='uploads/' + filename)
        l = 'https://whatsapptestflask.herokuapp.com'+url_for('static', filename='images/' + filename)
        messenger = WhatsApp(environ.get("TOKEN"), phone_number_id=environ.get("PHONE_NUMBER_ID")) #this should be writen as

        # For sending  images
        # response = messenger.send_image(image=l,recipient_id="923462901820",)
        # response = messenger.send_audio(audio=l,recipient_id="923462901820")
        # response = messenger.send_video(video=l,recipient_id="923462901820",)
        response = messenger.send_document(document=l,recipient_id="923462901820",)
        # For sending an Image
        # messenger.send_image(
        #         image="https://i.imgur.com/YSJayCb.jpeg",
        #         recipient_id="91989155xxxx",
        #     )
        print(response)
        print('url is',l)

        return redirect(url_for('static', filename='images/' + filename), code=301)

    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

    return jsonify({"success": True, "response": "Pet adddded"})
@app.route('/sendaudio', methods=['POST'])
def upload_image4():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # file.save(secure_filename(file.filename))
        # usersave = User( profile_pic=file.filename)
        # usersave.save()
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        o=url_for('static', filename='uploads/' + filename)
        l = 'https://whatsapptestflask.herokuapp.com'+url_for('static', filename='images/' + filename)
        messenger = WhatsApp(environ.get("TOKEN"), phone_number_id=environ.get("PHONE_NUMBER_ID")) #this should be writen as

        # For sending  images
        # response = messenger.send_image(image=l,recipient_id="923462901820",)
        response = messenger.send_audio(audio=l,recipient_id="923462901820")
        # response = messenger.send_video(video=l,recipient_id="923462901820",)
        # response = messenger.send_document(document=l,recipient_id="923462901820",)
        # For sending an Image
        # messenger.send_image(
        #         image="https://i.imgur.com/YSJayCb.jpeg",
        #         recipient_id="91989155xxxx",
        #     )
        print(response)
        print('url is',l)

        return redirect(url_for('static', filename='images/' + filename), code=301)

    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

    return jsonify({"success": True, "response": "Pet added"})
@app.route('/sendvideo', methods=['POST'])
def upload_image5():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # file.save(secure_filename(file.filename))
        # usersave = User( profile_pic=file.filename)
        # usersave.save()
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        o=url_for('static', filename='uploads/' + filename)
        l = 'https://whatsapptestflask.herokuapp.com'+url_for('static', filename='images/' + filename)
        messenger = WhatsApp(environ.get("TOKEN"), phone_number_id=environ.get("PHONE_NUMBER_ID")) #this should be writen as

        # For sending  images
        # response = messenger.send_image(image=l,recipient_id="923462901820",)
        # response = messenger.send_audio(audio=l,recipient_id="923462901820")
        response = messenger.send_video(video=l,recipient_id="923462901820",)
        # response = messenger.send_document(document=l,recipient_id="923462901820",)
        # For sending an Image
        # messenger.send_image(
        #         image="https://i.imgur.com/YSJayCb.jpeg",
        #         recipient_id="91989155xxxx",
        #     )
        print(response)
        print('url is',l)


        return redirect(url_for('static', filename='images/' + filename), code=301)

    else:
        flash('Allowed image  ggg types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

    return jsonify({"success": True, "response": "Pet added"})
if __name__ == "__main__":
    app.run(port=4000, debug=True)
