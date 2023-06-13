// Initializes card editing.  Used when the page is first loaded and
// whenever the cards are refreshed.  Assigns event handlers.
var refreshImagesURL;
var photo_edit_forms;
var btn_refresh = document.getElementById('refresh');
var img_container = document.getElementById('img_container');


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

function rename_photo(e) {
  e.preventDefault();
  var img_url = e.target.dataset.imgUrl;
  var filename = img_url.split('/')[3];

  var input_txt_box = document.getElementById(`${e.target.id}_txt_name`);
  var text = input_txt_box.value;

  var btn_download = document.getElementById(`${e.target.id}-download`);

  var img = document.getElementById(`img-${e.target.id}`);

  var url = `/tools/update_text/${filename}/${text}`;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      // set new img url
      new_img_url = data.new_filename;
      e.target.dataset.imgUrl = new_img_url;

      // reset card preview image
      img.src = new_img_url;

      // reset edit name text
      input_txt_box.value = text;

      // update download link
      btn_download.href = new_img_url;
    });
}

