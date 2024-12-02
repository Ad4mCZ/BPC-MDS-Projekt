const container = document.getElementById("cards");

const files = [];

var dir = "/media";
var fileextension = ".png";

$.ajax({
  //This will retrieve the contents of the folder if the folder is configured as 'browsable'
  url: dir,
  success: function (data) {
    // List all png file names in the page
    $(data)
      //find ahref elements
      .find("a:contains(" + fileextension + ")")
      //strip the url and keep just the filename
      .each(function () {
        var filename = this.href
          .replace(window.location.host, "")
          .replace("http:///", "");
        //append the array
        files.push(filename);
      });
    //generate cards using the data in the array
    files.forEach((file) => {
      const card = generateCard(file, file);
      container.appendChild(card);
      const modal = generateModal(file, "strem");
      container.appendChild(modal);
    });
  },
});

function generateCard(imageSrc, textSrc) {
  const card = document.createElement("div");
  card.className = "card";
  card.style.width = "18rem";

  const img = document.createElement("img");
  img.className = "card-img-top";
  img.src = imageSrc;
  img.alt = "Card image cap";

  const cardBody = document.createElement("div");
  cardBody.className = "card-body";

  const link = document.createElement("a");
  link.className = "btn btn-primary stretched-link";
  link.textContent = "Open Stream";
  link.setAttribute("type", "button");
  link.setAttribute("data-bs-toggle", "modal");
  link.setAttribute("data-bs-target", "#exampleModal");

  const text = document.createElement("p");
  text.className = "card-text";
  text.textContent = textSrc;

  cardBody.appendChild(text);
  cardBody.appendChild(link);
  card.appendChild(img);
  card.appendChild(cardBody);

  return card;
}

function generateModal(textSrc, streamSrc) {
  // Create the modal container div
  const modal = document.createElement("div");
  modal.className = "modal fade";
  modal.id = "exampleModal";
  modal.tabIndex = "-1";
  modal.setAttribute("aria-labelledby", "exampleModalLabel");
  modal.setAttribute("aria-hidden", "true");

  // Create the modal-dialog div
  const modalDialog = document.createElement("div");
  modalDialog.className = "modal-dialog";

  // Create the modal-content div
  const modalContent = document.createElement("div");
  modalContent.className = "modal-content";

  // Create the modal-header div
  const modalHeader = document.createElement("div");
  modalHeader.className = "modal-header";

  // Add the modal title
  const modalTitle = document.createElement("h1");
  modalTitle.className = "modal-title fs-5";
  modalTitle.id = "exampleModalLabel";
  modalTitle.textContent = textSrc;

  // Add the close button
  const closeButton = document.createElement("button");
  closeButton.type = "button";
  closeButton.className = "btn-close";
  closeButton.setAttribute("data-bs-dismiss", "modal");
  closeButton.setAttribute("aria-label", "Close");

  // Append title and close button to modal-header
  modalHeader.appendChild(modalTitle);
  modalHeader.appendChild(closeButton);

  // Create the modal-body div
  const modalBody = document.createElement("div");
  modalBody.className = "modal-body";

  // Create the <video> element
  const video = document.createElement("video");
  video.id = "my-video";
  video.className = "video-js";
  video.controls = true;
  video.preload = "auto";
  video.width = 426;
  video.height = 240;
  video.poster = "MY_VIDEO_POSTER.jpg";
  video.setAttribute("data-setup", "{}");

  // Create the  <source> element
  const sourceMp4 = document.createElement("source");
  sourceMp4.src = "MY_VIDEO.mp4";
  sourceMp4.type = "video/mp4";

  // Create the fallback <p> element
  const fallbackText = document.createElement("p");
  fallbackText.className = "vjs-no-js";
  fallbackText.innerHTML =
    'To view this video please enable JavaScript, and consider upgrading to a web browser that <a href="https://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a>.';

  // Append the sources and fallback text to the video element
  video.appendChild(sourceMp4);
  video.appendChild(fallbackText);
  // Append the video to the modal body
  modalBody.appendChild(video);

  // Create the modal-footer div
  const modalFooter = document.createElement("div");
  modalFooter.className = "modal-footer";

  // Add the Close button to the footer
  const closeFooterButton = document.createElement("button");
  closeFooterButton.type = "button";
  closeFooterButton.className = "btn btn-secondary";
  closeFooterButton.setAttribute("data-bs-dismiss", "modal");
  closeFooterButton.textContent = "Close";

  // Add the Save changes button to the footer
  const saveChangesButton = document.createElement("button");
  saveChangesButton.type = "button";
  saveChangesButton.className = "btn btn-primary";
  saveChangesButton.textContent = "Save changes";

  // Append buttons to modal-footer
  modalFooter.appendChild(closeFooterButton);
  modalFooter.appendChild(saveChangesButton);

  // Assemble the modal structure
  modalContent.appendChild(modalHeader);
  modalContent.appendChild(modalBody);
  modalContent.appendChild(modalFooter);
  modalDialog.appendChild(modalContent);
  modal.appendChild(modalDialog);

  // Append the modal to the body
  return modal;
}
