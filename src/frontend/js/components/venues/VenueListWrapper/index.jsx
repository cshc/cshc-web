import { compose } from 'react-apollo';
import switchable from 'components/common/ViewSwitcher/switchableView';
import filterable from 'components/filters/filterableContainer';
import { SwitchableView } from 'util/constants';
import VenueListQuery from './venueListQuery';
import VenueListWrapper from './VenueListWrapper';

const SwitchableVenueListView = switchable(SwitchableView.VenueList);

export default compose(filterable, VenueListQuery, SwitchableVenueListView)(VenueListWrapper);
