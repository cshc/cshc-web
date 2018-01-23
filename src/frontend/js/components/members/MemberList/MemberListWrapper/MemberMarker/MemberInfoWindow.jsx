import React from 'react';
import PropTypes from 'prop-types';
import { InfoWindow } from 'react-google-maps';
import Member from 'models/member';
import Urls from 'util/urls';

const MemberInfoWindow = ({ onCloseClick, member }) => (
  <InfoWindow onCloseClick={() => onCloseClick(null)}>
    <div>
      <h6>{Member.fullName(member)}</h6>
      <p>
        {member.prefPosition !== 'Not known' ? (
          <span>
            {member.prefPosition}
            <br />
          </span>
        ) : null}
      </p>
      <a href={Urls.member_detail(member.id)} className="btn u-btn-primary" title="Member Details">
        Details...
      </a>
    </div>
  </InfoWindow>
);

MemberInfoWindow.propTypes = {
  member: PropTypes.shape({}).isRequired,
  onCloseClick: PropTypes.func.isRequired,
};

export default MemberInfoWindow;
