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

  getPosition: (venue) => {
    if (!venue.position) return undefined;
    const pos = venue.position.split(',');
    return {
      lat: parseFloat(pos[0]),
      lng: parseFloat(pos[1]),
    };
  },
};

export default Venue;
