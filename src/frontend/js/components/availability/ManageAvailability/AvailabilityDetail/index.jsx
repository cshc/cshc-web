import { compose } from 'react-apollo';
import UpdateMatchAvailabilityMutation from 'components/availability/updateMatchAvailabilityMutation';
import ActionMatchAvailabilityMutation from 'components/availability/actionMatchAvailabilityMutation';
import AvailabilityDetail from './AvailabilityDetail';

export default compose(UpdateMatchAvailabilityMutation, ActionMatchAvailabilityMutation)(
  AvailabilityDetail,
);
