import React from 'react';
import PropTypes from 'prop-types';
import Urls from 'util/urls';

/**
 * The core details of a Member (profile pic, name, position, squad)
 * 
 * Displayed in the Member Details app
 */
const MemberCard = ({ member }) => (
  <div className="g-brd-around g-brd-gray-light-v4 text-center g-font-weight-600">
    <img
      className="img-fluid w-100"
      src={member.profilePicUrl || Urls.static('img/avatar-placeholder.jpg')}
      alt="Profile pic"
    />
    <div className="g-pa-20">
      <h3 className="m-0">
        {member.firstName}
        <br />
        {member.lastName}
      </h3>
    </div>
    {(member.profilePicUrl || member.squad) && (
      <div className="g-pb-20">
        {member.prefPosition && <div className="g-font-size-18">{member.prefPosition}</div>}
        {member.squad && (
          <div className="g-font-size-18">
            <a title="Team Details" href={Urls.clubteam_detail(member.squad.slug)}>
              {member.squad.name}
            </a>
          </div>
        )}
      </div>
    )}
  </div>
);

MemberCard.propTypes = {
  member: PropTypes.shape({
    firstName: PropTypes.string.isRequired,
    lastName: PropTypes.string.isRequired,
    profilePicUrl: PropTypes.string,
    prefPosition: PropTypes.string,
    squad: PropTypes.shape({
      slug: PropTypes.string,
      name: PropTypes.string,
    }),
  }).isRequired,
};

MemberCard.defaultProps = {};

export default MemberCard;
