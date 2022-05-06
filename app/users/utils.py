import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail

def save_picture(form_picture):
    # let's convert the file name to a random name so that
    # two images with same name won't override
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # because we don't need file name
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # let's resize our picture
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # let's save the resized image
    i.save(picture_path)
    return picture_fn # return the picture filename so that we can save it to database

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _exteral=True)}

If you did not make this request then simply ignore this email and no changes will be made
"""
    mail.send(msg)
