import React from 'react';
import PropTypes from 'prop-types';
import Member from 'models/member';
import Urls from 'util/urls';

/**
 * Text representation of a club member, hyperlinked to their profile.
 */
const MemberLink = ({ member, badgeCount, useFullName }) => {
  const title = `${Member.fullName(member)} - view profile`;
  const label = useFullName ? Member.fullName(member) : Member.firstNameAndInitial(member);
  return (
    <a href={Urls.member_detail(member.id)} title={title}>
      {label}
      {badgeCount > 1 && <span className=""> ({badgeCount})</span>}
    </a>
  );
};

MemberLink.propTypes = {
  member: PropTypes.shape({
    firstName: PropTypes.string,
    lastName: PropTypes.string,
  }).isRequired,
  badgeCount: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  useFullName: PropTypes.bool,
};

MemberLink.defaultProps = {
  badgeCount: undefined,
  className: '',
  useFullName: false,
};

export default MemberLink;
