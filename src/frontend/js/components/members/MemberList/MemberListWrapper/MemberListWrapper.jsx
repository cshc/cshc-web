import React from 'react';
import PropTypes from 'prop-types';
import { Marker } from 'react-google-maps';
import GoogleMap, { MapIcons } from 'components/common/GoogleMap';
import Member from 'models/member';
import { getPosition } from 'util/cshc';
import { ViewType, Gender } from 'util/constants';
import { ViewSwitcher, ViewSwitcherView } from 'components/common/ViewSwitcher';
import MemberTable from './MemberTable';
import MemberMarker from './MemberMarker';

const MemberListWrapper = ({ canViewMap, data, viewType, onSelectViewType }) => (
  <div>
    {canViewMap ? (
      <ViewSwitcher currentView={viewType} onSelectViewType={onSelectViewType}>
        <ViewSwitcherView iconClass="fas fa-table" label={ViewType.List} />
        <ViewSwitcherView iconClass="far fa-map" label={ViewType.Map} />
      </ViewSwitcher>
    ) : null}
    {!canViewMap || viewType === ViewType.List ? (
      <MemberTable members={data.results} />
    ) : (
      <GoogleMap
        markers={data.results
          .filter(member => member.addrPosition)
          .map(member => <MemberMarker key={member.id} member={member} />)}
      />
    )}
  </div>
);

MemberListWrapper.propTypes = {
  canViewMap: PropTypes.bool.isRequired,
  data: PropTypes.shape(),
  viewType: PropTypes.string.isRequired,
  onSelectViewType: PropTypes.func.isRequired,
};

MemberListWrapper.defaultProps = {
  data: undefined,
};

export default MemberListWrapper;
