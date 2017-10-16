import React from 'react';
import PropTypes from 'prop-types';
import { format } from 'date-fns';
import Match from 'models/match';
import MemberLink from 'components/members/MemberLink';
import FixtureTypeIcon from '../../FixtureTypeIcon';
import MatchDate from '../../MatchDate';
import OppositionTeam from '../../OppositionTeam';
import KitClash from '../../KitClash';
import MatchVenue from '../../MatchVenue';
import MatchLink from '../../MatchLink';
import styles from './style.scss';

const MatchTableRow = ({ match, excludeColumns, dateFormat }) => {
  const incl = columnName => !excludeColumns.includes(columnName);
  return (
    <tr>
      {incl('fixtureType') && (
        <td className="align-middle priority3">
          <FixtureTypeIcon fixtureType={match.fixtureType} />
        </td>
      )}
      {incl('date') && (
        <td className="align-middle no-break">
          <MatchDate date={match.date} format={dateFormat} />
        </td>
      )}
      {incl('opposition') && (
        <td className="align-middle">
          <OppositionTeam team={match.oppTeam} />
          <KitClash match={match} />
        </td>
      )}
      {incl('time') && (
        <td className="align-middle priority2">
          {match.time && format(Match.datetime(match), 'H:mm')}
        </td>
      )}
      {incl('venue') && (
        <td className="align-middle priority2">
          <MatchVenue match={match} />
        </td>
      )}
      {incl('result') && (
        <td className="align-middle g-text-center">
          <span className={`${Match.resultClass(match)} g-py-5 g-px-8`}>
            {Match.scoreDisplay(match)}
          </span>
        </td>
      )}
      {incl('scorers') && (
        <td className="align-middle priority3">
          <div className={styles.flexWrap}>
            {Match.scorers(match).map(scorer => (
              <MemberLink
                key={scorer.member.modelId}
                member={scorer.member}
                badgeCount={scorer.goals}
                className="g-mr-10"
              />
            ))}
          </div>
        </td>
      )}
      {incl('awards') && (
        <td className="align-middle priority3">
          <div className={styles.flexWrap}>
            {Match.mom(match).map(awardWinner => (
              <MemberLink
                key={awardWinner.member.modelId}
                member={awardWinner.member}
                className="g-mr-10"
              />
            ))}
          </div>
        </td>
      )}
      {incl('awards') && (
        <td className="align-middle priority3">
          <div className={styles.flexWrap}>
            {Match.lom(match).map(awardWinner => (
              <MemberLink
                key={awardWinner.member.modelId}
                member={awardWinner.member}
                className="g-mr-10"
              />
            ))}
          </div>
        </td>
      )}
      {incl('report') && (
        <td className="align-middle g-text-center">
          <MatchLink match={match} />
        </td>
      )}
    </tr>
  );
};

MatchTableRow.propTypes = {
  match: PropTypes.shape().isRequired,
  excludeColumns: PropTypes.arrayOf(PropTypes.string),
  dateFormat: PropTypes.string,
};

MatchTableRow.defaultProps = {
  excludeColumns: [],
  dateFormat: 'Do MMM',
};

export default MatchTableRow;
