import { compose } from 'react-apollo';
import switchable from 'components/common/ViewSwitcher/switchableView';
import { addUrlProps } from 'react-url-query';
import Paged from 'components/common/Paged';
import { SwitchableView } from 'util/constants';
import VenueListQuery from './venueListQuery';
import VenueListWrapper from './VenueListWrapper';
import { urlPropsQueryConfig } from '../VenueFilterSet';

const SwitchableVenueListView = switchable(SwitchableView.VenueList);

const withUrlProps = addUrlProps({
  urlPropsQueryConfig: {
    ...urlPropsQueryConfig,
    ...Paged,
  },
});

export default compose(withUrlProps, VenueListQuery, SwitchableVenueListView)(VenueListWrapper);
