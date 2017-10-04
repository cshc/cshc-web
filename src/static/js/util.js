var isMobile = {
  Android() {
    return navigator.userAgent.match(/Android/i);
  },
  BlackBerry() {
    return navigator.userAgent.match(/BlackBerry/i);
  },
  iOS() {
    return navigator.userAgent.match(/iPhone|iPad|iPod/i);
  },
  Opera() {
    return navigator.userAgent.match(/Opera Mini/i);
  },
  Windows() {
    return navigator.userAgent.match(/IEMobile/i);
  },
  any() {
    return (
      isMobile.Android() ||
      isMobile.BlackBerry() ||
      isMobile.iOS() ||
      isMobile.Opera() ||
      isMobile.Windows()
    );
  },
};

/**
 * Returns the full address with (not None) address items separated by commas.
 * If the address is empty, returns 'Address unknown'.
 */
const full_address = (venue) => {
  const addr = [venue.addr1, venue.addr2, venue.addr3, venue.addr_city, venue.addr_postcode]
    .filter(i => !!i)
    .join(', ');

  if (!addr) {
    return 'Address unknown';
  }
  return addr;
};
