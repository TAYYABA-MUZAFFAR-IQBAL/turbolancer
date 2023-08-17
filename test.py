import random
from flask import Flask, request, render_template, redirect, url_for, jsonify, send_file, send_from_directory, render_template_string
from flask_wtf import FlaskForm
from wtforms import FileField
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import io
import uuid
import datetime
import turbolancer_data_Security
from jinja2 import Environment, FileSystemLoader
from flask_socketio import SocketIO, emit


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
developer_collection = db['developers']
user_collection = db['users']
serving_sectors_collection = db['serving_sectors']
sectors_technologies_collection = db['technologies']
chat_rooms = db['chatrooms']
question_collection = db['questions']
image_collection = db['images']


def generate_id():
    return str(uuid.uuid4())


# Form for uploading images
class ImageUploadForm(FlaskForm):
    image = FileField('Image')


@app.route('/')
def main():
    return render_template('index.html')


@app.route("/signup_d", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        encoded_email = turbolancer_data_Security.encrypt(
            key, request.form["email"])
        encoded_password = turbolancer_data_Security.encrypt(
            key, request.form["ps"])
        encoded_phone = turbolancer_data_Security.encrypt(
            key, request.form['ph'])
        encoded_country = turbolancer_data_Security.encrypt(
            key, request.form['con'])
        d = 'd'
        skils = []

        # Check if the developer already exists in the database
        print(encoded_email)
        user = developer_collection.find_one({"email": encoded_email})

        if user:
            return render_template("signup-c.html",  x='This  Seller already exists!', y='onload= this.click')
        else:
            t = name.replace(' ', '')
            tag = '@' + t
            user_id = generate_id()
            count = developer_collection.count_documents({"name": name})
            count = int(count)+1
            year = datetime.date.today().year
            count = str(count)
            user = {
                "_id": user_id,
                'image': '',
                "name": name,
                'tag': tag + str(count),
                "email": encoded_email,
                "password": encoded_password,
                "country": encoded_country,
                'phone_number': encoded_phone,
                'about_self': '',
                'd': d,
                'sk': skils,
                'grade': 'C',
                'earnings': 0,
                'rating': 0.0,
                'member_since': year,
                'english': '',
                'payment_method': 'Visa',
                'project_history': []
            }
            developer_collection.insert_one(user)

            return render_template('dataform.html', id=user_id, name=name, email=encoded_email)

    return render_template("signup-c.html")


@app.route("/signup_and_upload_image", methods=['GET', "POST"])
def signup_and_upload_image():
    if request.method == "POST":
        # Retrieve form data, including the encrypted email
        name = request.form["name"]
        encoded_email = turbolancer_data_Security.encrypt(
            key, request.form["email"])
        encoded_password = turbolancer_data_Security.encrypt(
            key, request.form["ps"])
        encoded_phone = turbolancer_data_Security.encrypt(
            key, request.form["ph"])
        encoded_country = turbolancer_data_Security.encrypt(
            key, request.form["con"])
        d = "c"

        # Check if the user already exists in the database
        user = user_collection.find_one({"email": encoded_email})

        if user:
            return jsonify({"error": "This user already exists!"})

        # Save the uploaded image to the database
        image = request.files["image"]
        image_data = image.read()
        image_id = image_collection.insert_one(
            {"data": image_data}).inserted_id

        # Update the user collection with the associated image link
        user_id = generate_id()
        year = datetime.date.today().year
        user = {
            "_id": user_id,
            "image": "/get_image/" + str(image_id),
            "name": name,
            "email": encoded_email,
            "password": encoded_password,
            "country": encoded_country,
            "phone_number": encoded_phone,
            "d": d,
            "spending": 0,
            "account_created_in": year,
            "payment_method": "Visa",
            "orders_history": [],
        }
        user_collection.insert_one(user)

        # Return a success response
        return jsonify({"message": "Signup and image upload successful."})

    return render_template("sin-c.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        encoded_email = turbolancer_data_Security.encrypt(
            key, request.form["email"])
        encoded_password = turbolancer_data_Security.encrypt(
            key, request.form["ps"])

        user = developer_collection.find_one({"email": encoded_email})

        if user:
            return render_template("signin.html", a="This User does not exist!")
        else:
            user_id = generate_id()
            user = {"_id": user_id, "email": encoded_email,
                    "password": encoded_password}
            developer_collection.insert_one(user)

            return render_template('home.html')

    return render_template("signin.html")


@app.route('/insert_skill', methods=['GET', 'POST'])
def insert_skill():
    if request.method == 'POST':
        skill = request.form['skill']
        image = request.form['image']
        req = request.form['test_req']
        skill_id = generate_id()

        skill_data = {"_id": skill_id, "skill": skill,
                      "image": image, 'req': req}
        serving_sectors_collection.insert_one(skill_data)

        return redirect(url_for('insert_skill'))

    return render_template('insert_skill.html')


@app.route('/insert_tech', methods=['GET', 'POST'])
def insert_tech():
    if request.method == 'POST':
        sec = request.form.get('sector')
        tech = request.form.get('tech')
        image = request.form.get('image')
        req = request.form.get('req')
        skill_id = generate_id()

        skill_data = {"_id": skill_id, "sector": sec,
                      "tech": tech, "image": image, 'req': req}
        sectors_technologies_collection.insert_one(skill_data)

        return redirect(url_for('insert_tech'))

    return render_template('technology.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/api/quiz/<path:x>', methods=['GET'])
def get_quiz_data(x):
    topics = x.split('|')  # Split the path parameter into individual topics
    all_questions = []
    answer = 40/len(topics)
    rounded_answer = round(answer)
    print(rounded_answer)
    for topic in topics:
        topic = topic.replace('_', ' ')
        filtered_data = list(question_collection.find({"topic": topic}))
        random.shuffle(filtered_data)
        # Select the first 40 questions or all available questions if there are fewer
        selected_questions = filtered_data[:min(
            len(filtered_data), rounded_answer)]
        all_questions.extend(selected_questions)

    # Shuffle all the selected questions from different topics
    random.shuffle(all_questions)
    serializable_data = [{'topic': item['topic'], 'question': item['question'],
                          'options': item['options'], 'correctIndex': item['correctIndex']} for item in all_questions]

    return jsonify(serializable_data)


@app.route('/update_value', methods=['POST'])
def update_value():
    data = request.get_json()

    value = data['rangeValue']
    encoded_email = data['email']
    print(encoded_email)

    developer = developer_collection.find_one({"email": encoded_email})

    if developer:
        developer_collection.update_one(
            {"email": encoded_email}, {"$set": {"english": value}})
        return jsonify({'link': f'/selects_skill/{encoded_email}'})
    else:
        return jsonify({'error': 'Developer not found.'})


@app.route('/selects_skill/<email>')
def selects_skill(email):
    if email:
        developer = developer_collection.find_one({"email": email})
        img = developer['image']
        name = developer['name']
        email = turbolancer_data_Security.decrypt(key, email)
        print(email)
        skills = serving_sectors_collection.find()
        encoded_skills = skills

        template_path = 'template/select_sk.html'
        with open(template_path, 'r') as file:
            template_content = file.read()

        rendered_template = render_template_string(template_content, x='hi', h1='Select your serving sector', function2='next(this)', function1=None, disc='Click to select tecknology for ',
                                                   b='Select technology', o=encoded_skills, image=img, name=name, email2=turbolancer_data_Security.encrypt(key, email), email=email)

        return rendered_template
    else:
        return '<h1><b>Method Not Allowd</b></h1>'


@app.route('/select_technology/<email>/<topic>')
def select_technology(email, topic):
    if email and topic:
        developer = developer_collection.find_one({"email": email})
        img = developer['image']
        name = developer['name']
        email = turbolancer_data_Security.decrypt(key, email)
        print(email)

        # Filter skills based on the provided topic
        skills = sectors_technologies_collection.find({"sector": topic})

        encoded_skills = []
        for skill in skills:
            encoded_skill = {'skill': skill['tech'], 'image': skill['image']}
            encoded_skills.append(encoded_skill)

        template_path = 'template/select_sk.html'
        with open(template_path, 'r') as file:
            template_content = file.read()

        rendered_template = render_template_string(
            template_content, h1=f'Select technology for {topic}', function2=None, function1='select(this)', disc='Click to choose technology', b='Take test', o=encoded_skills, image=img, name=name, email=email)

        return rendered_template

    else:
        return '<h1><b>Method Not Allowd</b></h1>'


@app.route('/UPLOAD_IMAGE', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        # Obtain the uploaded image and the email from the request payload
        image = request.files['image']
        encoded_email = request.form.get('email')
        print(encoded_email)

        # Retrieve the developer document
        developer = developer_collection.find_one({"email": encoded_email})

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
        developer_collection.update_one({"email": encoded_email}, {
                                        "$set": {"image": '/get_image/' + str(image_id)}})

        return jsonify({'image_id': str(image_id)})
    else:
        return jsonify({'error': 'No image file found'})


@app.route('/send_IMAGE', methods=['POST'])
def send_image():
    if 'image' in request.files:
        # Obtain the uploaded image and the email from the request payload
        image = request.files['image']
        chatroom_Id = request.form.get('chatroom')
        print(chatroom_Id)

        # Retrieve the developer document
        chatroom = chat_rooms.find_one({"_id": ObjectId(chatroom_Id)})

        # Save the uploaded image to the database
        image_data = image.read()
        image_id = image_collection.insert_one(
            {'data': image_data}).inserted_id

        return jsonify({'image_id': '/turbolancer/gett_image/chats/turbolancer_qazwsxedcrfvqwerty/'+str(image_id)})
    else:
        return jsonify({'error': 'No image file found'})


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
@app.route('/turbolancer/gett_image/chats/turbolancer_qazwsxedcrfvqwerty/<image_id>', methods=['GET'])
def mess(image_id):
    # Retrieve the image from the database
    image_data = image_collection.find_one({'_id': ObjectId(image_id)})

    if image_data and 'data' in image_data:
        # Serve the image data with appropriate content type
        return send_file(io.BytesIO(image_data['data']), mimetype='image/jpeg')
    else:
        return jsonify({'error': 'Image not found'})


@app.route('/update_data', methods=['POST'])
def update_data():
    data = request.get_json()
    encoded_email = data.get('email')
    print(encoded_email)

    text_area_value = data.get('textAreaValue')

    if encoded_email and text_area_value:
        developer = developer_collection.find_one({"email": encoded_email})

        if developer:
            developer_collection.update_one({"email": encoded_email}, {
                                            "$set": {"about_self": text_area_value}})
            return jsonify({'message': 'Data updated successfully.'})
        else:
            return jsonify({'error': 'Developer not found.'})
    else:
        return jsonify({'error': 'Invalid data.'})


@app.route('/update_result', methods=['POST'])
def update_result():
    data = request.get_json()
    encoded_email = data.get('email')
    print(encoded_email)

    text_area_value = data.get('result')

    if encoded_email and text_area_value:
        developer = developer_collection.find_one({"email": encoded_email})
        skill = developer_collection.find_one({"sk": encoded_email})

        if developer:
            developer_collection.update_one({"email": encoded_email}, {
                                            "$set": {"about_self": text_area_value}})
            return jsonify({'message': 'Data updated successfully.'})
        else:
            return jsonify({'error': 'Developer not found.'})
    else:
        return jsonify({'error': 'Invalid data.'})


@app.route('/Dashbord')
def Dashbord():
    return render_template('home.html')


@app.route('/try')
def index():
    return render_template('try.html')


def get_user_data(user_id, Atype):
    if 'd' in Atype:
        user_data = developer_collection.find_one({"_id": user_id})
    elif 'c' in Atype:
        user_data = user_collection.find_one({'_id': user_id})
    return user_data

@socketio.on('join')
def handle_join(data):
    user_id = data['userId']
    account = data['account']
    # Retrieve the user's chat room list from the user collection
    user_data = get_user_data(user_id, account)

    if user_data is None:
        emit('join_response', {"status": "USER_NOT_FOUND"})
        return

    chat_rooms_list = user_data.get("chat_rooms", [])
    print(chat_rooms_list)
    namesli = []
    img_s = []
    chids = []
    last_message=[]

    for names in chat_rooms_list:
        other_users = user_collection.find({"chat_rooms": {"$in": [names]}})
        chat_room_data = chat_rooms.find_one({"chat_room_name": names})

        if not other_users:
            other_users = developer_collection.find(
                {"chat_rooms": {"$in": [names]}})
            chat_room_data = chat_rooms.find_one({"chat_room_name": names})

        for user in other_users:
            name = user.get('name')
            img = user.get('image')
            id = user.get('_id')
            chid = chat_room_data.get('_id')
            chid = str(chid)
            print(id)
            if id not in chat_rooms_list:
                namesli.append(name)
                img_s.append(img)
                chids.append(chid)

    emit('join_response', {'status': 'OK',
         "name": namesli, "imgs": img_s, 'chid': chids, 'last_message': last_message})


@socketio.on('sendMessage')
def handle_send_message(data):
    user_id = data['userId']
    current_time = data['currentTime']
    chat_room_name = data['chatRoomName']
    message = data.get('message')
    image_link = data.get('imageLink')
    print(image_link)

    if image_link:
        chat_rooms.update_one(
            {"_id": ObjectId(chat_room_name)},
            {"$push": {"messages": {'message': image_link,
                                    'timestamp': current_time, 'sender': user_id}}},
            upsert=True
        )
        emit('newMessage', {'message': image_link, 'timestamp': current_time, 'sender': user_id},
             broadcast=True, include_self=True)

    else:
        chat_rooms.update_one(
            {"_id": ObjectId(chat_room_name)},
            {"$push": {"messages": {'message': message,
                                    'timestamp': current_time, 'sender': user_id}}},
            upsert=True
        )
        emit('newMessage', {'message': message, 'timestamp': current_time, 'sender': user_id},
             broadcast=True, include_self=True)

    # Emit the new message to all clients in the chat room


@app.route('/get_messages', methods=['POST'])
def get_messages():
    data = request.get_json()  # Get the JSON data from the request body
    user_id = data.get('user_id')
    print(user_id)
    chat_room_name = data.get('chat_room_name')
    print(chat_room_name)

    if not user_id or not chat_room_name:
        return jsonify(messages=[], time=[])

    # Retrieve messages from the chat room collection
    chat_room_data = chat_rooms.find_one({"_id": ObjectId(chat_room_name)})
    if not chat_room_data:
        # Handle the case where the chat room data is not found
        return jsonify(messages=[], time=[])

    messagesli = chat_room_data.get("messages", [])
    messages = []
    time = []
    sender = []

    for m in messagesli:
        a = m.get('message')
        b = m.get('timestamp')
        print(b)
        c = m.get('sender')
        messages.append(a)
        time.append(b)
        sender.append(c)
    print(time)

    return jsonify(messages=messages, time=time, sender=sender)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
