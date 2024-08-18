document.getElementById('numberSongsForm').addEventListener('submit', function (event) {
  event.preventDefault();
  const numberSongs = document.getElementById('numberSongs_input').value;

  window.location.href = `talentshow_form.html?numberSongs=${numberSongs}`;
});
