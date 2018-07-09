import React from 'react';
import PropTypes from 'prop-types';
import MemberLink from 'components/members/MemberLink';

const AwardWinner = ({ awardWinner, className }) => {
  if (awardWinner.member) {
    return <MemberLink key={awardWinner.member.id} member={awardWinner.member} useFullName />;
  }
  return <span className={className}>{awardWinner.awardee}</span>;
};

AwardWinner.propTypes = {
  awardWinner: PropTypes.shape({
    member: PropTypes.shape({
      firstName: PropTypes.string,
      lastName: PropTypes.string,
      id: PropTypes.string,
      gender: PropTypes.string,
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
