document.head.innerHTML +=
  '<link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Montserrat:400,600&display=swap" />';

document.head.innerHTML +=
  '<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.10.2/css/all.min.css" />';

const snackbar = document.createElement('div');
snackbar.className = 'snackbar';
snackbar.id = 'snackbar';

const dropdownContent = document.createElement('div');
dropdownContent.className = 'dropdownContent hidden';
dropdownContent.id = 'dropdownContent';

const p = document.createElement('p');

dropdownContent.appendChild(p);
snackbar.appendChild(dropdownContent);

const toggleButton = document.createElement('a');
toggleButton.innerHTML = '<i class="fas arrow-alt-circle-up"></i>';
toggleButton.id = 'btnOpenDrawer';
toggleButton.className = 'btnOpenDrawer';

const changeTextContent = text => {
  const textContent = document.createTextNode(text);
  const div = document.createElement('div');

  div.className = 'snackbarContent';

  div.appendChild(toggleButton);
  div.appendChild(textContent);
  snackbar.appendChild(div);
};

const textCondition = isPolitical => (isPolitical ? 'not' : '');

export const setFlag = isPolitical => {
  snackbar.className = 'snackbar';
  if (isPolitical) {
    snackbar.classList.add('political');
  } else {
    snackbar.classList.add('noPolitical');
  }

  changeTextContent(`This article is ${textCondition(isPolitical)} objective!`);
};

export const openDropdown = () => {
  snackbar.classList.toggle('open');
  snackbar.classList.toggle('showContent');
  dropdownContent.classList.toggle('hidden');
};

toggleButton.onclick = openDropdown;

export default snackbar;
