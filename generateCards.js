const container = document.getElementById("cards");

const files = [];


var xhr = new XMLHttpRequest();
xhr.open("GET", "/thumbnails", true);
xhr.responseType = "document";
xhr.onload = () => {
  if (xhr.status === 200) {
    var elements = xhr.response.getElementsByTagName("a");
    for (x of elements) {
      if (x.href.match(/_thumbnail001\.jpg$/)) {
        const fileName = x.href.match(/[^/]+(?=\.[^/]+$)/).toString();
        const card = generateCard(x.href, fileName);
        container.appendChild(card);
        const modal = generateModal(fileName, fileName, x.href);
        container.appendChild(modal);

// videojs(fileName);

      }
    }
  } else {
    alert("Request failed. Returned status of " + xhr.status);
  }
};
xhr.send();

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
  link.setAttribute("data-bs-target", "#" + textSrc);

  const text = document.createElement("p");
  text.className = "card-text";
  text.textContent = textSrc.replace(/_thumbnail001/g, "");
  cardBody.appendChild(text);
  cardBody.appendChild(link);
  card.appendChild(img);
  card.appendChild(cardBody);

  return card;
}

function generateModal(textSrc, streamSrc, imgSrc) {
  // Create the modal container div
  const modal = document.createElement("div");
  modal.className = "modal fade";
  modal.id = textSrc;
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
  video.id = textSrc;
  video.className = "video-js";
  video.controls = true;
  video.preload = "auto";
  video.width = 426;
  video.height = 240;
  video.poster = imgSrc;
  video.setAttribute("data-setup", "{}");

  // Create the  <source> element
  const sourceMp4 = document.createElement("source");
  sourceMp4.src = "http://localhost/streams/" + streamSrc.replace(/_thumbnail001/g, ".m3u8");
  sourceMp4.type = "application/x-mpegURL";

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

  // Add the download changes button to the footer
  const downloadChangeButton = document.createElement("button");
  downloadChangeButton.type = "button";
  downloadChangeButton.className = "btn btn-primary";
  downloadChangeButton.textContent = "Download stream";

  // Append buttons to modal-footer
  modalFooter.appendChild(closeFooterButton);
  modalFooter.appendChild(downloadChangeButton);

  // Assemble the modal structure
  modalContent.appendChild(modalHeader);
  modalContent.appendChild(modalBody);
  modalContent.appendChild(modalFooter);
  modalDialog.appendChild(modalContent);
  modal.appendChild(modalDialog);

  // Append the modal to the body
  return modal;
}

setTimeout(getVideos,5000 );



function getVideos(){
  console.log("hi");
  const videoElements = document.querySelectorAll('video');
  videoElements.forEach(video => {
    console.log(video.id || 'No ID');
videojs(video, {liveui: true});
  });
}
