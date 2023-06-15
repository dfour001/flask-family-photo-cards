from time import sleep

def get_card_html(id, img_url):
    print('get_card_html', id, img_url)
    filename = img_url.split('/')[-1]  # Get just the file name from image url
    name = filename.split('.')[0]  # Remove extension
    name = name.split('~')[1]  # Remove card~ prefix
    name = name.replace('_', ' ')
    return f"""
        <div class="card_edit mb-6" data-id="{id}" data-img-url="{img_url}">
            <div class="columns">
                <div class="column has-text-centered">
                    <img id="img-{id}" src="{img_url}" class="card_preview">
                </div>
                <div class="column">
                    <form id="{id}" data-img-url="{img_url}">
                        <label class="label">Change image text</label>
                        <div class="field has-addons">
                            <div class="control">
                                <input type="text" id="{id}_txt_name" class="input" name="{id}_txt_name" value="{name}">
                            </div>
                            <div class="control">
                                <input type="submit" class="button is-link" value="Update">
                            </div>
                        </div>
                    </form>
                    <br>
                    <label class="label">Rotate Image</label>
                    <div class="field has-addons">
                        <div class="control">
                            <div class="button is-link" id="{id}-rotate-left" data-id="{id}"><span class="icon iconify" data-icon="carbon:rotate-counterclockwise-alt"></span></div>
                        </div>
                        <div class="control">
                            <div class="button is-link" id="{id}-rotate-right" data-id="{id}"><span class="icon iconify" data-icon="carbon:rotate-clockwise-alt"></span></div>
                        </div>
                    </div>
                    <label class="label">Cropping</label>
                    <div class="field has-addons">
                        <div class="control">                        
                            <button class="button is-link is-selected" id="{id}-auto-crop" data-id="{id}"><span class="icon iconify" data-icon="fluent:crop-sparkle-24-regular"></span> <span>Auto</span></button>
                        </div>
                        <div class="control">
                            <button class="button" id="{id}-reset-crop" data-id="{id}"><span>No Cropping</span></button>
                        </div>
                        <div class="control">
                            <button class="button" id="{id}-manual-crop" data-id="{id}"><span class="icon iconify" data-icon="fluent:crop-16-filled"></span> <span>Manual</span></button>
                        </div>
                    </div>
                    <hr>
                    <div class="buttons is-grouped">
                        <div class="control">
                            <button id="{id}-delete" class="button is-danger is-light" data-id="{id}"><span class="icon iconify" data-icon="typcn:delete"></span> <span>Delete</span></button>
                        </div>
                        <div class="control">
                            <a id="{id}-download" data-id="{id}" href="{img_url}" class="button is-success is-light" download><span class="icon iconify" data-icon="ic:baseline-download"></span> <span>Download</span></a>
                        </div>
                    </div>
                </div>
            </div>      
        </div>
    """