import React from 'react';
import PropTypes from 'prop-types';
import GoogleMap from 'components/common/GoogleMap';
import { ViewType } from 'util/constants';
import { ViewSwitcher, ViewSwitcherView } from 'components/common/ViewSwitcher';
import VenueTable from './VenueTable';
import VenueMarker from './VenueMarker';

const VenueListWrapper = ({ data, viewType, onSelectViewType, ...props }) => (
  <div>
    <ViewSwitcher currentView={viewType} onSelectViewType={onSelectViewType}>
      <ViewSwitcherView iconClass="fas fa-table" label={ViewType.List} />
      <ViewSwitcherView iconClass="far fa-map" label={ViewType.Map} />
    </ViewSwitcher>
    {viewType === ViewType.List ? (
      <VenueTable venues={data.results} {...props} />
    ) : (
      <GoogleMap
        markers={data.results.map(venue => <VenueMarker key={venue.slug} venue={venue} />)}
      />
    )}
  </div>
);

VenueListWrapper.propTypes = {
  data: PropTypes.shape(),
  viewType: PropTypes.string.isRequired,
  onSelectViewType: PropTypes.func.isRequired,
};

VenueListWrapper.defaultProps = {
  data: undefined,
};

export default VenueListWrapper;
