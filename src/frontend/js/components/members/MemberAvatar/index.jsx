import React from 'react';
import PropTypes from 'prop-types';
import Member from 'models/member';
import Urls from 'util/urls';

/**
 * Avatar representation of a club member, hyperlinked to their profile.
 * 
 * If no profile picture is available, the appropriate mens/ladies shirt is shown, 
 * with the member's shirt number - if known.
 */
const MemberAvatar = ({ member, size, badgeCount, className }) => {
  const title = `${Member.fullName(member)} - view profile`;
  return (
    <a
      className={`${className} align-middle g-pos-rel d-inline-block`}
      href={Urls.member_detail(member.modelId)}
      title={title}
    >
      {badgeCount && (
        <span className="u-badge-v1 g-bg-primary g-color-white g-rounded-50x g-mt-5 g-mr-5">
          {badgeCount}
        </span>
      )}
      {member.thumbUrl ? (
        <img
          className={`media-object g-rounded-50x u-image-icon-size-${size}`}
          alt="Profile Pic"
          src={member.thumbUrl}
        />
      ) : (
        <span className={`shirt-number shirt-number-${size} ${member.gender.toLowerCase()}`}>
          {member.shirtNumber}
        </span>
      )}
    </a>
  );
};

MemberAvatar.propTypes = {
  member: PropTypes.shape({
    firstName: PropTypes.string,
    lastName: PropTypes.string,
    gender: PropTypes.string,
    thumbUrl: PropTypes.string,
    shirtNumber: PropTypes.string,
  }).isRequired,
  badgeCount: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  size: PropTypes.string,
  className: PropTypes.string,
};

MemberAvatar.defaultProps = {
  badgeCount: undefined,
  size: 'md',
  className: '',
};

export default MemberAvatar;
