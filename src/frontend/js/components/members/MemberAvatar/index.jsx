import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import Member from 'models/member';
import Urls from 'util/urls';
import { Gender } from 'util/constants';
import styles from './style.scss';

/**
 * Avatar representation of a club member, hyperlinked to their profile.
 * 
 * If no profile picture is available, the appropriate mens/ladies shirt is shown, 
 * with the member's shirt number - if known.
 */
class MemberAvatar extends React.Component {
  componentDidMount() {
    window.jQuery(`#shirt-${this.props.member.shirtNumber}`).fitText(0.5);
  }

  render() {
    const { member, badgeCount, className, rounded } = this.props;
    const title = `${Member.fullName(member)} - view profile`;
    const fallbackImage =
      member.gender === Gender.Male ? 'img/kit/mens_shirt_sq_y1.png' : 'img/kit/ladies_shirt_sq_y1.png';
    const fallbackImageUrl = Urls.static(fallbackImage);
    const imgClass = classnames('w-100', {
      'u-shadow-v29 rounded-circle': rounded,
    });

    return (
      <a
        className={`${className} g-pos-rel d-block`}
        href={Urls.member_detail(member.id)}
        title={title}
      >
        {badgeCount && (
          <span className="u-badge-v1 g-bg-primary g-color-white g-rounded-50x g-mt-5 g-mr-5">
            {badgeCount}
          </span>
        )}
        {member.thumbUrl ? (
          <img className={imgClass} alt="Profile Pic" src={member.thumbUrl} />
        ) : (
          <div className="">
            <img className="w-100" alt="Shirt" src={fallbackImageUrl} />
            {member.shirtNumber && (
              <div
                id={`shirt-${member.shirtNumber}`}
                className={`g-pos-abs text-center ${styles.shirtNumber}`}
              >
                {member.shirtNumber}
              </div>
            )}
          </div>
        )}
      </a>
    );
  }
}

MemberAvatar.propTypes = {
  member: PropTypes.shape({
    firstName: PropTypes.string,
    lastName: PropTypes.string,
    gender: PropTypes.string,
    thumbUrl: PropTypes.string,
    shirtNumber: PropTypes.string,
  }).isRequired,
  badgeCount: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  className: PropTypes.string,
  rounded: PropTypes.bool,
};

MemberAvatar.defaultProps = {
  badgeCount: undefined,
  className: '',
  rounded: true,
};

export default MemberAvatar;
