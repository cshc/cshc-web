import React from 'react';
import PropTypes from 'prop-types';
import round from 'lodash/round';
import Member from 'models/member';
import { Gender } from 'util/constants';
import Urls from 'util/urls';

// Colors to use for the ranking labels
const genderColor = {
  [Gender.Male]: 'green',
  [Gender.Female]: 'blue',
};

const GoalKingTableRow = ({ entry }) => (
  <tr>
    <td className="text-center">
      <span className={`u-label g-bg-${genderColor[entry.member.gender]}`}>{entry.rank}</span>
    </td>
    <td>
      <a href={Urls.member_detail(entry.member.modelId)} title="Member details">
        {Member.fullName(entry.member)}
      </a>
    </td>
    <td className="priority3">{entry.m1Goals}</td>
    <td className="priority3">{entry.m2Goals}</td>
    <td className="priority3">{entry.m3Goals}</td>
    <td className="priority3">{entry.m4Goals}</td>
    <td className="priority3">{entry.m5Goals}</td>
    <td className="priority3">{entry.l1Goals}</td>
    <td className="priority3">{entry.l2Goals}</td>
    <td className="priority3">{entry.l3Goals}</td>
    <td className="priority3">{entry.l4Goals}</td>
    <td className="priority3">{entry.mixedGoals}</td>
    <td className="priority3">{entry.indoorGoals}</td>
    <td>{entry.totalGoals}</td>
    <td>{round(entry.goalsPerGame, 2)}</td>
  </tr>
);

GoalKingTableRow.propTypes = {
  entry: PropTypes.shape().isRequired,
};

export default GoalKingTableRow;
