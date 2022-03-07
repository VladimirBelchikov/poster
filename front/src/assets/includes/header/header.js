export function header() {

  const phoneButton = document.querySelector('.header__phone-button');

  phoneButton.onclick = () => {
    const phone = document.createElement("a");
    phone.innerHTML = '<span>+7(923)480-44-66</span>'
    const container = document.querySelector('.header__buttons');
    phone.href = "tel:79234804466";
    phone.classList.add("header__phone-number", "text");
    container.replaceChild(phone, phoneButton);
  }

  const menuBurger = document.querySelector('.header__menu-burger');
  const listWrapper = document.querySelector('.header__list-wrapper');

  window.addEventListener('click', e => {
    let target = e.target;
    let isBurgerClicked = menuBurger.contains(target)
    let isMenuClicked = listWrapper.contains(target);
    let isActive = menuBurger.classList.contains('active');

    let isListClicked = document.querySelector('.header__list').contains(target);


    if (!isActive && isBurgerClicked) {
      menuBurger.classList.add('active');
      listWrapper.classList.add('active');
    }

    if (isActive && (isBurgerClicked || !isMenuClicked || !isListClicked)) {
      listWrapper.classList.remove('active');
      menuBurger.classList.remove('active');
    }
  })
}
