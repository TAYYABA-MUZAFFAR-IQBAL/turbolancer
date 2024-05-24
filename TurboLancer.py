# romE2I69nPailBx4S8agYb09En3XPhhVJXnE74qChVS sandbox api
# set CLOUDINARY_URL=cloudinary://489474321839884:82k4ZB3pAQWVtZSzfdHHLMpo0QM@dfew09nzc
# romE2I69nPailBx4S8agYb09En3XPhhVJXnE74qChVS sandbox api
import os
import re
import io
import uuid
import json
import random
import datetime
from urllib.parse import unquote
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    jsonify,
    send_file,
    render_template_string,
    abort,
)
from flask_wtf import FlaskForm
from wtforms import FileField
from pymongo import MongoClient
from bson.objectid import ObjectId
import turbolancer_data_Security
import TurboLancer_RePhrase_text
from flask_socketio import SocketIO, emit, join_room
from werkzeug.datastructures import ImmutableMultiDict
import uploade_video as uv
from jinja2 import Environment, FileSystemLoader
import base64
app = Flask(__name__, template_folder="template", static_folder="static")
app.config["SECRET_KEY"] = os.urandom(24)
socketio = SocketIO(app)
env = Environment(loader=FileSystemLoader("template"))

# Connect to MongoDB
client = MongoClient(
    "mongodb+srv://junaidiqbal:allahsadaro@junaid.lkpmjko.mongodb.net/?retryWrites=true&w=majority"
)
db = client["Tasker"]
key = b'||/:?"(:@junaid)'

# Set collection names
seller_collection = db["Sellers"]
user_collection = db["users"]
serving_sectors_collection = db["serving_sectors"]
sectors_technologies_collection = db["technologies"]
chat_rooms = db["chatrooms"]
question_collection = db["questions"]
image_collection = db["images"]
catalogue_collection = db["catalogue"]
slideshow_collection = db["slideshow"]


def generate_id():
    return str(uuid.uuid4())


def getkey(data):
    keys_to_find = ["ideo", "emalo", "deno"]
    found_items = {key: data.get(key) for key in keys_to_find if key in data}
    return found_items


def check(data, file):
    try:
        compound = getkey(data)
        if compound:
            if compound.get("ideo", None):
                id_ = turbolancer_data_Security.decrypt(key, compound.get("ideo", None))
                ud = seller_collection.find_one(
                    {"_id": id_}
                ) or user_collection.find_one({"_id": id_})

                if ud:
                    if (
                        compound.get("emalo") == ud["email"]
                        and ud["d"] == "d"
                        and not compound.get("deno")
                    ):
                        return None
                    elif (
                        compound.get("emalo") == ud["email"]
                        and ud["d"] == "d"
                        and compound.get("deno")
                    ):
                        return file
                    elif compound.get("emalo") == ud["email"] and ud["d"] == "c":
                        return file
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"An error occurred in check function: {e}")
        return None


# Form for uploading images
class ImageUploadForm(FlaskForm):
    image = FileField("Image")


@app.route("/")
def main():
    try:
        cookies = getkey(request.cookies)
        if cookies.get("ideo"):
            id_ = turbolancer_data_Security.decrypt(key, cookies.get("ideo"))
            ud = seller_collection.find_one({"_id": id_}) or user_collection.find_one(
                {"_id": id_}
            )
            if (
                cookies.get("emalo") == ud.get("email")
                and ud.get("d") == "d"
                and not cookies.get("deno")
            ):
                return redirect(f'/addinfo/{id_}/{ud["name"]}/{ud["email"]}')
            elif (
                cookies.get("emalo") == ud["email"]
                and ud["d"] == "d"
                and cookies.get("deno")
            ):
                return redirect(f'/home-c/{id_}/{ud["d"]}')
            elif cookies.get("emalo") == ud["email"] and ud["d"] == "c":
                return redirect(f'/home-c/{id_}/{ud["d"]}')
    except Exception as e:
        print(f"An error occurred in main route: {e}")

    return render_template("index.html")


