import React from 'react';
import PropTypes from 'prop-types';
import { NetworkStatus as NS } from 'apollo-client';
import { Marker } from 'react-google-maps';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';
import GoogleMap from 'components/common/GoogleMap';
import Member from 'models/member';
import { getPosition } from 'util/cshc';
import { ViewType } from 'util/constants';
import { ViewSwitcher, ViewSwitcherView } from 'components/common/ViewSwitcher';
import MemberTable from '../MemberTable';

const MemberListWrapper = ({ networkStatus, error, members, viewType, onSelectViewType }) => {
  if (error) return <ErrorDisplay errorMessage="Failed to load members" />;
  if (!members && networkStatus === NS.loading) {
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
        <GoogleMap
          markers={members.edges.map(memberEdge => (
            <Marker
              key={memberEdge.node.modelId}
              position={getPosition(memberEdge.node.addrPosition)}
              title={Member.fullName(memberEdge.node)}
            />
          ))}
        />
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
