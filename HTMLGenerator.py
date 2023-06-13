from time import sleep

def get_card_html(id, img_url):
    print('get_card_html', id, img_url)
    filename = img_url.split('/')[-1]  # Get just the file name from image url
    name = filename.split('.')[0]  # Remove extension
    name = name.split('~')[1]  # Remove card~ prefix
    name = name.replace('_', ' ')
    return f"""
        <div class="card_edit" data-id="{id}" data-img-url="{img_url}">
            <img id="img-{id}" src="{img_url}" class="card_preview">

            <form id="{id}" data-img-url="{img_url}">
                <label for="{id}_txt_name">Edit Display Name:</label><br>
                <input type="text" id="{id}_txt_name" name="{id}_txt_name" value="{name}"><br>
                <input type="submit" value="Submit">
            </form>
            <div type="button" id="{id}-delete" data-id="{id}" data-img-url="{img_url}">Delete</div>
            <br>
            <button type="button" id="{id}-rotate-left" data-id="{id}" data-img-url="{img_url}">Rotate Left</button>
            <button type="button" id="{id}-rotate-right" data-id="{id}" data-img-url="{img_url}">Rotate Right</button>
            <br>
            <button type="button" id="{id}-auto-crop" data-id="{id}" data-img-url="{img_url}">Auto Cropping</button>
            <button type="button" id="{id}-reset-crop" data-id="{id}" data-img-url="{img_url}">Reset Cropping</button>
            <button type="button" id="{id}-manual-crop" data-id="{id}" data-img-url="{img_url}">Manual Cropping</button>
            <br>
            <a id="{id}-download" data-id="{id}" href="{img_url}" download>Download</a>        
            <hr>
        </div>
    """