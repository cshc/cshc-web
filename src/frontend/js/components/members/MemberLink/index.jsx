import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import Member from 'models/member';
import Urls from 'util/urls';
import styles from './style.scss';

/**
 * Text representation of a club member, hyperlinked to their profile.
 */
const MemberLink = ({ member, badgeCount, className, useFullName }) => {
  const linkClassName = classnames(className, styles.memberLink);
  const title = `${Member.fullName(member)} - view profile`;
  const label = useFullName ? Member.fullName(member) : Member.firstNameAndInitial(member);
  return (
    <a className={linkClassName} href={Urls.member_detail(member.modelId)} title={title}>
      {badgeCount && (
        <span className="u-badge-v1 g-bg-primary g-color-white g-rounded-50x">{badgeCount}</span>
      )}
      {member.thumbUrl && (
        <img src={member.thumbUrl} alt="Profile Pic" className={styles.memberImage} />
      )}
      <span className={styles.memberName}>{label}</span>
    </a>
  );
};

MemberLink.propTypes = {
  member: PropTypes.shape({
    firstName: PropTypes.string,
    lastName: PropTypes.string,
    thumbUrl: PropTypes.string,
  }).isRequired,
  badgeCount: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  className: PropTypes.string,
  useFullName: PropTypes.bool,
};

MemberLink.defaultProps = {
  badgeCount: undefined,
  className: '',
  useFullName: false,
};

export default MemberLink;
