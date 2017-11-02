import React from 'react';
import PropTypes from 'prop-types';
import { Marker } from 'react-google-maps';
import { getPosition } from 'util/cshc';
import Member from 'models/member';
import GoogleMap from 'components/common/GoogleMap';

const MemberMap = ({ index, onToggleOpen, isOpen, members }) => (
  <GoogleMap items={members}>
    {members.edges.map(memberEdge => (
      <Marker
        position={getPosition(memberEdge.node.addrPosition)}
        title={Member.fullName(memberEdge.node)}
        onClick={() => onToggleOpen(index)}
      />
    ))}
  </GoogleMap>
);

MemberMap.propTypes = {
  members: PropTypes.shape().isRequired,
  index: PropTypes.number.isRequired,
  isOpen: PropTypes.bool.isRequired,
  onToggleOpen: PropTypes.func.isRequired,
};

MemberMap.defaultProps = {
  members: undefined,
};

export default MemberMap;
