import imghdr
import os
import json
import logging

from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory, session
from werkzeug.utils import secure_filename
import uuid

from HTMLGenerator import get_card_html
from MakeCards import create_card, get_unique_name

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG) # Set the debug level here
fileHandler = logging.FileHandler(f'my.log', mode='w')
log.addHandler(fileHandler)


app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'files'
app.config['SECRET_KEY'] = 'you-will-never-guess'

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


def get_id():
    return str(uuid.uuid4())



@app.route('/')
def index():
    """ Loads home screen where the user can upload and edit imgs """

    # Prepare user id
    if 'id' not in session:
        session['id'] = get_id()
    
    id = session['id']

    # Get photo editing html
    imgs = get_all_imgs()

    return render_template('index.html', imgs=imgs, id=id)


@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']

    # Check that filename is safe
    filename = secure_filename(uploaded_file.filename)
    # Check for supported file extension
    if filename != '':
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
            abort(400)
    
    # Get user folder
    user_folder_path = os.path.join(app.config['UPLOAD_PATH'], session['id'])
    if not os.path.exists(user_folder_path):
        os.mkdir(user_folder_path)
    
    # Save file
    filepath = os.path.join(user_folder_path, filename)
    uploaded_file.save(filepath)
    
    # Create card
    cardPath = os.path.join(user_folder_path, f'card~{filename}')
    cardText = filename.split('.')[0].replace('_',' ')
    create_card(filepath, cardText, cardPath)
    
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/files/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/get_img/<id>/<filename>')
def get_img(id, filename):
    path = os.path.join(app.config['UPLOAD_PATH'], id)
    return send_from_directory(path, filename)


@app.route('/html/get_all_imgs')
@app.route('/html/get_all_imgs/<json>')
def get_all_imgs(json=False):
    """ Loads all of the pictures within the user's folder and returns edit 
        image cards for each.  If folder does not exist or folder is empty,
        returns blank html. 
        
        Set json=True to return as json, otherwise returns as html string """
    
    user_folder_path = os.path.join(app.config['UPLOAD_PATH'], session['id'])
    
    # Default output until files are verified to exist
    output = {'html': '<h1>No files to display</h1>'} if json else '<h1>No files to display</h1>'

    # Check if folder does not exist
    if not os.path.exists(user_folder_path):
        return output
    
    # Get images
    imgs = [img for img in os.listdir(user_folder_path) if 'card~' in img]
    if len(imgs) == 0:
        return output

    # Generate html
    output = ""
    for i, img in enumerate(imgs):
        img_path = url_for('get_img', id=session['id'], filename=img)
        output += get_card_html(i, os.path.join(user_folder_path, img_path))
    
    if json:
        return {'html': output}
    
    return output

@app.route('/tools/delete/<filename>')
def delete(filename):
    """ Deletes the input filename """
    user_folder_path = os.path.join(app.config['UPLOAD_PATH'], session['id'])
    file_path = os.path.join(user_folder_path, filename)
    os.remove(file_path)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/tools/update_text/<filename>/<text>')
def update_text(filename, text):
    """ Updates the text under the image on the card """
    log.debug(f'update_text({filename}, {text})')

    ori_filename = filename.split('~')[1]
    user_folder_path = os.path.join(app.config['UPLOAD_PATH'], session['id'])
    log.debug(f'    user_folder_path: {user_folder_path}')
    
    # Path to original file that user uploaded
    oriPath = os.path.join(user_folder_path, ori_filename)
    log.debug(f'    oriPath: {oriPath}')

    # Path to the currently displayed card
    cardPath = os.path.join(user_folder_path, filename)
    log.debug(f'    cardPath: {cardPath}')

    new_filename = get_unique_name(filename, os.listdir(user_folder_path))
    new_cardPath = os.path.join(user_folder_path, new_filename)
    log.debug(f'    new_filename: {new_filename}')
    log.debug(f'    new_cardPath: {new_cardPath}')
    create_card(oriPath, text, new_cardPath)
    
    # Delete previous version of card
    os.remove(cardPath)

    new_img_path = url_for('get_img', id=session['id'], filename=new_filename)
    return_data = {'success':True, 'new_filename':new_img_path}
    log.debug(f'Done - returning:\n    {return_data}\n\n')

    return json.dumps(return_data), 200, {'ContentType':'application/json'}


@app.route('/tools/edit_card', methods=['POST'])
def edit_card():
    """ Updates the card based on changes sent in json format.  Sample input:
     
        {
            'img_url': '/get_img/15b989db-608b-434c-9c2f-c7c1cd3e8405/1_card~PXL_20230617_185630750.jpg', 
            'text': 'Nadia',
            'background_color': '#FFFFFF',
            'font': '',
            'font_color': '#000000',
            'crop': 'auto',
            'rotate_clockwise': False,
            'rotate_counterclockwise': False
        }        
    """
    log.debug(f'edit_card())')
    edits = request.get_json()
    log.debug(f'Edits:\n{edits}')
    img_url = edits['img_url']
    filename = img_url.split('/')[-1]
    ori_filename = filename.split('~')[1]
    text = edits['text']
    rotate_clockwise = edits['rotate_clockwise']
    rotate_counterclockwise = edits['rotate_counterclockwise']
    crop = edits['crop']

    user_folder_path = os.path.join(app.config['UPLOAD_PATH'], session['id'])
    log.debug(f'    user_folder_path: {user_folder_path}')
    
    # Path to original file that user uploaded
    oriPath = os.path.join(user_folder_path, ori_filename)
    log.debug(f'    oriPath: {oriPath}')

    # Path to the currently displayed card
    cardPath = os.path.join(user_folder_path, filename)
    log.debug(f'    cardPath: {cardPath}')

    new_filename = get_unique_name(filename, os.listdir(user_folder_path))
    new_cardPath = os.path.join(user_folder_path, new_filename)
    log.debug(f'    new_filename: {new_filename}')
    log.debug(f'    new_cardPath: {new_cardPath}')
    create_card(oriPath, text, new_cardPath)
    
    # Delete previous version of card
    os.remove(cardPath)

    new_img_path = url_for('get_img', id=session['id'], filename=new_filename)
    return_data = {'success':True, 'new_filename':new_img_path}
    log.debug(f'Done - returning:\n    {return_data}\n\n')

    return json.dumps(return_data), 200, {'ContentType':'application/json'}


@app.route('/test', methods=['POST'])
def test():
    data = request.get_json()

    print(type(data))

    return_data = {'success':True}
    return json.dumps(return_data), 200, {'ContentType':'application/json'}