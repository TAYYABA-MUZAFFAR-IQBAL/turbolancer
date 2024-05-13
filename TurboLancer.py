import random
from flask import Flask, request, render_template, redirect, url_for, jsonify, send_file, send_from_directory, render_template_string, abort
from flask_wtf import FlaskForm
from wtforms import FileField
from pymongo import MongoClient
from bson.objectid import ObjectId
import os, re, io
import uuid
import json
import datetime
import turbolancer_data_Security
from jinja2 import Environment, FileSystemLoader
from flask_socketio import SocketIO, emit, join_room
import TurboLancer_RePhrase_text
from werkzeug.datastructures import ImmutableMultiDict
from urllib.parse import unquote

app = Flask(__name__, template_folder='template', static_folder='static')
env = Environment(loader=FileSystemLoader('template'))

app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

# Connect to MongoDB
client = MongoClient(
    "mongodb+srv://junaidiqbal:allahsadaro@junaid.lkpmjko.mongodb.net/?retryWrites=true&w=majority")
db = client["Tasker"]
key = b'||/:?"(:@junaid)'
# Set collection names
seller_collection = db['developers']
user_collection = db['users']
serving_sectors_collection = db['serving_sectors']
sectors_technologies_collection = db['technologies']
chat_rooms = db['chatrooms']
question_collection = db['questions']
image_collection = db['images']


def generate_id():
    return str(uuid.uuid4())


def getkey(data):
    keys_to_find = ['ideo', 'emalo', 'deno']

    found_items = {key: data.get(key) for key in keys_to_find if key in data}
    # (found_items)
    return found_items


def check(data, file):
    compound = getkey(data)
    if compound:
        if compound.get('ideo', None):
            id_ = turbolancer_data_Security.decrypt(
                key, compound.get('ideo', None))
        # (id_)
            ud = seller_collection.find_one({"_id": id_}) or user_collection.find_one({"_id": id_})

            if ud:
                if compound.get('emalo') == ud['email'] and ud['d'] == 'd' and not compound.get('deno'):
                    return None
                elif compound.get('emalo') == ud['email'] and ud['d'] == 'd' and compound.get('deno'):
                    return file
                elif compound.get('emalo') == ud['email'] and ud['d'] == 'c':
                    return file
            else:
                return None
        else:
            return None
    else:
        return None


# Form for uploading images
class ImageUploadForm(FlaskForm):
    image = FileField('Image')


@app.route('/')
def main():
    cookies = getkey(request.cookies)
    if cookies.get('ideo'):
        id_ = turbolancer_data_Security.decrypt(key, cookies.get('ideo'))
        # ("\n" +id_)
        ud:str = seller_collection.find_one(
            {"_id": id_}) or user_collection.find_one({"_id": id_})
        if cookies.get('emalo') == ud['email'] and ud['d'] == 'd' and not cookies.get('deno'):
            return redirect(f'/addinfo/{id_}/{ud["name"]}/{ud["email"]}')
        elif cookies.get('emalo') == ud['email'] and ud['d'] == 'd' and cookies.get('deno'):
            return redirect(f'/home-c/{id_}/{ud["d"]}')
        elif cookies.get('emalo') == ud['email'] and ud['d'] == 'c':
            return redirect(f'/home-c/{id_}/{ud["d"]}')

    return render_template('index.html')


@app.route("/start_selling_now", methods=["GET", "POST"])
def signup():
    if check(request.cookies, 'file') is not None:
        return redirect(url_for('main'))
    if (not check(request.cookies, 'file')) and (request.method == "POST"):
        name = request.form["name"]
        encoded_email = turbolancer_data_Security.encrypt(
            key, request.form["email"])
        encoded_password = turbolancer_data_Security.encrypt(
            key, request.form["ps"])
        encoded_phone = turbolancer_data_Security.encrypt(
            key, request.form['ph'])
        encoded_bir = turbolancer_data_Security.encrypt(
            key, request.form.get("bir"))
        encoded_gan = turbolancer_data_Security.encrypt(
            key, request.form.get("gan"))

        encoded_country = turbolancer_data_Security.encrypt(
            key, request.form['con'])
        d = 'd'

        # Check if the developer already exists in the database
        # (encoded_email)
        user = seller_collection.find_one({"email": encoded_email}) or user_collection.find_one(
            {"email": encoded_email}) or seller_collection.find_one({"ph": encoded_phone}) or user_collection.find_one({"ph": encoded_phone})
        user_ph = seller_collection.find_one({"ph": encoded_phone}) or user_collection.find_one(
            {"ph": encoded_phone}) or seller_collection.find_one({"ph": encoded_phone}) or user_collection.find_one({"ph": encoded_phone})
        user_id = generate_id()

        if user or user_ph:

            return render_template("signup-c.html",  x='Account already exists with this email/phone.', y='onload= this.click')
        else:
            t = name.replace(' ', '')
            tag:str = '@' + t
            user_id = generate_id()
            count = seller_collection.count_documents({"name": name})
            count_s = user_collection.count_documents({"name": name})

            count = str((int(count + count_s) + 1) * 1000)[::-1]

            year = datetime.date.today().year
            count = str(count)
            if count:
                count += str(random.randint(0, 9))
            user = {
                "_id":  user_id,
                "image": '',
                "name": name,
                "tag": tag + count,
                "email": encoded_email,
                "password": encoded_password,
                "country": encoded_country,
                "phone_number": encoded_phone,
                "about_self": '',
                "d": d,
                "sk": [],
                "grade": "C",
                "earnings": 0,
                "rating": 0,
                "english": '',
                "payment_method": "Visa",
                "project_history": [],
                "chat_rooms": [],
                "account_created_in": year,
                'bir': encoded_bir,
                'gan': encoded_gan
            }

            seller_collection.insert_one(user)
            ide = user_id
            user_id = turbolancer_data_Security.encrypt(key, user_id)
        return render_template('save_cook.html', keys=[['ideo', 'emalo', 'tp'], [user_id, encoded_email, 'd']], redi=f'addinfo/{ide}/{name}/{encoded_email}')

    return render_template("signup-c.html")


