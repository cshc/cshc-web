import React from 'react';
import PropTypes from 'prop-types';
import Member from 'models/member';
import { Gender, NoFilter } from 'util/constants';
import Urls from 'util/urls';
import styles from './style.scss';

// Colors to use for the ranking labels
const genderColor = {
  [Gender.Male]: 'green',
  [Gender.Female]: 'blue',
};

const GoalKingTableRow = ({ entry, teamFilter, maxGoals }) => {
  const teamClass = teamSlug =>
    (teamSlug === teamFilter ? 'g-font-weight-600 priority3' : 'priority3');
  const goals = teamFilter === NoFilter ? entry.totalGoals : entry[`${teamFilter}Goals`];
  const progressWidth = 100 * (goals / maxGoals);
  return (
    <tr>
      <td>
        <span className={`u-label g-bg-${genderColor[entry.member.gender]}`}>{entry.rank}</span>
      </td>
      <td className="text-left">
        <a href={Urls.member_detail(entry.member.id)} title="Member details">
          {Member.fullName(entry.member)}
        </a>
        <div className={styles.progressBar}>
          <div
            className={`${styles.progress} g-bg-primary`}
            role="progressbar"
            style={{ width: `${progressWidth}%` }}
          />
        </div>
      </td>
      <td className={teamClass('m1')}>{entry.m1Goals || ''}</td>
      <td className={teamClass('m2')}>{entry.m2Goals || ''}</td>
      <td className={teamClass('m3')}>{entry.m3Goals || ''}</td>
      <td className={teamClass('m4')}>{entry.m4Goals || ''}</td>
      <td className={teamClass('m5')}>{entry.m5Goals || ''}</td>
      <td className={teamClass('l1')}>{entry.l1Goals || ''}</td>
      <td className={teamClass('l2')}>{entry.l2Goals || ''}</td>
      <td className={teamClass('l3')}>{entry.l3Goals || ''}</td>
      <td className={teamClass('l4')}>{entry.l4Goals || ''}</td>
      <td className={teamClass('l5')}>{entry.l5Goals || ''}</td>
      <td className={teamClass('mv')}>{entry.mvGoals || ''}</td>
      <td className={teamClass('lv')}>{entry.lvGoals || ''}</td>
      <td className={teamClass('mind')}>{entry.mindGoals || ''}</td>
      <td className={teamClass('lind')}>{entry.lindGoals || ''}</td>
      <td className={teamClass('mixed')}>{entry.mixedGoals || ''}</td>
      <td className={teamFilter === NoFilter ? 'g-font-weight-600' : ''}>{entry.totalGoals}</td>
      <td>{entry.gpg.toFixed(2)}</td>
    </tr>
  );
};

GoalKingTableRow.propTypes = {
  entry: PropTypes.shape().isRequired,
  teamFilter: PropTypes.string,
  maxGoals: PropTypes.number.isRequired,
};

GoalKingTableRow.defaultProps = {
  teamFilter: undefined,
};

export default GoalKingTableRow;
