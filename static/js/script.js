// Initializes card editing.  Used when the page is first loaded and
// whenever the cards are refreshed.  Assigns event handlers.
var refreshImagesURL;
var photo_edit_forms;
var btn_refresh = document.getElementById('refresh');
var img_container = document.getElementById('img_container');
var edits = {};  // Will store edits for each loaded card

// REMOVE THIS
var btnTest = document.getElementById('btn_test');
btnTest.addEventListener('click', () =>{
  fetch(`test`, {
    method: "POST",
    body: JSON.stringify(edits),
    headers: {
      'content-type': 'application/json'
    }
  });
})

function init(imagesURL) {
  btn_refresh.addEventListener('click', refresh_images)
  refreshImagesURL = imagesURL
  // Add event listeners to card editing forms
  setup_card_edit_forms();
}


function refresh_images() {
  img_container.innerHTML = '<h1>Refreshing Images...</h1>';

  let url = `${refreshImagesURL}/json`;
  fetch(url)
    .then(response => response.json())
    .then(data => img_container.innerHTML = data.html)
    .finally(() => setup_card_edit_forms());
}


function get_card_data(id, variable) {
  let card = document.getElementById(id);

  data = {
    'img_url': card.dataset.imgUrl,
    'img_filename': card.dataset.imgUrl.split('/')[3]
  }

  if (typeof variable == 'undefined') {
    return data
  }
  else {
    return data[variable]
  }
}


function setup_card_edit_forms() {
  // Add event listeners for card edit forms
  photo_edit_forms = document.getElementsByClassName('card_edit');
  for (let i = 0; i < photo_edit_forms.length; i++) {
    let current_form = photo_edit_forms[i];
    let current_id = current_form.dataset.id;
    let current_img_url = current_form.dataset.imgUrl;
    let current_text = current_form.dataset.nameText;
    let current_background_color = '#FFFFFF';
    let current_font = '';
    let current_font_color = '#000000';
    let current_crop = 'auto';


    // Set up edits entry
    edits[current_id] = {
      'img_url': current_img_url,
      'text': current_text,
      'background_color': current_background_color,
      'font': current_font,
      'font_color': current_font_color,
      'crop': current_crop,
      'rotate_clockwise': false,
      'rotate_counterclockwise': false
    }

    // Rename card caption
    current_form.addEventListener('submit', rename_photo);

    // Delete image
    let btn_delete = document.getElementById(`${current_id}-delete`);
    btn_delete.addEventListener('click', () => delete_photo(get_card_data(current_id, 'img_filename')));
  }
}


function delete_photo(imgUrl) {
  url = `tools/delete/${imgUrl}`;
  fetch(url)
    .then(() => refresh_images());
}


function figure_this_out(test) {
  console.log(test);
}


function rename_photo(e) {
  e.preventDefault();
  let id = e.target.id;
  let input_txt_box = document.getElementById(`${id}_txt_name`);
  edits[id]['text'] = input_txt_box.value;
  edit_photo(e);
}


function reload_img(img, img_url, input_txt_box, text) {
  fetch(img_url, { cache: "reload" })
    .then(r => r.json())
    .then(data => {
      console.log(data)
      new_filename = data.new_filename;
      img.src = new_filename;
      input_txt_box.value = text;
    });
}

function edit_photo(e) {
  e.preventDefault();
  let id = e.target.dataset.id;
  let card_edits = edits[id];  // Load edits for current card

  let img_url = card_edits['img_url'];
  let filename = img_url.split('/')[3];

  let input_txt_box = document.getElementById(`${id}_txt_name`);
  let text = card_edits['text'];

  let btn_download = document.getElementById(`${id}-download`);

  let img = document.getElementById(`img-${id}`);

  let url = `/tools/edit_card`;

  fetch(url, {
    method: "POST",
    body: JSON.stringify(card_edits),
    headers: {
      'content-type': 'application/json'
    }
  })
    .then(response => response.json())
    .then(data => {
      // set new img url
      new_img_url = data.new_filename;
      e.target.dataset.imgUrl = new_img_url;
      edits[id].img_url = new_img_url;

      // reset card preview image
      img.src = new_img_url;

      // reset edit name text
      input_txt_box.value = text;

      // update download link
      btn_download.href = new_img_url;
    });
}

