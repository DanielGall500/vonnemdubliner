/* Change the website theme between dark and light. */
const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');

function switchTheme(e) {
  if (e.target.checked) {
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
  }
  else {
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('theme','light');
  }
}

toggleSwitch.addEventListener('click', switchTheme, false);

/* Set the theme based on previous preferences */
const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;

if (currentTheme) {
  document.documentElement.setAttribute('data-theme', currentTheme)
  if (currentTheme == 'dark') {
    toggleSwitch.checked = true;
  }
}
