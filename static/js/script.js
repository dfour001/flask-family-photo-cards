// Initializes card editing.  Used when the page is first loaded and
// whenever the cards are refreshed.  Assigns event handlers.
var refreshImagesURL;
var photo_edit_forms;
var btn_refresh = document.getElementById('refresh');
var img_container = document.getElementById('img_container');
var edits = {};  // Will store edits for each loaded card

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

    // Rotate clockwise
    let btn_rotate_clockwise = document.getElementById(`${current_id}-rotate-clockwise`);
    btn_rotate_clockwise.addEventListener('click', () => {
      btn_rotate_clockwise.classList.add('is-loading');
      edits[current_id].rotate_clockwise = true;
      let current_form = document.getElementById(current_id);
      edit_photo(undefined, current_id);
    });

    // Rotate counterclockwise
    let btn_rotate_counterclockwise = document.getElementById(`${current_id}-rotate-counterclockwise`);
    btn_rotate_counterclockwise.addEventListener('click', () => {
      btn_rotate_counterclockwise.classList.add('is-loading');
      edits[current_id].rotate_counterclockwise = true;
      edit_photo(undefined, current_id);
    });

    // Cropping buttons
    let btn_auto_crop = document.getElementById(`${current_id}-auto-crop`);
    let btn_no_crop = document.getElementById(`${current_id}-reset-crop`);
    let btn_manual_crop = document.getElementById(`${current_id}-manual-crop`);

    // Auto crop
    btn_auto_crop.addEventListener('click', () => {
      btn_auto_crop.classList.add('is-loading', 'is-link', 'is-selected');
      btn_no_crop.classList.remove('is-link', 'is-selected');
      btn_manual_crop.classList.remove('is-link', 'is-selected');
      edits[current_id].crop = 'auto';
      edit_photo(undefined, current_id);
    })

    // No crop
    btn_no_crop.addEventListener('click', () => {
      btn_no_crop.classList.add('is-loading', 'is-link', 'is-selected');
      btn_auto_crop.classList.remove('is-link', 'is-selected');
      btn_manual_crop.classList.remove('is-link', 'is-selected');
      edits[current_id].crop = 'no';
      edit_photo(undefined, current_id);
    })

    // Manual crop
    btn_manual_crop.addEventListener('click', () => {
      btn_manual_crop.classList.add('is-loading', 'is-link', 'is-selected');
      btn_auto_crop.classList.remove('is-link', 'is-selected');
      btn_no_crop.classList.remove('is-link', 'is-selected');
      edits[current_id].crop = 'manual';
      edit_photo(undefined, current_id);
    })

    // Image modal
    let img_card = document.getElementById(`img-${current_id}`)
    img_card.addEventListener('click', () => {
      let img_url = img_card.src;
      let modal_img = document.getElementById('modal-image');
      modal_img.src = img_url;
      openModal();
    })


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
      new_filename = data.new_filename;
      img.src = new_filename;
      input_txt_box.value = text;
    });
}

function edit_photo(e, id) {
  if (typeof e !== 'undefined') {
    e.preventDefault();
    id = e.target.dataset.id;
  }
    
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
      let card = document.getElementById(`${id}_card-edit`);
      card.dataset.imgUrl = new_img_url;

      // update edits dict
      edits[id].img_url = new_img_url;
      edits[id]['rotate_clockwise'] = false;
      edits[id]['rotate_counterclockwise'] = false;

      // reset card preview image
      img.src = new_img_url;

      // reset edit name text
      input_txt_box.value = text;

      // update download link
      btn_download.href = new_img_url;

      // reset loading animations
      loading_elements = document.getElementsByClassName('is-loading');
      for (let i = 0; i < loading_elements.length; i++) {
        loading_elements[i].classList.remove('is-loading');
      }
    });
}


// Functions to open and close a modal
function openModal() {
  $el = document.getElementsByClassName('modal')[0]
  $el.classList.add('is-active');
}

function closeModal() {
  $el = document.getElementsByClassName('modal')[0]
  $el.classList.remove('is-active');
}

function closeAllModals() {
  (document.querySelectorAll('.modal') || []).forEach(($modal) => {
    closeModal($modal);
  });
}

// Add a click event on various child elements to close the parent modal
(document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
  const $target = $close.closest('.modal');

  $close.addEventListener('click', () => {
    closeModal($target);
  });
});

// Add a keyboard event to close all modals
document.addEventListener('keydown', (event) => {
  const e = event || window.event;

  if (e.keyCode === 27) { // Escape key
    closeAllModals();
  }
});