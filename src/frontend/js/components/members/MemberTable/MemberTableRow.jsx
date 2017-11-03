import React from 'react';
import PropTypes from 'prop-types';

const MemberTableRow = ({ member }) => (
  <tr>
    <td>{member.firstName}</td>
    <td>{member.lastName}</td>
    <td className="priority3">{member.gender[0]}</td>
    <td className="priority3">{member.prefPosition}</td>
    <td>{member.numAppearances}</td>
    <td>{member.goals}</td>
  </tr>
);

MemberTableRow.propTypes = {
  member: PropTypes.shape({
    first_name: PropTypes.string,
    last_name: PropTypes.string,
  }).isRequired,
};

export default MemberTableRow;
