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
      const card = generateCard(file, "odkaz", "nejaky text");
      container.appendChild(card);
    });
  },
});

function generateCard(imageSrc, linkHref, textSrc) {
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
  link.href = linkHref;
  link.className = "btn btn-primary stretched-link";
  link.textContent = "Open Stream";

  const text = document.createElement("p");
  text.className = "card-text";
  text.textContent = textSrc;

  cardBody.appendChild(text);
  cardBody.appendChild(link);
  card.appendChild(img);
  card.appendChild(cardBody);

  return card;
}
