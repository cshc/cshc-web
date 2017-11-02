import React from 'react';
import PropTypes from 'prop-types';
import { NetworkStatus as NS } from 'apollo-client';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';
import { ViewType } from 'util/constants';
import { ViewSwitcher, ViewSwitcherView } from 'components/common/ViewSwitcher';
import VenueTable from '../VenueTable';
import VenueMap from '../VenueMap';

const VenueListWrapper = ({ networkStatus, error, venues, viewType, onSelectViewType }) => {
  if (error) return <ErrorDisplay errorMessage="Failed to load venues" />;
  if (!venues || networkStatus === NS.loading) {
    return <Loading message="Fetching venues..." />;
  }
  return (
    <div>
      <ViewSwitcher currentView={viewType} onSelectViewType={onSelectViewType}>
        <ViewSwitcherView iconClass="fa fa-table" label={ViewType.List} />
        <ViewSwitcherView iconClass="fa fa-map-0" label={ViewType.Map} />
      </ViewSwitcher>
      {viewType === ViewType.List ? <VenueTable venues={venues} /> : <VenueMap venues={venues} />}
    </div>
  );
};

VenueListWrapper.propTypes = {
  networkStatus: PropTypes.number.isRequired,
  error: PropTypes.instanceOf(Error),
  venues: PropTypes.shape(),
  viewType: PropTypes.string.isRequired,
  onSelectViewType: PropTypes.func.isRequired,
};

VenueListWrapper.defaultProps = {
  error: undefined,
  venues: undefined,
};

export default VenueListWrapper;
