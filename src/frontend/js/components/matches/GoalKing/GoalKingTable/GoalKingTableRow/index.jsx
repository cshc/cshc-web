import React from 'react';
import PropTypes from 'prop-types';
import round from 'lodash/round';
import Member from 'models/member';
import { Gender, NoFilter } from 'util/constants';
import Urls from 'util/urls';

// Colors to use for the ranking labels
const genderColor = {
  [Gender.Male]: 'green',
  [Gender.Female]: 'blue',
};

const GoalKingTableRow = ({ entry, teamFilter }) => {
  const teamClass = teamSlug =>
    (teamSlug === teamFilter ? 'g-font-weight-600 priority3' : 'priority3');
  return (
    <tr>
      <td>
        <span className={`u-label g-bg-${genderColor[entry.member.gender]}`}>{entry.rank}</span>
      </td>
      <td className="text-left">
        <a href={Urls.member_detail(entry.member.id)} title="Member details">
          {Member.fullName(entry.member)}
        </a>
      </td>
      <td className={teamClass('m1')}>{entry.m1Goals}</td>
      <td className={teamClass('m2')}>{entry.m2Goals}</td>
      <td className={teamClass('m3')}>{entry.m3Goals}</td>
      <td className={teamClass('m4')}>{entry.m4Goals}</td>
      <td className={teamClass('m5')}>{entry.m5Goals}</td>
      <td className={teamClass('l1')}>{entry.l1Goals}</td>
      <td className={teamClass('l2')}>{entry.l2Goals}</td>
      <td className={teamClass('l3')}>{entry.l3Goals}</td>
      <td className={teamClass('l4')}>{entry.l4Goals}</td>
      <td className={teamClass('mixed')}>{entry.mixedGoals}</td>
      <td className={teamClass('indoor')}>{entry.indoorGoals}</td>
      <td className={teamFilter === NoFilter ? 'g-font-weight-600' : ''}>{entry.totalGoals}</td>
      <td>{round(entry.gpg, 2)}</td>
    </tr>
  );
};

GoalKingTableRow.propTypes = {
  entry: PropTypes.shape().isRequired,
  teamFilter: PropTypes.string,
};

GoalKingTableRow.defaultProps = {
  teamFilter: undefined,
};

export default GoalKingTableRow;
