import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import MemberLink from 'components/members/MemberLink';
import styles from './style.scss';

const AwardWinner = ({ awardWinner, className }) => {
  const awardWinnerClassName = classnames(className, styles.awardWinner);

  if (awardWinner.member) {
    return (
      <MemberLink
        key={awardWinner.member.modelId}
        member={awardWinner.member}
        className={className}
        useFullName
      />
    );
  }
  return <div className={awardWinnerClassName}>{awardWinner.awardee}</div>;
};

AwardWinner.propTypes = {
  awardWinner: PropTypes.shape({
    member: PropTypes.shape({
      firstName: PropTypes.string,
      lastName: PropTypes.string,
      modelId: PropTypes.number,
      gender: PropTypes.string,
      thumbUrl: PropTypes.string,
    }),
    awardee: PropTypes.string,
    award: PropTypes.shape({
      name: PropTypes.string,
    }),
  }).isRequired,
  className: PropTypes.string,
};

AwardWinner.defaultProps = {
  className: '',
};

export default AwardWinner;
