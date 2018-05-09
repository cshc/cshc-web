import { AvailabilityType } from 'util/constants';

const Availability = {
  context(availabilityType) {
    if (availabilityType === AvailabilityType.Playing) return 'play';
    else if (availabilityType === AvailabilityType.Umpiring) return 'umpire';
    return '???';
  },
};

export default Availability;
