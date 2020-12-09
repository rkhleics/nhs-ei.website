/**
 * for issue https://github.com/rkhleics/nhs-ei.website/issues/29
 * a patch to make the search button work
 * we won't need this going forward but it needs to remain in place for now
 * until the wagtailfrontend package is no longer used
 * an altertanive is to use the header includes from wagtailfrontend package that has
 * been altered to allow this to work when its used but not for now.
 */

const searchBar = document.querySelector('.nhsuk-header__search');
if (searchBar) {
  const toggleButton = document.querySelector('#toggle-search');
  const closeButton = document.querySelector('#close-search');
  const searchContainer = document.querySelector('#wrap-search');
  const menuSearchContainer = document.querySelector('#content-header');
  toggleButton.addEventListener('click', function(){
    toggleButton.setAttribute('aria-expanded', true);
    toggleButton.classList.add('is-active');
    searchContainer.classList.add('js-show');
    menuSearchContainer.classList.add('js-show');
  });
  closeButton.addEventListener('click', function(){
    toggleButton.removeAttribute('aria-expanded');
    toggleButton.classList.remove('is-active');
    searchContainer.classList.remove('js-show');
    menuSearchContainer.classList.remove('js-show');
  });
}

/** end */