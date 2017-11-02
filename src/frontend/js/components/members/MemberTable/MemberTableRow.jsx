import React from 'react';
import PropTypes from 'prop-types';

const MemberTableRow = ({ member }) => (
  <tr>
    <td>{member.firstName}</td>
    <td>{member.lastName}</td>
    <td>{member.gender[0]}</td>
    <td>{member.prefPosition}</td>
  </tr>
);

MemberTableRow.propTypes = {
  member: PropTypes.shape({
    first_name: PropTypes.string,
    last_name: PropTypes.string,
  }).isRequired,
};

export default MemberTableRow;
