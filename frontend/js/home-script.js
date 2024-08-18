const button1 = document.getElementById('button1');
const button2 = document.getElementById('button2');

button1.addEventListener('click', function () {
  $('#ModalOne').modal('show');
});

button2.addEventListener('click', function () {
  $('#ModalTwo').modal('show');
});
