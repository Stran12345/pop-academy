document.addEventListener('DOMContentLoaded', function () {
  let currentPage = 1;
  const totalPages = 3;
  const params = new URLSearchParams(window.location.search);
  const numberSongs = params.get('numberSongs');

  const formContainer = document.getElementById('formContainer');
  const subButton = document.getElementById('submitButton');
  const loadingGif = document.getElementById('loading');
  const loadingWrapper = document.getElementById('loading-wrapper');

  for (let i = 1; i <= numberSongs; i++) {
    const form = document.createElement('form');
    form.setAttribute('id', `form${i}`);
    form.innerHTML = `
      <div id="folderForm${i}" class="container formy" style="font-size: large">
        <h1 style="text-align: center">
          <b>Contestant Number ${i}</b>
        </h1>
        <p style="margin-top: 0px; margin-bottom: 0px">Enter song #${i}</p>
        <div class="mb-3">
          <label for="song${i}_input" class="form-label">
            Song:
          </label>
          <input
            type="text"
            class="form-control"
            id="song${i}_input"
            style="font-size: large"
            required
          />
        </div>
        <div class="mb-3">
          <label for="artist${i}_input" class="form-label">
            Artist(s):
          </label>
          <input
            type="text"
            class="form-control"
            id="artist${i}_input"
            style="font-size: large"
            required
          />
        </div>
      </div>
    `;
    formContainer.appendChild(form);
  }

  function isImageURL(url) {
    return url.startsWith('https://i.scdn.co/image/') || url.startsWith('https://img.freepik.com');
  }

  function addTableToModal(tableData, pagenum) {
    const tableContainer = document.getElementById(`tableContainer${pagenum}`);
    const table = document.createElement('table');
    table.classList.add('table');

    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');

    tableData.headers.forEach((headerText, index) => {
      const th = document.createElement('th');
      th.scope = 'col';
      th.classList.add('sortable');
      th.innerHTML = `${headerText} <span class="sort-arrow"></span>`;
      th.addEventListener('click', () => sortTable(table, index));
      headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    tableData.rows.forEach(rowData => {
      const tr = document.createElement('tr');
      rowData.forEach(cellData => {
        const td = document.createElement('td');
        if (isImageURL(cellData)) {
          const img = document.createElement('img');
          img.src = cellData;
          img.style.width = '100%';
          img.style.height = 'auto';
          img.style.margin = '0';
          img.style.maxWidth = '100%';
          td.style.width = '15rem';
          td.appendChild(img);
        } else {
          td.textContent = cellData;
        }
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });

    table.appendChild(tbody);
    tableContainer.appendChild(table);
  }

  function sortTable(table, columnIndex) {
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.rows);

    const th = table.querySelectorAll('th')[columnIndex];
    const isAscending = th.classList.contains('asc');

    const isNumeric = rows.every(
      row => !isNaN(row.cells[columnIndex].innerText.trim().replace(/,/g, '')),
    );
    const isDate = rows.every(row => !isNaN(Date.parse(row.cells[columnIndex].innerText.trim())));

    rows.sort((rowA, rowB) => {
      let cellA = rowA.cells[columnIndex].innerText.trim();
      let cellB = rowB.cells[columnIndex].innerText.trim();

      let comparison;
      if (isNumeric) {
        cellA = parseFloat(cellA.replace(/,/g, ''));
        cellB = parseFloat(cellB.replace(/,/g, ''));
        comparison = cellA - cellB;
      } else if (isDate) {
        cellA = new Date(cellA);
        cellB = new Date(cellB);
        comparison = cellA - cellB;
      } else {
        comparison = cellA.localeCompare(cellB);
      }
      return isAscending ? -comparison : comparison;
    });

    rows.forEach(row => tbody.appendChild(row));
    table.querySelectorAll('th').forEach(th => {
      th.classList.remove('asc', 'desc');
      th.querySelector('.sort-arrow').textContent = '';
    });

    th.classList.toggle('asc', !isAscending);
    th.classList.toggle('desc', isAscending);
    th.querySelector('.sort-arrow').textContent = isAscending ? ' ▲' : ' ▼';
  }

  function formatNumberWithCommas(numberStr) {
    let number = parseFloat(numberStr);
    if (isNaN(number)) {
      return 'Invalid number';
    }
    return number.toLocaleString();
  }

  document.getElementById('submitButton').addEventListener('click', function () {
    const basic = {
      headers: ['Track Image', 'Title', 'Artist', 'Release Date'],
      rows: [],
    };

    const streaming = {
      headers: ['Title', 'Artist', 'Spotify Popularity', 'Last.fm Listeners', 'Last.fm Playcount'],
      rows: [],
    };

    const video = {
      headers: ['Title', 'Artist', 'Youtube Comments', 'Youtube Likes', 'Youtube Views'],
      rows: [],
    };

    let fetchPromises = [];
    let allFieldsFilled = true;

    for (let i = 1; i <= numberSongs; i++) {
      const songInput = document.getElementById(`song${i}_input`);
      const artistInput = document.getElementById(`artist${i}_input`);

      if (!songInput.value.trim() || !artistInput.value.trim()) {
        allFieldsFilled = false;
        alert(`Please fill in all fields for Song ${i}`);
        break;
      }
    }

    if (!allFieldsFilled) {
      return;
    }

    loadingWrapper.style.display = 'flex';
    loadingGif.style.display = 'flex';
    formContainer.style.display = 'none';
    subButton.style.display = 'none';

    for (let i = 1; i <= numberSongs; i++) {
      const song_name = document.getElementById(`song${i}_input`).value;
      const artist_name = document.getElementById(`artist${i}_input`).value;

      let fetchPromise = fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ song_name, artist_name }),
      })
        .then(response => response.json())
        .then(data => {
          basic.rows.push([data.picy, data.titley, data.artisty, data.release_datey]);
          streaming.rows.push([
            data.titley,
            data.artisty,
            formatNumberWithCommas(data.popularityy),
            formatNumberWithCommas(data.listenersy),
            formatNumberWithCommas(data.playcounty),
          ]);
          video.rows.push([
            data.titley,
            data.artisty,
            formatNumberWithCommas(data.commentsy),
            formatNumberWithCommas(data.likesy),
            formatNumberWithCommas(data.viewsy),
          ]);
        })
        .catch(error => {
          console.error('Error:', error);
        });

      fetchPromises.push(fetchPromise);
    }

    Promise.all(fetchPromises)
      .then(() => {
        loadingGif.style.display = 'none';
        loadingWrapper.style.display = 'none';
        formContainer.style.display = 'flex';
        subButton.style.display = 'initial';
        addTableToModal(basic, 1);
        addTableToModal(streaming, 2);
        addTableToModal(video, 3);
        const myModal = new bootstrap.Modal(document.getElementById('resultModal'));
        myModal.show();
      })
      .catch(error => {
        console.error('Error in processing fetch calls:', error);
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

  document.getElementById('resultModal').addEventListener('hidden.bs.modal', function () {
    currentPage = 1;
    document.getElementById('tableContainer1').innerHTML = '';
    document.getElementById('tableContainer2').innerHTML = '';
    document.getElementById('tableContainer3').innerHTML = '';
    updateModal();
  });

  function updateModal() {
    document.querySelectorAll('.modal-page').forEach(page => (page.style.display = 'none'));
    document.getElementById('page' + currentPage).style.display = 'block';
  }
});
