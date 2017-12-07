import React from 'react';
import PropTypes from 'prop-types';
import GoogleMap from 'components/common/GoogleMap';
import { ViewType } from 'util/constants';
import { ViewSwitcher, ViewSwitcherView } from 'components/common/ViewSwitcher';
import VenueTable from './VenueTable';
import VenueMarker from './VenueMarker';

const VenueListWrapper = ({ data, viewType, onSelectViewType }) => (
  <div>
    <ViewSwitcher currentView={viewType} onSelectViewType={onSelectViewType}>
      <ViewSwitcherView iconClass="fa fa-table" label={ViewType.List} />
      <ViewSwitcherView iconClass="fa fa-map-0" label={ViewType.Map} />
    </ViewSwitcher>
    {viewType === ViewType.List ? (
      <VenueTable venues={data} />
    ) : (
      <GoogleMap
        markers={data.edges.map(venueEdge => (
          <VenueMarker key={venueEdge.node.slug} venue={venueEdge.node} />
        ))}
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
