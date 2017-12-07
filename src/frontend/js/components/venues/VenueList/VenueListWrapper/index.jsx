import { compose } from 'react-apollo';
import switchable from 'components/common/ViewSwitcher/switchableView';
import { addUrlProps } from 'react-url-query';
import { SwitchableView } from 'util/constants';
import VenueListQuery from './venueListQuery';
import VenueListWrapper, { urlPropsQueryConfig } from './VenueListWrapper';

const SwitchableVenueListView = switchable(SwitchableView.VenueList);

const withUrlProps = addUrlProps({ urlPropsQueryConfig });

export default compose(withUrlProps, VenueListQuery, SwitchableVenueListView)(VenueListWrapper);
