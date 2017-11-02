import React from 'react';
import PropTypes from 'prop-types';
import { NetworkStatus as NS } from 'apollo-client';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';
import { ViewType } from 'util/constants';
import { ViewSwitcher, ViewSwitcherView } from 'components/common/ViewSwitcher';
import MemberTable from '../MemberTable';
import MemberMap from '../MemberMap';

const MemberListWrapper = ({ networkStatus, error, members, viewType, onSelectViewType }) => {
  if (error) return <ErrorDisplay errorMessage="Failed to load members" />;
  if (!members || networkStatus === NS.loading) {
    return <Loading message="Fetching members..." />;
  }
  return (
    <div>
      <ViewSwitcher currentView={viewType} onSelectViewType={onSelectViewType}>
        <ViewSwitcherView iconClass="fa fa-table" label={ViewType.List} />
        <ViewSwitcherView iconClass="fa fa-map-0" label={ViewType.Map} />
      </ViewSwitcher>
      {viewType === ViewType.List ? (
        <MemberTable members={members} />
      ) : (
        <MemberMap members={members} />
      )}
    </div>
  );
};

MemberListWrapper.propTypes = {
  networkStatus: PropTypes.number.isRequired,
  error: PropTypes.instanceOf(Error),
  members: PropTypes.shape(),
  viewType: PropTypes.string.isRequired,
  onSelectViewType: PropTypes.func.isRequired,
};

MemberListWrapper.defaultProps = {
  error: undefined,
  members: undefined,
};

export default MemberListWrapper;
