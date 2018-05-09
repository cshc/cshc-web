import { compose } from 'react-apollo';
import Paged from 'components/common/Paged';
import CreateMatchAvailabilityMutation from 'components/availability/createMatchAvailabilityMutation';
import ActionMatchAvailabilityMutation from 'components/availability/actionMatchAvailabilityMutation';
import AvailabilityData from './availabilityQuery';
import ManageAvailability from './ManageAvailability';

export default compose(
  Paged,
  AvailabilityData,
  CreateMatchAvailabilityMutation,
  ActionMatchAvailabilityMutation,
)(ManageAvailability);
