import React from 'react';
import PropTypes from 'prop-types';
import { Marker } from 'react-google-maps';
import { MapIcons } from 'components/common/GoogleMap';
import Member from 'models/member';
import { getPosition } from 'util/cshc';
import MemberInfoWindow from './MemberInfoWindow';

const MemberMarker = ({ member, isOpen, onClick }) => (
  <Marker
    position={getPosition(member.addrPosition)}
    icon={MapIcons[member.gender]}
    title={Member.fullName(member)}
    onClick={onClick}
  >
    {isOpen && <MemberInfoWindow member={member} onCloseClick={onClick} />}
  </Marker>
);

// Note: isOpen and onClick should be set by the GoogleMap parent component.
MemberMarker.propTypes = {
  member: PropTypes.shape().isRequired,
  isOpen: PropTypes.bool,
  onClick: PropTypes.func,
};

MemberMarker.defaultProps = {
  isOpen: false,
  onClick: () => {},
};

export default MemberMarker;
