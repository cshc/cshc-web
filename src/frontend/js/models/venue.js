const Venue = {
  full_address: (venue) => {
    const addr = [venue.addr1, venue.addr2, venue.addr3, venue.addrCity, venue.addrPostcode]
      .filter(i => !!i)
      .join(', ');

    if (!addr) {
      return '';
    }
    return addr;
  },
};

export default Venue;