@app.route('/addinfo/<x>/<y>/<z>')
def addinfo(x, y, z):
    cookies = getkey(request.cookies)
    if cookies:
        print(cookies.get('emalo'))
        if cookies.get('emalo') in z:
            return render_template('dataform.html', id=x, name=y, email=z, emaloz=turbolancer_data_Security.decrypt(key, cookies.get('emalo')))
        else:
            return redirect(url_for('main'))
    else:
        return redirect(url_for('main'))


@app.route("/begin_client_journey", methods=['GET', 'POST'])
def signup_and_upload_image():
    if check(request.cookies, 'file') is not None:
        return redirect(url_for('main'))
    if (not check(request.cookies, 'file')) and (request.method == "POST"):
        name = request.form.get("name")
        encoded_email = turbolancer_data_Security.encrypt(
            key, request.form["email"])
        encoded_password = turbolancer_data_Security.encrypt(
            key, request.form["ps"])
        encoded_phone = turbolancer_data_Security.encrypt(
            key, request.form['ph'])

        encoded_country = turbolancer_data_Security.encrypt(
            key, request.form['con'])
        d = 'c'
        encoded_bir = turbolancer_data_Security.encrypt(
            key, request.form.get("bir"))
        encoded_gan = turbolancer_data_Security.encrypt(
            key, request.form.get("gan"))
        # Check if the developer already exists in the database
        # (encoded_email)
        user = seller_collection.find_one({"email": encoded_email}) or user_collection.find_one(
            {"email": encoded_email}) or seller_collection.find_one({"ph": encoded_phone}) or user_collection.find_one({"ph": encoded_phone})
        user_ph = seller_collection.find_one({"ph": encoded_phone}) or user_collection.find_one(
            {"ph": encoded_phone}) or seller_collection.find_one({"ph": encoded_phone}) or user_collection.find_one({"ph": encoded_phone})
        user_id = generate_id()

        if 'image' not in request.files:
            return render_template("error.html", message="No image uploaded")
        else:
            image = request.files["image"]
            print(image)
            image_data = image.read()
            image_id = image_collection.insert_one(
                {"data": image_data}).inserted_id

        if user or user_ph:
            return render_template("sin-c.html", x='Account already exists with this email/phone.', y='onload= this.click')

        elif user is None and user_ph is None:
            t = name.replace(' ', '')
            tag = '@' + t
            user_id = generate_id()
            count = seller_collection.count_documents({"name": name})
            count_s = user_collection.count_documents({"name": name})

            count = str((int(count + count_s) + 1) * 1000)[::-1]

            year = datetime.date.today().year
            count = str(count)
            if count:
                count += str(random.randint(0, 9))
            user = {
                "_id": user_id,
                "image": "/get_image/" + str(image_id),
                "name": name,
                "tag": tag + count,
                "email": encoded_email,
                "password": encoded_password,
                "country": encoded_country,
                "phone_number": encoded_phone,
                "d": d,
                "spending": 0,
                "account_created_in": year,
                "payment_method": "Visa",
                "orders_history": [],
                'bir': encoded_bir,
                'gan': encoded_gan
            }

            user_collection.insert_one(user)
            ide = user_id
            print(f'/redi/{user_id}/{encoded_email}/{ide}/{user["d"]}')
            user_id = turbolancer_data_Security.encrypt(key, user_id)
            return jsonify({"success": True, "redirect_url": f'/redi/{user_id}/{encoded_email}/{ide}/{user["d"]}'})
        return render_template("sin-c.html")

    return render_template("sin-c.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if check(request.cookies, 'file') is not None:
        return redirect(url_for('main'))
    if (not check(request.cookies, 'file')) and (request.method == "POST"):

        encoded_email = turbolancer_data_Security.encrypt(
            key, request.form["email"])
        encoded_password = turbolancer_data_Security.encrypt(
            key, request.form["ps"])

        user = seller_collection.find_one(
            {"email": encoded_email}) or user_collection.find_one({"email": encoded_email})

        if user:
            # (user['email'] +" heelo")
            stored_password = user['password']
            if stored_password != encoded_password:
                return jsonify({"error": "Incorrect password!"})
            else:
                ide = user['_id']
                user_id = turbolancer_data_Security.encrypt(key, ide)
                print(user['d'] == 'd' and (user['image']
                      == "" or user['about_self'] == ""))

                if user['d'] == 'd' and (user['image'] == "" or user['about_self'] == ""):
                    return jsonify({"success": True, "redirect_url": f'redi/{user_id}/{encoded_email}/{ide}/{user["d"]}/none'})

                return jsonify({"success": True, "redirect_url": f'redi/{user_id}/{encoded_email}/{ide}/{user["d"]}/_[__xxx__%12*79)(56)[:]-++784kdd]_'})

        else:
            return jsonify({"error": "Account does not exist!"})

    return render_template("singin.html")


@app.route('/redi/<user_id>/<encoded_email>/<ide>/<user_d>/<deno>')
def redi(user_id, encoded_email, ide, user_d, deno):
    expected_deno = '_[__xxx__%12*79)(56)[:]-++784kdd]_'
    print(unquote(expected_deno) == deno)
    if unquote(expected_deno) == deno:
        return render_template('save_cook.html', keys=[['ideo', 'emalo', 'tp', 'deno'], [user_id, encoded_email, user_d, deno]], redi=f'/home-c/{ide}/{user_d}')

    return render_template('save_cook.html', keys=[['ideo', 'emalo', 'tp'], [user_id, encoded_email, user_d]], redi=f'/home-c/{ide}/{user_d}')


@app.route('/UPLOAD_IMAGE', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        # Obtain the uploaded image and the email from the request payload
        image = request.files['image']
        encoded_email = request.form.get('email')
        # (encoded_email)

        # Retrieve the developer document
        developer = seller_collection.find_one({"email": encoded_email})

        if developer and 'image' in developer:
            # Get the previous image ID
            previous_image_link = developer['image']
            if previous_image_link != '':
                previous_image_id = previous_image_link.split('/')[-1]

                # Delete the previous image from the image collection
                image_collection.delete_one(
                    {'_id': ObjectId(previous_image_id)})

        # Save the uploaded image to the database
        image_data = image.read()
        image_id = image_collection.insert_one(
            {'data': image_data}).inserted_id

        # Update the developer document with the associated image ID
        seller_collection.update_one({"email": encoded_email}, {
                                        "$set": {"image": '/get_image/' + str(image_id)}})

        return jsonify({'image_id': str(image_id)})
    else:
        return jsonify({'error': 'No image file found'})


def upload_image_local(image_data, encoded_email, ideo):
    collection = seller_collection.find_one({'_id': ideo, "email": encoded_email}) or user_collection.find_one({'_id': ideo, "email": encoded_email})
    if 'image' in collection:
        previous_image_link = collection['image']
        if previous_image_link != '':
            previous_image_id = previous_image_link.split('/')[-1]
            image_collection.delete_one({'_id': ObjectId(previous_image_id)})
    image_id = image_collection.insert_one({'data': image_data}).inserted_id

    # Update the 'image' field in the appropriate collection
    if seller_collection.find_one({'_id': ideo, "email": encoded_email}):
        seller_collection.update_one({"_id": ideo, "email": encoded_email}, {"$set": {"image": '/get_image/' + str(image_id)}})
    else:
        user_collection.update_one({"_id": ideo, "email": encoded_email}, {"$set": {"image": '/get_image/' + str(image_id)}})

    return jsonify({'image_id': str(image_id)})
    
# @app.route('/send_IMAGE', methods=['POST'])
# def send_image():
#     if 'image' in request.files:
#         # Obtain the uploaded image and the email from the request payload
#         image = request.files['image']
#         chatroom_Id = request.form.get('chatroom')
#         # (chatroom_Id)

#         # Retrieve the developer document
#         chatroom = chat_rooms.find_one({"_id": ObjectId(chatroom_Id)})

#         # Save the uploaded image to the database
#         image_data = image.read()
#         image_id = image_collection.insert_one(
#             {'data': image_data}).inserted_id

#         return jsonify({'image_id': '/turbolancer/gett_image/chats/turbolancer_qazwsxedcrfvqwerty/'+str(image_id)})
#     else:
#         return jsonify({'error': 'No image file found'})


@app.route('/get_image/<image_id>', methods=['GET'])
def get_image(image_id):
    # Retrieve the image from the database
    image_data = image_collection.find_one({'_id': ObjectId(image_id)})

    if image_data and 'data' in image_data:
        # Serve the image data with appropriate content type
        return send_file(io.BytesIO(image_data['data']), mimetype='image/jpeg')
    else:
        return jsonify({'error': 'Image not found'})

    ##############################################################################################


# @app.route('/turbolancer/gett_image/chats/turbolancer_qazwsxedcrfvqwerty/<image_id>', methods=['GET'])
# def mess(image_id):
#     # Retrieve the image from the database
#     image_data = image_collection.find_one({'_id': ObjectId(image_id)})

#     if image_data and 'data' in image_data:
#         # Serve the image data with appropriate content type
#         return send_file(io.BytesIO(image_data['data']), mimetype='image/jpeg')
#     else:
#         return jsonify({'error': 'Image not found'})


@app.route('/update_data', methods=['POST'])
def update_data():
    data = request.get_json()
    encoded_email = data.get('email')
    # (encoded_email)

    text_area_value = data.get('textAreaValue')

    if encoded_email and text_area_value:
        developer = seller_collection.find_one({"email": encoded_email})

        if developer:
            seller_collection.update_one({"email": encoded_email}, {
                                            "$set": {"about_self": text_area_value}})
            print(f"home-c/{developer['_id']}/d")
            return jsonify({'message': '_{__xxx__%12*79)(56)[:]-++784kdd}_', 'ne': 'deno', 're': f"/home-c/{developer['_id']}/d"})
        else:
            return jsonify({'error': 'seller not found.'})
    else:
        return jsonify({'error': 'Invalid data.'})


# @app.route('/update_result', methods=['POST'])
# def update_result():
#     data = request.get_json()
#     encoded_email = data.get('email')
#     # (encoded_email)

#     text_area_value = data.get('result')

#     if encoded_email and text_area_value:
#         developer = seller_collection.find_one({"email": encoded_email})
#         skill = seller_collection.find_one({"sk": encoded_email})

#         if developer:
#             seller_collection.update_one({"email": encoded_email}, {
#                                             "$set": {"about_self": text_area_value}})
#             return jsonify({'message': 'Data updated successfully.'})
#         else:
#             return jsonify({'error': 'Developer not found.'})
#     else:
#         return jsonify({'error': 'Invalid data.'})


# @app.route('/Dashbord/<x>/<y>')
# def Dashbord(x, y):
#     try:
#         if y != 'd':
#             return jsonify({'error': 'Invalid value for "y"'}), 400

#         user_data = seller_collection.find_one({"_id": x})
#         email = turbolancer_data_Security.decrypt(key, user_data["email"])
#         image = user_data["image"]
#         name = user_data["name"]
#         tag = user_data["tag"]
#         country = turbolancer_data_Security.decrypt(key, user_data["country"])
#         ph = turbolancer_data_Security.decrypt(key, user_data["phone_number"])
#         about = user_data['about_self']
#         grade = user_data['grade']
#         earnings = user_data['earnings']
#         ratting = user_data['rating']
#         en = user_data['english']
#         year = user_data['account_created_in']
#         method = user_data["payment_method"]
#         user_id = x
#         account = y

#         # Call your get_user_data function here
#         user_data = get_user_dataA(user_id, account)
#         chat_rooms_list = user_data.get("chat_rooms", [])

#         namesli = []
#         img_s = []
#         chids = []
#         last_message = []

#         for names in chat_rooms_list:
#             user_users = user_collection.find({"chat_rooms": {"$in": [names]}})

#             developer_users = seller_collection.find(
#                 {"chat_rooms": {"$in": [names]}})

#             chat_room_data = chat_rooms.find_one({"chat_room_name": names})
#             if chat_room_data is None:
#                 new_chat_room_id = ObjectId()
#                 new_chat_room_name = str(new_chat_room_id)
#                 chat_rooms.insert_one(
#                     {"_id": new_chat_room_id, "chat_room_name": new_chat_room_name})
#                 chat_room_data = {"_id": new_chat_room_id,
#                                   "chat_room_name": new_chat_room_name}

#             other_users = list(user_users) + list(developer_users)

#             for user in other_users:
#                 name = user.get('name')
#                 img = user.get('image')
#                 # (img)
#                 id = user.get('_id')
#                 chid = chat_room_data.get('_id')
#                 chid = str(chid)

#                 if str(id) != user_id:
#                     namesli.append(name)
#                     img_s.append(img)
#                     chids.append(chid)
#         zipped_data = zip(namesli, img_s)

#         return render_template('home.html', email=email,
#                                image=image,
#                                name=name,
#                                tag=tag,
#                                cont=country,
#                                ph=ph,
#                                abs=about,
#                                grade=grade,
#                                ern=earnings,
#                                ratting=ratting,
#                                el=en,
#                                check=user_data['email'],
#                                year=year,
#                                method=method,
#                                zipped_data=zipped_data)

#     except Exception as e:
#         # ("An error occurred:", str(e))
#         return jsonify({'error': 'An error occurred'}), 500


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Sorry! Resource not found'}), 404


# @app.route('/chat')
# def index():
#     cookies = getkey(request.cookies)
#     if cookies.get('ideo'):
#         id_ = turbolancer_data_Security.decrypt(key, cookies.get('ideo'))
#         print (id_)
#         return render_template('try.html', _id = id_)
#     return render_template('try.html', id_ = '')


# def get_user_data(user_id, Atype):
#     print('id ' + user_id)
#     if 'd' in Atype:
#         user_data = seller_collection.find_one({"_id": user_id})
#         print(user_data)
#     elif 'c' in Atype:
#         user_data = user_collection.find_one({'_id': user_id})
#         print(user_data)
#     return user_data


# @socketio.on('join')
# def handle_join(data):
#     user_id = data['userId']
#     account = data['account']
#     print(user_id )
#     print('this is from user id')

#     # Retrieve the user's chat room list from the user collection
#     user_data = get_user_data(user_id,account)
#     print( user_data)
#     if user_data is None:
#         emit('join_response', {"status": "USER_NOT_FOUND"})
#         return

#     chat_rooms_list = user_data.get("chat_rooms", [])
#     # (chat_rooms_list)

#     namesli = []
#     img_s = []
#     chids = []
#     last_message = []

#     for names in chat_rooms_list:
#         # Search for users in the 'user_collection'
#         user_users = user_collection.find({"chat_rooms": {"$in": [names]}})

#         # Search for users in the 'seller_collection'
#         developer_users = seller_collection.find(
#             {"chat_rooms": {"$in": [names]}})

#         # Find or create the chat room
#         chat_room_data = chat_rooms.find_one({"chat_room_name": names})
#         if chat_room_data is None:
#             new_chat_room_id = ObjectId()
#             new_chat_room_name = str(new_chat_room_id)
#             chat_rooms.insert_one(
#                 {"_id": new_chat_room_id, "chat_room_name": new_chat_room_name})
#             chat_room_data = {"_id": new_chat_room_id,
#                               "chat_room_name": new_chat_room_name}

#         # Combine results from both collections
#         other_users = list(user_users) + list(developer_users)

#         for user in other_users:
#             name = user.get('name')
#             img = user.get('image')
#             id = user.get('_id')
#             chid = chat_room_data.get('_id')
#             chid = str(chid)

#             # Compare ObjectId to user_id
#             if str(id) != user_id:
#                 namesli.append(name)
#                 img_s.append(img)
#                 chids.append(chid)

#     emit('join_response', {'status': 'OK',
#          "name": namesli, "imgs": img_s, 'chid': chids, 'last_message': last_message})


# @socketio.on('sendMessage')
# def handle_send_message(data):
#     user_id = data['userId']
#     current_time = data['currentTime']
#     chat_room_name = data['chatRoomName']
#     message = data.get('message')
#     # (message)
#     image_link = data.get('imageLink')
#     diff = data.get('diff')

#     if image_link:
#         chat_rooms.update_one(
#             {"_id": ObjectId(chat_room_name)},
#             {"$push": {"messages": {'message': image_link,
#                                     'timestamp': current_time, 'sender': user_id, 'diff': diff}}},
#             upsert=True
#         )
#         emit('newMessage', {'message': image_link, 'timestamp': current_time, 'sender': user_id, 'ch': chat_room_name, 'diff': diff},
#              broadcast=True, include_self=True)

#     else:
#         chat_rooms.update_one(
#             {"_id": ObjectId(chat_room_name)},
#             {"$push": {"messages": {'message': message,
#                                     'timestamp': current_time, 'sender': user_id, 'diff': diff}}},
#             upsert=True
#         )
#         emit('newMessage', {'message': message, 'timestamp': current_time, 'sender': user_id, 'ch': chat_room_name, 'diff': diff},
#              broadcast=True, include_self=True)


# @socketio.on('delete_message')
# def delmessage(data):
#     sender = data.get('sender')
#     time = data.get('time')
#     message = data.get('message')
#     index = data.get('index')
#     chatroomname = data.get('chatroomname')
#     new_blocked_by = sender

#     # Find the chat room by its _id and the specific message by time
#     chat_room = chat_rooms.find_one({"_id": ObjectId(chatroomname)})

#     if chat_room:
#         messages = chat_room.get('messages', [])
#         x = 0
#         for message in messages:
#             # (message.get('timestamp'))
#             # (time)
#             if message.get('timestamp') == time and x == index:
#                 # Add new_blocked_by to the 'blocked_by' list in the specific message
#                 message.setdefault('blocked_by', []).append(new_blocked_by)
#                 # (message)
#                 # Update the chat room with the modified messages list
#                 chat_rooms.update_one(
#                     {"_id": ObjectId(chatroomname)},
#                     {"$set": {"messages": messages}}, upsert=True
#                 )
#                 # (chat_room.get('chat_room_name'))
#                 # Broadcast the message_deleted event to all clients in the chat room
#                 emit('messagedeleted', {'index': x, 'sender': sender},
#                      broadcast=True, include_self=True)
#             x += 1
#     return {'response': "Message with the specified items not found."}


# @socketio.on('delete_message_from_evryone')
# def delmessageev(data):
#     sender = data.get('sender')
#     time = data.get('time')
#     typee = data.get('type')
#     name = get_user_data(sender, typee)
#     # (name['name'])
#     message = data.get('message')
#     index = data.get('index')
#     chatroomname = data.get('chatroomname')
#     new_blocked_by = 'h4d64bdy4b4hf74hhh44jfuff848vfn4u48f '+name['name']

#     # Find the chat room by its _id and the specific message by time
#     chat_room = chat_rooms.find_one({"_id": ObjectId(chatroomname)})

#     if chat_room:
#         messages = chat_room.get('messages', [])
#         x = 0
#         for message in messages:
#             # (message.get('timestamp'))
#             # (time)

#             if message.get('timestamp') == time and x == index:
#                 # Add new_blocked_by to the 'blocked_by' list in the specific message
#                 message.setdefault('blocked_by', []).append(new_blocked_by)
#                 # (message)
#                 # Update the chat room with the modified messages list
#                 chat_rooms.update_one(
#                     {"_id": ObjectId(chatroomname)},
#                     {"$set": {"messages": messages}}, upsert=True
#                 )
#                 # (chat_room.get('chat_room_name'))
#                 # Broadcast the message_deleted event to all clients in the chat room
#                 emit('messagedeletedbyall', {'index': x, 'by': new_blocked_by, 'sender': sender},
#                      broadcast=True, include_self=True)
#             x += 1

#     return {'response': "Message with the specified items not found."}


# @app.route('/get_messages', methods=['POST'])
# def get_messages():
#     data = request.get_json()
#     user_id = data.get('user_id')
#     # (user_id)
#     chat_room_name = data.get('chat_room_name')
#     # (chat_room_name)

#     if not user_id or not chat_room_name:
#         return jsonify(messages=[], time=[])

#     # Retrieve messages from the chat room collection
#     chat_room_data = chat_rooms.find_one({"_id": ObjectId(chat_room_name)})
#     if not chat_room_data:
#         # Handle the case where the chat room data is not found
#         return jsonify(messages=[], time=[])

#     messagesli = chat_room_data.get("messages", [])
#     messages = []
#     time = []
#     sender = []
#     bloaked_by = []
#     diffl = []

#     for m in messagesli:
#         a = m.get('message')
#         b = m.get('timestamp')
#         diff = m.get('diff')
#         # (b)
#         c = m.get('sender')
#         d = m.get('blocked_by')
#         messages.append(a)
#         time.append(b)
#         sender.append(c)
#         bloaked_by.append(d)
#         diffl.append(diff)
#     # (time)
#     # bloaked()_by[0] is a lsit

#     return jsonify(messages=messages, time=time, sender=sender, blb=bloaked_by, diff=diffl)


@app.route('/home-c/<x>/<y>')
def home_c(x, y):
    if not check(request.cookies, 'file'):
        return redirect(url_for('main'))

    elif check(request.cookies, 'file') and turbolancer_data_Security.decrypt(key, getkey(request.cookies)['ideo']) != x:
        return redirect(url_for('main'))
    user_data = user_collection.find_one(
        {"_id": x, 'd': y}) or seller_collection.find_one({"_id": x})

    if user_data:
        email = turbolancer_data_Security.decrypt(key, user_data["email"])
        image = user_data["image"]
        name = user_data["name"]
        # tag = user_data["tag"]
        country = turbolancer_data_Security.decrypt(key, user_data["country"])
        ph = turbolancer_data_Security.decrypt(key, user_data["phone_number"])

        year = user_data['account_created_in']
        method = user_data["payment_method"]
        user_id = x
        account = ['c', 'd']

        if 'c' in account:
            return render_template(
                'clint-side-db.html', name=name, image=image, aclink=f'/account/{user_id}/{y}')

    return redirect(url_for('main'))


@app.route('/update_profile', methods=['POST'])
def update_profile():
    cookies = getkey(request.cookies)
    image_data = ''
    encoded_email = cookies.get('emalo')
    ideo = turbolancer_data_Security.decrypt(key, cookies.get('ideo'))
    check_result = check(request.cookies, 'file')
    if not check_result:
        return redirect(url_for('main'))

    elif check_result and request.method == 'POST':
        data = dict(request.form)
        file = request.files.get('image')
        if file:
            image_data = file.read()
            upload_image_local(image_data, encoded_email, ideo)

        data = handle_data_encryption(data)

        collection = get_collection(ideo, encoded_email)
        update_database(collection, ideo, encoded_email, data)

        print(data)
        return jsonify({"success": True})

    return jsonify({"success": False})

def handle_data_encryption(data):
    if data.get('bir'):
        data['bir'] = turbolancer_data_Security.encrypt(key, data['bir'])
    if data.get('gan'):
        data['gan'] = turbolancer_data_Security.encrypt(key, data['gan'])
    return data

def get_collection(ideo, encoded_email):
    if seller_collection.find_one({'_id': ideo, "email": encoded_email}):
        return seller_collection
    else:
        return user_collection
def split_into_child_arrays(original_array):
    child_arrays = []
    for i in range(0, len(original_array), 3):
        child_array = original_array[i:i+3]
        child_arrays.append(child_array)
    return child_arrays


@app.route('/delItem', methods=['POST'])
def delItem():
    cookies = getkey(request.cookies)
    encoded_email = cookies.get('emalo')
    ideo = turbolancer_data_Security.decrypt(key, cookies.get('ideo'))
    check_result = check(request.cookies, 'file')
    if not check_result:
        return redirect(url_for('main'))

    elif check_result and request.method == 'POST':
        data = request.form
        print(data['sk'])
        ud = seller_collection.find_one({'_id': ideo, "email": encoded_email})
        if ud and ud['sk']:
            base : list = ud['sk']
            for x in range(len(ud['sk'])):
                if base[x][0] == data['sk']:
                    base.pop(x)
                    seller_collection.update_one({"_id": ideo, "email": encoded_email}, {"$set": {'sk': base}})
                    return jsonify({"success": True})
        return jsonify({"success": False})
    return jsonify({"success": False})




def update_database(collection, ideo, encoded_email, data):
    for field in ['bir', 'gan', 'name', 'about_self', 'sk']:
        if field == 'sk' and data.get(field):
            arr = data['sk'].split(',')
            arr = split_into_child_arrays(arr)  # Assuming this function is defined elsewhere
            ud = collection.find_one({'_id': ideo, "email": encoded_email})
            if ud and 'sk' in ud:
                main_arr = ud['sk']
                print(main_arr)
                for x in range(len(arr)):
                    found = False
                    for y in range(len(main_arr)):
                        if main_arr[y][0] == arr[x][0]:
                            main_arr[y] = arr[x]
                            found = True
                            break
                    if not found:
                        main_arr.append(arr[x])
                print(main_arr)

                collection.update_one({"_id": ideo, "email": encoded_email}, {"$set": {'sk': main_arr}})
        elif data.get(field):
            collection.update_one({"_id": ideo, "email": encoded_email}, {"$set": {field: data[field]}})


def delete_image(image_id):
    image_id = image_id.split('/')[-1]
    filter = {'_id': ObjectId(image_id)}

    result = image_collection.delete_one(filter)

    if result.deleted_count > 0:
        print(f'Image with ID {image_id} deleted successfully.')
    else:
        print(f'No image found with ID {image_id}.')


def get_user_dataA(user_id):
    user_data = user_collection.find_one({"_id": user_id})
    if user_data:
        email = turbolancer_data_Security.decrypt(key, user_data["email"])
        image = user_data["image"]
        name = user_data["name"]
        country = turbolancer_data_Security.decrypt(key, user_data["country"])
        ph = turbolancer_data_Security.decrypt(key, user_data["phone_number"])
        year = user_data['account_created_in']
        method = user_data["payment_method"]
        bir = turbolancer_data_Security.decrypt(key, user_data["bir"])
        gan = turbolancer_data_Security.decrypt(key, user_data.get("gan", None)) or None
        tag = user_data['tag'] or None

        return {
            'name': name,
            'image': image,
            'email': email,
            'country': country,
            'ph': ph,
            'year': year,
            'bir': bir,
            'tag': tag,
            'gan': gan
        }

    return None


def get_developer_data(developer_id):
    developer_data = seller_collection.find_one({"_id": developer_id})
    if developer_data:
        email = turbolancer_data_Security.decrypt(key, developer_data["email"])
        image = developer_data["image"]
        name = developer_data["name"]
        country = turbolancer_data_Security.decrypt(key, developer_data["country"])
        ph = turbolancer_data_Security.decrypt(key, developer_data["phone_number"])
        year = developer_data['account_created_in']
        method = developer_data["payment_method"]
        grade = developer_data['grade']
        rating = developer_data['rating']
        about_self = developer_data['about_self']
        tag = developer_data['tag'] or None
        sk = developer_data['sk'] or None
        earnings = developer_data['earnings'] or None
        bir = turbolancer_data_Security.decrypt(key, developer_data["bir"]) or None
        gan = turbolancer_data_Security.decrypt(key, developer_data.get("gan", None)) or None
        length = len(sk) if sk else 0
        return {
            'name': name,
            'image': image,
            'email': email,
            'country': country,
            'ph': ph,
            'year': year,
            'about_self': about_self,
            'rating': rating,
            'grade': grade,
            'tag': tag,
            'bir': bir,
            'gan': gan,
            'sk':sk,
            'earnings' : earnings,
            'len':length
        }
    return None
@app.route('/account/<x>/<y>')
def account(x, y):
  

    if not check(request.cookies, 'file'):
        return redirect(url_for('main'))

    decrypted_x = turbolancer_data_Security.decrypt(
        key, getkey(request.cookies)['ideo'])

    if check(request.cookies, 'file') and decrypted_x != x:
        ud = get_user_dataA(x) or get_developer_data(x)
        lud = get_user_dataA(decrypted_x) or get_developer_data(decrypted_x)

        if ud['ph'] == lud['ph']:

            if y in ['c', 'd']:
                if y == 'c':
                    user_data = get_user_dataA(x)
                    if user_data:
                        # Dummy data for user_data
                        user_data['total_earnings'] = "$12,345"
                        user_data['total_catalog_items'] = 125
                        user_data['total_projects'] = 42
                        user_data['user_rating'] = 4.8
                        return render_template('profile_page.html', **user_data, )
                elif y == 'd':
                    developer_data = get_developer_data(x)
                    if developer_data:
                        # Dummy data for developer_data
                        developer_data['total_catalog_items'] = 125
                        developer_data['total_projects'] = 42
                        developer_data['rating'] = float(developer_data['rating'])
                        
                        return render_template('profile_page.html', **developer_data, d='avail')

                    return redirect(url_for('main'))
        return redirect(url_for('main'))


    if y in ['c', 'd']:
        if y == 'c':
            user_data = get_user_dataA(x)
            if user_data:
                # Dummy data for user_data
                user_data['total_earnings'] = "$12,345"
                user_data['total_catalog_items'] = 125
                user_data['total_projects'] = 42
                user_data['user_rating'] = 4.8
                return render_template('profile_page.html', **user_data, )
        elif y == 'd':
            developer_data = get_developer_data(x)
            if developer_data:
                # Dummy data for developer_data
                developer_data['total_catalog_items'] = 125
                developer_data['total_projects'] = 42
                developer_data['rating'] = float(developer_data['rating'])

                return render_template('profile_page.html', **developer_data, d='avail', x = 'yes')

            return redirect(url_for('main'))

    return redirect(url_for('main'))


@app.errorhandler(404)
def page_not_found(error):
    return '404'


@app.route('/upjobpage')
def page():
    return render_template('upload_job.html')


@app.route('/getserved')
def get_searved():
    return render_template('get_served.html')


@app.route('/proj')
def proj():
    return render_template('project.html')

def remove_word_without_space(text, word):
    pattern = rf'\b{word}(?!\s)'
    return re.sub(pattern, '', text)
def remove_first_uppercase(s):
    if len(s) >= 2 and s[:2].isupper():
        return s[1:]
    return s
@app.route('/rephrase_text', methods=['POST'])
def rephrase():
    data = request.get_json()
    input_text = data.get('text')
    main = data.get('main')
    print(main)
    print(input_text)
    response = TurboLancer_RePhrase_text.do(input_text,main)
  
    response = response.replace('\n','')
    response = response.replace(']]','')
    response = response.replace('[[','')
    response = response.replace('[[[','')
    response = response.replace(']]]','')
    response = response.replace('IIPlease','')
    response = response.replace('IPlease','')
    response = response.replace('IIIPlease','')
    response = response.replace('IIIIPlease','')
    response = response.replace('TheI','I')
    response = response.replace('I I','I')
    response = response.replace('II','I')
    response = response.replace('BasedBased on','Based')
    response = response.replace('BasedBased','')
    response = response.replace('Based the','Based on the')
    response = response.replace('the client form','this project')
    response = response.replace('is is','is')    
    response = response.replace('ForFor','For')    
    response = response.replace('BasedI','I')
    response = response.replace('[IBased','Based')
    response = remove_word_without_space(response, 'Based')
    response = remove_word_without_space(response, 'The')
    response = remove_word_without_space(response, 'For')
    # response = remove_first_uppercase(response)

    print(response)
    return jsonify(text=response)


if __name__ == '__main__':
    socketio.run(app, debug=True)