@app.route("/start_selling_now", methods=["GET", "POST"])
def signup():
    try:
        if check(request.cookies, "file") is not None:
            return redirect(url_for("main"))

        if not check(request.cookies, "file") and request.method == "POST":
            name = request.form["name"]
            encoded_email = turbolancer_data_Security.encrypt(
                key, request.form["email"]
            )
            encoded_password = turbolancer_data_Security.encrypt(
                key, request.form["ps"]
            )
            encoded_phone = turbolancer_data_Security.encrypt(key, request.form["ph"])
            encoded_bir = turbolancer_data_Security.encrypt(
                key, request.form.get("bir")
            )
            encoded_gan = turbolancer_data_Security.encrypt(
                key, request.form.get("gan")
            )
            encoded_country = turbolancer_data_Security.encrypt(
                key, request.form["con"]
            )
            d = "d"

            user = (
                seller_collection.find_one({"email": encoded_email})
                or user_collection.find_one({"email": encoded_email})
                or seller_collection.find_one({"ph": encoded_phone})
                or user_collection.find_one({"ph": encoded_phone})
            )
            user_ph = (
                seller_collection.find_one({"ph": encoded_phone})
                or user_collection.find_one({"ph": encoded_phone})
                or seller_collection.find_one({"ph": encoded_phone})
                or user_collection.find_one({"ph": encoded_phone})
            )
            user_id = generate_id()

            if user or user_ph:
                return render_template(
                    "signup-c.html",
                    x="Account already exists with this email/phone.",
                    y="onload= this.click",
                )
            else:
                t = name.replace(" ", "")
                tag = "@" + t
                user_id = generate_id()
                count = seller_collection.count_documents({"name": name})
                count_s = user_collection.count_documents({"name": name})
                count = str((int(count + count_s) + 1) * 1000)[::-1]
                year = datetime.date.today().year
                month = datetime.date.today().strftime("%b")
                count = str(count)
                if count:
                    count += str(random.randint(0, 9))
                user = {
                    "_id": user_id,
                    "image": "",
                    "name": name,
                    "tag": tag + count,
                    "email": encoded_email,
                    "password": encoded_password,
                    "country": encoded_country,
                    "phone_number": encoded_phone,
                    "about_self": "",
                    "d": d,
                    "sk": [],
                    "grade": "C",
                    "earnings": [0],
                    "rating": 0,
                    "english": "",
                    "payment_method": "Visa",
                    "project_history": [],
                    "chat_rooms": [],
                    "account_created_in": str(month) + " " + str(year),
                    "bir": encoded_bir,
                    "gan": encoded_gan,
                }

                seller_collection.insert_one(user)
                ide = user_id
                user_id = turbolancer_data_Security.encrypt(key, user_id)
            return render_template(
                "save_cook.html",
                keys=[["ideo", "emalo", "tp"], [user_id, encoded_email, "d"]],
                redi=f"addinfo/{ide}/{name}/{encoded_email}",
            )
    except Exception as e:
        print(f"An error occurred in signup route: {e}")

    return render_template("signup-c.html")


@app.route("/addinfo/<x>/<y>/<z>")
def addinfo(x, y, z):
    try:
        cookies = getkey(request.cookies)
        if cookies:
            if cookies.get("emalo") in z:
                return render_template(
                    "dataform.html",
                    id=x,
                    name=y,
                    email=z,
                    emaloz=turbolancer_data_Security.decrypt(key, cookies.get("emalo")),
                )
            else:
                return redirect(url_for("main"))
        else:
            return redirect(url_for("main"))
    except Exception as e:
        print(f"An error occurred in addinfo route: {e}")
        return redirect(url_for("main"))


