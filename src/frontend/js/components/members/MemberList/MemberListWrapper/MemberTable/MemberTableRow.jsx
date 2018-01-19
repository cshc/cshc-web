import React from 'react';
import PropTypes from 'prop-types';
import Urls from 'util/urls';

const MemberTableRow = ({ member }) => (
  <tr className="g-cursor-pointer" title="View member details..." onClick={() => { window.location = Urls.member_detail(member.id); }}>
    <td>{member.firstName}</td>
    <td>{member.lastName}</td>
    <td className="priority3">{member.gender[0]}</td>
    <td className="priority3">
      {member.prefPosition !== 'Not known' ? member.prefPosition : null}
    </td>
    <td className="priority3">{member.shirtNumber}</td>
    <td>{member.numAppearances}</td>
    <td>{member.goals}</td>
  </tr>
);

MemberTableRow.propTypes = {
  member: PropTypes.shape({
    id: PropTypes.string,
    first_name: PropTypes.string,
    last_name: PropTypes.string,
  }).isRequired,
};

export default MemberTableRow;
