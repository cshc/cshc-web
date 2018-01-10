import React from 'react';
import PropTypes from 'prop-types';
import { Marker } from 'react-google-maps';
import GoogleMap from 'components/common/GoogleMap';
import Member from 'models/member';
import { getPosition } from 'util/cshc';
import { ViewType } from 'util/constants';
import { ViewSwitcher, ViewSwitcherView } from 'components/common/ViewSwitcher';
import MemberTable from './MemberTable';

const MemberListWrapper = ({ data, viewType, onSelectViewType }) => (
  <div>
    <ViewSwitcher currentView={viewType} onSelectViewType={onSelectViewType}>
      <ViewSwitcherView iconClass="fa fa-table" label={ViewType.List} />
      <ViewSwitcherView iconClass="fa fa-map-0" label={ViewType.Map} />
    </ViewSwitcher>
    {viewType === ViewType.List ? (
      <MemberTable members={data} />
    ) : (
      <GoogleMap
        markers={data.results.map(member => (
          <Marker
            key={member.id}
            position={getPosition(member.addrPosition)}
            title={Member.fullName(member)}
          />
        ))}
      />
    )}
  </div>
);

MemberListWrapper.propTypes = {
  data: PropTypes.shape(),
  viewType: PropTypes.string.isRequired,
  onSelectViewType: PropTypes.func.isRequired,
};

MemberListWrapper.defaultProps = {
  data: undefined,
};

export default MemberListWrapper;
