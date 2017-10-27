import React from 'react';
import PropTypes from 'prop-types';
import MemberAvatar from 'components/members/MemberAvatar';
import Member from 'models/member';
import Urls from 'util/urls';

/**
 * Tabular representation of a Squad Roster. Each member is a row on the table.
 */
const SquadRosterTable = ({ squadStats: { squad } }) => (
  <table className="table table-sm table-hover table-responsive">
    <thead>
      <tr>
        <th className="priority3" />
        <th>Name</th>
        <th className="priority2">Position</th>
        <th className="text-center">Played</th>
        <th className="text-center">Goals</th>
        <th className="text-center">
          <i className="fa fa-star g-mr-5" />
          <abbr title="Man of the Match">MOM</abbr>
        </th>
        <th className="text-center">
          <i className="fa fa-lemon-o g-mr-5" />
          <abbr title="Lemon of the Match">LOM</abbr>
        </th>
      </tr>
    </thead>
    <tbody>
      {squad.map(memberStats => (
        <tr key={memberStats.member.modelId}>
          <td className="priority3 ">
            <MemberAvatar member={memberStats.member} />
          </td>
          <td className="align-middle">
            <a href={Urls.member_detail(memberStats.member.modelId)} title="View Profile">
              {Member.fullName(memberStats.member)}
            </a>
          </td>
          <td className="priority2 align-middle">{memberStats.member.prefPosition}</td>
          <td className="align-middle text-center">{memberStats.played}</td>
          <td className="align-middle text-center">
            {memberStats.goals > 0 ? memberStats.goals : ''}
          </td>
          <td className="align-middle text-center">{memberStats.mom > 0 ? memberStats.mom : ''}</td>
          <td className="align-middle text-center">{memberStats.lom > 0 ? memberStats.lom : ''}</td>
        </tr>
      ))}
    </tbody>
  </table>
);

SquadRosterTable.propTypes = {
  squadStats: PropTypes.shape({
    totals: PropTypes.shape(),
    squad: PropTypes.arrayOf(PropTypes.shape()),
  }),
};

SquadRosterTable.defaultProps = {
  squadStats: undefined,
};

export default SquadRosterTable;
