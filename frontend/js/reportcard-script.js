document.addEventListener('DOMContentLoaded', function () {
  let currentPage = 1;
  const totalPages = 3;
  const loadingGif = document.getElementById('loading');
  const loadingWrapper = document.getElementById('loading-wrapper');
  const formPic = document.getElementById('folderForm');
  const spotify_urlResult = document.getElementById('spotify_urlResult');
  const songForm = document.getElementById('songForm');
  const titleResult = document.getElementById('titleResult');
  const artistResult = document.getElementById('artistResult');
  const pictureResult = document.getElementById('pictureResult');
  const release_dateResult = document.getElementById('release_dateResult');
  const popularityResult = document.getElementById('popularityResult');
  const danceabilityResult = document.getElementById('danceabilityResult');
  const energyResult = document.getElementById('energyResult');
  const loudnessResult = document.getElementById('loudnessResult');
  const speechinessResult = document.getElementById('speechinessResult');
  const acousticnessResult = document.getElementById('acousticnessResult');
  const instrumentalnessResult = document.getElementById('instrumentalnessResult');
  const livenessResult = document.getElementById('livenessResult');
  const valenceResult = document.getElementById('valenceResult');
  const tempoResult = document.getElementById('tempoResult');
  const spot_tagsResult = document.getElementById('spot_tagsResult');
  const last_urlResult = document.getElementById('last_urlResult');
  const listenersResult = document.getElementById('listenersResult');
  const playcountResult = document.getElementById('playcountResult');
  const last_tagsResult = document.getElementById('last_tagsResult');
  const youtube_urlResult = document.getElementById('youtube_urlResult');
  const commentsResult = document.getElementById('commentsResult');
  const likesResult = document.getElementById('likesResult');
  const viewsResult = document.getElementById('viewsResult');
  const resultModal = $('#resultModal');

  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  songForm.addEventListener('submit', function (event) {
    event.preventDefault();
    loadingGif.style.display = 'flex';
    loadingWrapper.style.display = 'flex';
    formPic.style.display = 'none';
    songForm.style.display = 'none';

    const song_name = document.getElementById('song_input').value;
    const artist_name = document.getElementById('artist_input').value;

    fetch('https://popacademy-broq2hqh2-stevens-projects-7f537890.vercel.app/process', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ song_name, artist_name }),
    })
      .then(response => response.json())
      .then(data => {
        titleResult.textContent = `${data.titley}`;
        artistResult.textContent = `${data.artisty}`;
        pictureResult.src = `${data.picy}`;
        release_dateResult.textContent = `${data.release_datey}`;

        const link = document.createElement('a');
        link.href = `${data.spotify_urly}`;
        link.textContent = 'Listen on Spotify';
        link.target = '_blank';
        spotify_urlResult.innerHTML = '';
        spotify_urlResult.appendChild(link);

        popularityResult.textContent = ` ${data.popularityy}`;
        danceabilityResult.textContent = `${data.danceabilityy}`;
        energyResult.textContent = `${data.energyy}`;
        loudnessResult.textContent = `${data.loudnessy}`;
        speechinessResult.textContent = `${data.speechinessy}`;
        acousticnessResult.textContent = `${data.acousticnessy}`;
        instrumentalnessResult.textContent = `${data.instrumentalnessy}`;
        livenessResult.textContent = `${data.livenessy}`;
        valenceResult.textContent = `${data.valencey}`;
        tempoResult.textContent = `${data.tempoy}`;
        spot_tagsResult.textContent = `${data.spot_tagsy}`;
        listenersResult.textContent = `${data.listenersy}`;
        playcountResult.textContent = `${data.playcounty}`;
        last_tagsResult.textContent = `${data.last_tagsy}`;

        const link2 = document.createElement('a');
        link2.href = `${data.youtube_urly}`;
        link2.textContent = 'Listen on Youtube';
        link2.target = '_blank';
        youtube_urlResult.innerHTML = '';
        youtube_urlResult.appendChild(link2);

        const link3 = document.createElement('a');
        link3.href = `${data.last_urly}`;
        link3.textContent = 'Listen on Last.fm';
        link3.target = '_blank';
        last_urlResult.innerHTML = '';
        last_urlResult.appendChild(link3);

        commentsResult.textContent = `${data.commentsy}`;
        likesResult.textContent = `${data.likesy}`;
        viewsResult.textContent = `${data.viewsy}`;
        loadingGif.style.display = 'none';
        formPic.style.display = 'flex';
        songForm.style.display = 'block';
        $('#resultModal').modal('show');
      })
      .catch(error => {
        console.error('Error:', error);
        loadingGif.style.display = 'none';
        formPic.style.display = "url('folder.png')";
        songForm.style.display = 'block';
      });
  });

  document.getElementById('nextPage').addEventListener('click', function () {
    if (currentPage < totalPages) {
      currentPage++;
    } else {
      currentPage = 1;
    }
    updateModal();
  });

  document.getElementById('prevPage').addEventListener('click', function () {
    if (currentPage > 1) {
      currentPage--;
    } else {
      currentPage = totalPages;
    }
    updateModal();
  });

  resultModal.on('hidden.bs.modal', function () {
    currentPage = 1;
    updateModal();
  });

  function updateModal() {
    document.querySelectorAll('.modal-page').forEach(page => (page.style.display = 'none'));
    document.getElementById('page' + currentPage).style.display = 'block';
  }
});
