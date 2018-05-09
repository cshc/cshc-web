/**
 * Utility method to initialize the 'manual' handling of a bootstrap
 * dropdown button menu that is not hidden when one of its items is clicked.
 * 
 * This is useful when we put MutationButtons in the dropdown menu and want the
 * user to see the mutation progress feedback.
 */
const initStickyDropdown = (selector) => {
  const dropdownToggle = window.jQuery(`${selector} .dropdown-toggle`);
  const dropdownMenu = window.jQuery(`${selector} .dropdown-menu`);
  // Show/hide the dropdown menu when the button is clicked
  dropdownToggle.on('click', () => {
    window
      .jQuery(this)
      .parent()
      .toggleClass('show');
    dropdownMenu.toggleClass('show');
  });
  // Hide the dropdown menu when anything _but_ the dropdown menu is clicked
  window.jQuery('body').on('click', (e) => {
    if (
      !dropdownToggle.is(e.target) &&
      dropdownToggle.has(e.target).length === 0 &&
      window.jQuery('.show').has(e.target).length === 0
    ) {
      dropdownToggle.removeClass('show');
      dropdownMenu.removeClass('show');
    }
  });
};

module.exports = {
  initStickyDropdown,
};