@app.route("/begin_client_journey", methods=["GET", "POST"])
def signup_and_upload_image():
    try:
        if check(request.cookies, "file") is not None:
            return redirect(url_for("main"))

        if not check(request.cookies, "file") and request.method == "POST":
            name = request.form.get("name")
            encoded_email = turbolancer_data_Security.encrypt(
                key, request.form["email"]
            )
            encoded_password = turbolancer_data_Security.encrypt(
                key, request.form["ps"]
            )
            encoded_phone = turbolancer_data_Security.encrypt(key, request.form["ph"])
            encoded_country = turbolancer_data_Security.encrypt(
                key, request.form["con"]
            )
            d = "c"
            encoded_bir = turbolancer_data_Security.encrypt(
                key, request.form.get("bir")
            )
            encoded_gan = turbolancer_data_Security.encrypt(
                key, request.form.get("gan")
            )

            user = (
                seller_collection.find_one({"email": encoded_email})
                or user_collection.find_one({"email": encoded_email})
                or seller_collection.find_one({"ph": encoded_phone})
                or user_collection.find_one({"ph": encoded_phone})
            )
            user_ph = (
                seller_collection.find_one({"ph": encoded_phone})
                or user_collection.find_one({"ph": encoded_phone})
                or seller_collection.find_one({"ph": encoded_phone})
                or user_collection.find_one({"ph": encoded_phone})
            )
            user_id = generate_id()

            if "image" not in request.files:
                return render_template("error.html", message="No image uploaded")
            else:
                image = request.files["image"]
                image_data = image.read()
                image_id = image_collection.insert_one({"data": image_data}).inserted_id

            if user or user_ph:
                return render_template(
                    "sin-c.html",
                    x="Account already exists with this email/phone.",
                    y="onload= this.click",
                )

            elif user is None and user_ph is None:
                t = name.replace(" ", "")
                tag = "@" + t
                user_id = generate_id()
                count = seller_collection.count_documents({"name": name})
                count_s = user_collection.count_documents({"name": name})
                count = str((int(count + count_s) + 1) * 1000)[::-1]
                year = datetime.date.today().year
                month = datetime.date.today().strftime("%b")

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
                    "account_created_in": str(month) + " " + str(year),
                    "payment_method": "Visa",
                    "orders_history": [],
                    "bir": encoded_bir,
                    "gan": encoded_gan,
                }

                user_collection.insert_one(user)
                ide = user_id
                user_id = turbolancer_data_Security.encrypt(key, user_id)
                return jsonify(
                    {
                        "success": True,
                        "redirect_url": f'/redi/{user_id}/{encoded_email}/{ide}/{user["d"]}/none',
                    }
                )
        return render_template("sin-c.html")
    except Exception as e:
        print(f"An error occurred in signup_and_upload_image route: {e}")
        return render_template("sin-c.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    try:
        if check(request.cookies, "file") is not None:
            return redirect(url_for("main"))

        if not check(request.cookies, "file") and request.method == "POST":
            encoded_email = turbolancer_data_Security.encrypt(
                key, request.form["email"]
            )
            encoded_password = turbolancer_data_Security.encrypt(
                key, request.form["ps"]
            )

            user = seller_collection.find_one(
                {"email": encoded_email}
            ) or user_collection.find_one({"email": encoded_email})

            if user:
                stored_password = user["password"]
                if stored_password != encoded_password:
                    return jsonify({"error": "Incorrect password!"})
                else:
                    ide = user["_id"]
                    user_id = turbolancer_data_Security.encrypt(key, ide)

                    if user["d"] == "d" and (
                        user["image"] == "" or user["about_self"] == ""
                    ):
                        return jsonify(
                            {
                                "success": True,
                                "redirect_url": f'redi/{user_id}/{encoded_email}/{ide}/{user["d"]}/none',
                            }
                        )

                    return jsonify(
                        {
                            "success": True,
                            "redirect_url": f'redi/{user_id}/{encoded_email}/{ide}/{user["d"]}/_[__xxx__%12*79)(56)[:]-++784kdd]_',
                        }
                    )

            else:
                return jsonify({"error": "Account does not exist!"})
    except Exception as e:
        print(f"An error occurred in signin route: {e}")
        return jsonify({"error": "An error occurred during sign-in."})

    return render_template("singin.html")


@app.route("/redi/<user_id>/<encoded_email>/<ide>/<user_d>/<deno>")
def redi(user_id, encoded_email, ide, user_d, deno):
    try:
        expected_deno = "_[__xxx__%12*79)(56)[:]-++784kdd]_"
        if unquote(expected_deno) == deno:
            return render_template(
                "save_cook.html",
                keys=[
                    ["ideo", "emalo", "tp", "deno"],
                    [user_id, encoded_email, user_d, deno],
                ],
                redi=f"/home-c/{ide}/{user_d}",
            )

        return render_template(
            "save_cook.html",
            keys=[["ideo", "emalo", "tp"], [user_id, encoded_email, user_d]],
            redi=f"/home-c/{ide}/{user_d}",
        )
    except Exception as e:
        print(f"An error occurred in redi route: {e}")
        return redirect(url_for("main"))


@app.route("/UPLOAD_IMAGE", methods=["POST"])
def upload_image():
    try:
        if "image" in request.files:
            image = request.files["image"]
            encoded_email = request.form.get("email")

            developer = seller_collection.find_one({"email": encoded_email})

            if developer and "image" in developer:
                previous_image_link = developer["image"]
                if previous_image_link != "":
                    previous_image_id = previous_image_link.split("/")[-1]
                    image_collection.delete_one({"_id": ObjectId(previous_image_id)})

            image_data = image.read()
            image_id = image_collection.insert_one(
                {"data": image_data, "reference": developer["_id"]}
            ).inserted_id

            seller_collection.update_one(
                {"email": encoded_email},
                {"$set": {"image": "/get_image/" + str(image_id)}},
            )

            return jsonify({"image_id": str(image_id)})
        else:
            return jsonify({"error": "No image file found"})
    except Exception as e:
        print(f"An error occurred in upload_image route: {e}")
        return jsonify({"error": "An error occurred during image upload."})


def upload_image_local(image_data, encoded_email, ideo):
    collection = seller_collection.find_one(
        {"_id": ideo, "email": encoded_email}
    ) or user_collection.find_one({"_id": ideo, "email": encoded_email})
    if "image" in collection:
        previous_image_link = collection["image"]
        if previous_image_link != "":
            previous_image_id = previous_image_link.split("/")[-1]
            image_collection.delete_one({"_id": ObjectId(previous_image_id)})
    image_id = image_collection.insert_one(
        {"data": image_data, "reference": ideo}
    ).inserted_id

    # Update the 'image' field in the appropriate collection
    if seller_collection.find_one({"_id": ideo, "email": encoded_email}):
        seller_collection.update_one(
            {"_id": ideo, "email": encoded_email},
            {"$set": {"image": "/get_image/" + str(image_id)}},
        )
    else:
        user_collection.update_one(
            {"_id": ideo, "email": encoded_email},
            {"$set": {"image": "/get_image/" + str(image_id)}},
        )

    return jsonify({"image_id": str(image_id)})


@app.route("/get_image/<image_id>", methods=["GET"])
def get_image(image_id):
    # Retrieve the image from the database
    image_data = image_collection.find_one({"_id": ObjectId(image_id)}) or slideshow_collection.find_one({"_id": ObjectId(image_id)})

    if image_data and "data" in image_data:
        # Serve the image data with appropriate content type
        return send_file(io.BytesIO(image_data["data"]), mimetype="image/jpeg")
    else:
        return jsonify({"error": "Image not found"})

    ##############################################################################################


@app.route("/update_data", methods=["POST"])
def update_data():
    data = request.get_json()
    encoded_email = data.get("email")
    # (encoded_email)

    text_area_value = data.get("textAreaValue")

    if encoded_email and text_area_value:
        developer = seller_collection.find_one({"email": encoded_email})

        if developer:
            seller_collection.update_one(
                {"email": encoded_email}, {"$set": {"about_self": text_area_value}}
            )
            print(f"home-c/{developer['_id']}/d")
            return jsonify(
                {
                    "message": "_{__xxx__%12*79)(56)[:]-++784kdd}_",
                    "ne": "deno",
                    "re": f"/home-c/{developer['_id']}/d",
                }
            )
        else:
            return jsonify({"error": "seller not found."})
    else:
        return jsonify({"error": "Invalid data."})


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Sorry! Resource not found"}), 404


@app.route("/home-c/<x>/<y>")
def home_c(x, y):
    if not check(request.cookies, "file"):
        return redirect(url_for("main"))

    elif (
        check(request.cookies, "file")
        and turbolancer_data_Security.decrypt(key, getkey(request.cookies)["ideo"]) != x
    ):
        return redirect(url_for("main"))
    user_data = user_collection.find_one(
        {"_id": x, "d": y}
    ) or seller_collection.find_one({"_id": x})

    if user_data:
        image = user_data["image"]
        name = user_data["name"]
        tag = user_data["tag"]
        user_id = x
        account = ["c", "d"]

        if "c" in account:
            return render_template(
                "clint-side-db.html",
                name=name,
                image=image,
                tag=tag,
                d=y,
                aclink=f"/account/{user_id}/{y}",
                c="c",
                allink=f"/dashboard/{user_id}/{y}",
            )

    return redirect(url_for("main"))


@app.route("/dashboard/<x>/<y>")
def dashboard(x, y):
    if not check(request.cookies, "file"):
        return redirect(url_for("main"))

    elif (
        check(request.cookies, "file")
        and turbolancer_data_Security.decrypt(key, getkey(request.cookies)["ideo"]) != x
    ):
        return redirect(url_for("main"))
    Seller_data = seller_collection.find_one({"_id": x, "d": y})

    if Seller_data:

        developer_data = get_seller_data(x)
        if developer_data:
            # Dummy data for developer_data
            developer_data["total_catalog_items"] = 125
            developer_data["total_projects"] = 42
            developer_data["rating"] = float(developer_data["rating"])
        if "d" in y:
            return render_template(
                "dashboard.html",
                **developer_data,
                aclink=f"/account/{x}/{y}",
                allink=f"/home-c/{x}/{y}",
                _id=x,
            )

    return redirect(url_for("main"))



@app.route("/catalogue/<x>/<y>", methods=["GET", "POST"])
def catalogue(x, y):
    if not check(request.cookies, "file"):
        return redirect(url_for("main"))
    elif (
        check(request.cookies, "file")
        and turbolancer_data_Security.decrypt(key, getkey(request.cookies)["ideo"]) != x
    ):
        return redirect(url_for("main"))

    Seller_data = seller_collection.find_one({"_id": x, "d": y})

    if Seller_data:
        if request.method == "GET":
            cat = list(catalogue_collection.find({"seller_id": x}))
            if cat:
                print(cat)
                return render_template("catalogue.html", **Seller_data, cat=cat)
            return render_template("catalogue.html", **Seller_data)

    if request.method == "POST":
        data = request.form.to_dict()
        uploaded_files =request.files.getlist('images')
        
        images = []
        for file in uploaded_files:
            binary_data = file.read()
            img_id = slideshow_collection.insert_one({'data': binary_data, 'reference': x}).inserted_id
            images.append("/get_image/" + str(img_id)) 
            print(images)
        catalogue_collection.insert_one({
            'title': data['title'],
            'seller_id': x,
            'category': data['category'],
            'description': data['description'],
            'tags': json.loads(data['tags']),
            'images': images,
            'inputLabels': json.loads(data['inputLabels']),
            'inputValues': json.loads(data['inputValues']),
            'date': datetime.date.today().strftime("%d/%m/%y"),
            'seller_image': Seller_data['image'],
            'seller_name': Seller_data['name'],
            'likes': 0,
            'orders': 0,
            'clicks': 0
        })

        return jsonify({"success": True})
        
"""
{'title': 'this is title',
 'category': 'Software Development',
   'description': '131231231232222222222222222222222222222222222222222222222222222222222222222222222222222222222222222',
     'tags': '["tag1","tag2","tag3","tag4","tag5","tag6","tag7","tag8"]',
       'images': '[object Blob],[object Blob]',
         'inputLabels': 'Price,Price,Price,Turnaround Time,Turnaround Time,Turnaround Time,Free Revisions,Free Revisions,Free Revisions',
           'inputValues': '123,234,345,2,5,7,8,9,4'}

          
"""


@app.route("/update_profile", methods=["POST"])
def update_profile():
    cookies = getkey(request.cookies)
    image_data = ""
    encoded_email = cookies.get("emalo")
    ideo = turbolancer_data_Security.decrypt(key, cookies.get("ideo"))
    check_result = check(request.cookies, "file")
    if not check_result:
        return redirect(url_for("main"))

    elif check_result and request.method == "POST":
        data = dict(request.form)
        file = request.files.get("image")
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
    if data.get("bir"):
        data["bir"] = turbolancer_data_Security.encrypt(key, data["bir"])
    if data.get("gan"):
        data["gan"] = turbolancer_data_Security.encrypt(key, data["gan"])
    return data


def get_collection(ideo, encoded_email):
    if seller_collection.find_one({"_id": ideo, "email": encoded_email}):
        return seller_collection
    else:
        return user_collection


def split_into_child_arrays(original_array):
    child_arrays = []
    for i in range(0, len(original_array), 3):
        child_array = original_array[i : i + 3]
        child_arrays.append(child_array)
    return child_arrays


@app.route("/delItem", methods=["POST"])
def delItem():
    cookies = getkey(request.cookies)
    encoded_email = cookies.get("emalo")
    ideo = turbolancer_data_Security.decrypt(key, cookies.get("ideo"))
    check_result = check(request.cookies, "file")
    if not check_result:
        return redirect(url_for("main"))

    elif check_result and request.method == "POST":
        data = request.form
        print(data["sk"])
        ud = seller_collection.find_one({"_id": ideo, "email": encoded_email})
        if ud and ud["sk"]:
            base: list = ud["sk"]
            for x in range(len(ud["sk"])):
                if base[x][0] == data["sk"]:
                    base.pop(x)
                    seller_collection.update_one(
                        {"_id": ideo, "email": encoded_email}, {"$set": {"sk": base}}
                    )
                    return jsonify({"success": True})
        return jsonify({"success": False})
    return jsonify({"success": False})


def update_database(collection, ideo, encoded_email, data):
    for field in ["bir", "gan", "name", "about_self", "sk"]:
        if field == "sk" and data.get(field):
            arr = data["sk"].split(",")
            arr = split_into_child_arrays(
                arr
            )  # Assuming this function is defined elsewhere
            ud = collection.find_one({"_id": ideo, "email": encoded_email})
            if ud and "sk" in ud:
                main_arr = ud["sk"]
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

                collection.update_one(
                    {"_id": ideo, "email": encoded_email}, {"$set": {"sk": main_arr}}
                )
        elif data.get(field):
            collection.update_one(
                {"_id": ideo, "email": encoded_email}, {"$set": {field: data[field]}}
            )


def delete_image(image_id):
    image_id = image_id.split("/")[-1]
    filter = {"_id": ObjectId(image_id)}

    result = image_collection.delete_one(filter)

    if result.deleted_count > 0:
        print(f"Image with ID {image_id} deleted successfully.")
    else:
        print(f"No image found with ID {image_id}.")


def get_user_dataA(user_id):
    user_data = user_collection.find_one({"_id": user_id})
    if user_data:
        email = turbolancer_data_Security.decrypt(key, user_data["email"])
        image = user_data["image"]
        name = user_data["name"]
        country = turbolancer_data_Security.decrypt(key, user_data["country"])
        ph = turbolancer_data_Security.decrypt(key, user_data["phone_number"])
        year = user_data["account_created_in"]
        method = user_data["payment_method"]
        bir = turbolancer_data_Security.decrypt(key, user_data["bir"])
        gan = turbolancer_data_Security.decrypt(key, user_data.get("gan", None)) or None
        tag = user_data["tag"] or None

        return {
            "name": name,
            "image": image,
            "email": email,
            "country": country,
            "ph": ph,
            "year": year,
            "bir": bir,
            "tag": tag,
            "gan": gan,
        }

    return None


def get_seller_data(developer_id):
    developer_data = seller_collection.find_one({"_id": developer_id})
    if developer_data:
        email = turbolancer_data_Security.decrypt(key, developer_data["email"])
        image = developer_data["image"]
        name = developer_data["name"]
        country = turbolancer_data_Security.decrypt(key, developer_data["country"])
        ph = turbolancer_data_Security.decrypt(key, developer_data["phone_number"])
        year = developer_data["account_created_in"]
        method = developer_data["payment_method"]
        grade = developer_data["grade"]
        rating = developer_data["rating"]
        about_self = developer_data["about_self"]
        tag = developer_data["tag"] or None
        sk = developer_data["sk"] or None
        earnings = developer_data["earnings"] or None
        bir = turbolancer_data_Security.decrypt(key, developer_data["bir"]) or None
        gan = (
            turbolancer_data_Security.decrypt(key, developer_data.get("gan", None))
            or None
        )
        length = len(sk) if sk else 0
        return {
            "name": name,
            "image": image,
            "email": email,
            "country": country,
            "ph": ph,
            "year": year,
            "about_self": about_self,
            "rating": rating,
            "grade": grade,
            "tag": tag,
            "bir": bir,
            "gan": gan,
            "sk": sk,
            "earnings": earnings,
            "len": length,
        }
    return None


@app.route("/account/<x>/<y>")
def account(x, y):

    if not check(request.cookies, "file"):
        return redirect(url_for("main"))

    decrypted_x = turbolancer_data_Security.decrypt(
        key, getkey(request.cookies)["ideo"]
    )

    if check(request.cookies, "file") and decrypted_x != x:
        ud = get_user_dataA(x) or get_seller_data(x)
        lud = get_user_dataA(decrypted_x) or get_seller_data(decrypted_x)

        if ud["ph"] == lud["ph"]:

            if y in ["c", "d"]:
                if y == "c":
                    user_data = get_user_dataA(x)
                    if user_data:
                        # Dummy data for user_data
                        user_data["total_earnings"] = "$12,345"
                        user_data["total_catalog_items"] = 125
                        user_data["total_projects"] = 42
                        user_data["user_rating"] = 4.8
                        return render_template(
                            "profile_page.html",
                            **user_data,
                        )
                elif y == "d":
                    developer_data = get_seller_data(x)
                    if developer_data:
                        # Dummy data for developer_data
                        developer_data["total_catalog_items"] = 125
                        developer_data["total_projects"] = 42
                        developer_data["rating"] = float(developer_data["rating"])

                        return render_template(
                            "profile_page.html", **developer_data, d="avail"
                        )

                    return redirect(url_for("main"))
        return redirect(url_for("main"))

    if y in ["c", "d"]:
        if y == "c":
            user_data = get_user_dataA(x)
            if user_data:
                # Dummy data for user_data
                user_data["total_earnings"] = "$12,345"
                user_data["total_catalog_items"] = 125
                user_data["total_projects"] = 42
                user_data["user_rating"] = 4.8
                return render_template(
                    "profile_page.html", **user_data, x="yes", c="yes"
                )
        elif y == "d":
            developer_data = get_seller_data(x)
            if developer_data:
                # Dummy data for developer_data
                developer_data["total_catalog_items"] = 125
                developer_data["total_projects"] = 42
                developer_data["rating"] = float(developer_data["rating"])

                return render_template(
                    "profile_page.html", **developer_data, d="avail", x="yes"
                )

            return redirect(url_for("main"))

    return redirect(url_for("main"))


@app.errorhandler(404)
def page_not_found(error):
    return "404"


@app.route("/upjobpage")
def page():
    return render_template("upload_job.html")


@app.route("/getserved")
def get_searved():
    return render_template("get_served.html")


@app.route("/proj")
def proj():
    return render_template("project.html")


def remove_word_without_space(text, word):
    pattern = rf"\b{word}(?!\s)"
    return re.sub(pattern, "", text)


def remove_first_uppercase(s):
    if len(s) >= 2 and s[:2].isupper():
        return s[1:]
    return s


@app.route("/rephrase_text", methods=["POST"])
def rephrase():
    data = request.get_json()
    input_text = data.get("text")
    main = data.get("main")
    print(main)
    print(input_text)
    response = TurboLancer_RePhrase_text.do(input_text, main)

    response = response.replace("\n", "")
    response = response.replace("]]", "")
    response = response.replace("[[", "")
    response = response.replace("[[[", "")
    response = response.replace("]]]", "")
    response = response.replace("IIPlease", "")
    response = response.replace("IPlease", "")
    response = response.replace("IIIPlease", "")
    response = response.replace("IIIIPlease", "")
    response = response.replace("TheI", "I")
    response = response.replace("I I", "I")
    response = response.replace("II", "I")
    response = response.replace("BasedBased on", "Based")
    response = response.replace("BasedBased", "")
    response = response.replace("Based the", "Based on the")
    response = response.replace("the client form", "this project")
    response = response.replace("is is", "is")
    response = response.replace("ForFor", "For")
    response = response.replace("BasedI", "I")
    response = response.replace("[IBased", "Based")
    response = remove_word_without_space(response, "Based")
    response = remove_word_without_space(response, "The")
    response = remove_word_without_space(response, "For")
    # response = remove_first_uppercase(response)

    print(response)
    return jsonify(text=response)


if __name__ == "__main__":
    socketio.run(app, debug=True)
