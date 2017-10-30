import React from 'react';
import PropTypes from 'prop-types';
import { NetworkStatus as NS } from 'apollo-client';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';
import { SwitchableView, ViewType } from 'util/constants';
import ViewSwitcher from 'components/common/ViewSwitcher';
import VenueTable from '../VenueTable';

const VenueListWrapper = ({ networkStatus, error, venues, viewType, onSelectViewType }) => {
  if (error) return <ErrorDisplay errorMessage="Failed to load venues" />;
  if (!venues || networkStatus === NS.loading) {
    return <Loading message="Fetching venues..." />;
  }
  const views = [
    {
      iconClass: 'fa fa-table',
      label: ViewType.List,
      onSelect: () => onSelectViewType(SwitchableView.VenueList, ViewType.List),
    },
    {
      iconClass: 'fa fa-map-o',
      label: ViewType.Map,
      onSelect: () => onSelectViewType(SwitchableView.VenueList, ViewType.Map),
    },
  ];
  return (
    <div>
      <ViewSwitcher views={views} currentView={viewType} />
      {viewType === ViewType.List ? <VenueTable venues={venues} /> : <div>Map</div>}
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
