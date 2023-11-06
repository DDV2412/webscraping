const perPage = document.getElementById('page-order');

const urlParams = new URLSearchParams(window.location.search);
const savedPerPage = urlParams.get('page-show');
const switchToggle = document.querySelector('.switch_toggle');
const duplicatedSwitch = document.getElementById('switch');

if (savedPerPage) {
  perPage.value = savedPerPage;
}

perPage.addEventListener('input', function () {
  updateQueryParam('page-show', perPage.value);
});

let currentPage =
  parseInt(new URLSearchParams(window.location.search).get('page')) || 1;
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

prevBtn.addEventListener('click', function () {
  if (currentPage > 1) {
    currentPage--;
    updateQueryParam('page', currentPage);
    prevBtn.removeAttribute('disabled');
  } else {
    prevBtn.setAttribute('disabled', 'true');
  }
});

nextBtn.addEventListener('click', function () {
  currentPage++;
  updateQueryParam('page', currentPage);
});

const searchQueryParam = urlParams.get('search');

if (searchQueryParam !== null) {
  const searchInput = document.getElementById('search-input');
  searchInput.value = searchQueryParam;
}

const searchForm = document.getElementById('search');

searchForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const searchInput = document.getElementById('search-input').value;
  updateQueryParam('search', searchInput);
});

function updateQueryParam(key, value) {
  const queryParams = new URLSearchParams(window.location.search);
  if (value === null) {
    queryParams.delete(key);
  } else {
    queryParams.set(key, value);
  }
  window.history.replaceState(null, null, '?' + queryParams.toString());
  window.location.reload();
}

function handleQueryParam() {
  const urlParams = new URLSearchParams(window.location.search);
  const duplicateParam = urlParams.get('duplicate');

  if (duplicateParam === 'true') {
    switchToggle.classList.add('duplicated');
  } else {
    switchToggle.classList.remove('duplicated');
  }
}

duplicatedSwitch.addEventListener('click', () => {
  if (switchToggle.classList.contains('duplicated')) {
    switchToggle.classList.remove('duplicated');
    updateQueryParam('duplicate', null);
  } else {
    switchToggle.classList.add('duplicated');
    updateQueryParam('duplicate', 'true');
  }
});

window.addEventListener('DOMContentLoaded', handleQueryParam);
