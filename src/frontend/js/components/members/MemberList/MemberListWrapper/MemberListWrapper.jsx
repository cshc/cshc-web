import React from 'react';
import PropTypes from 'prop-types';
import GoogleMap from 'components/common/GoogleMap';
import { ViewType } from 'util/constants';
import { ViewSwitcher, ViewSwitcherView } from 'components/common/ViewSwitcher';
import MemberTable from './MemberTable';
import MemberMarker from './MemberMarker';

const MemberListWrapper = ({ canViewMap, data, viewType, onSelectViewType, ...props }) => (
  <div>
    {canViewMap ? (
      <ViewSwitcher currentView={viewType} onSelectViewType={onSelectViewType}>
        <ViewSwitcherView iconClass="fas fa-table" label={ViewType.List} />
        <ViewSwitcherView iconClass="far fa-map" label={ViewType.Map} />
      </ViewSwitcher>
    ) : null}
    {!canViewMap || viewType === ViewType.List ? (
      <MemberTable members={data.results} {...props} />
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
