import React from 'react';
import PropTypes from 'prop-types';
import reduce from 'lodash/reduce';
import { Panel, ResponsiveAbbr } from 'components/Unify';
import { nonZero, rounded } from 'util/cshc';
import Urls from 'util/urls';
import { NoFilter } from 'util/constants';
import { getAllTeams } from '../util';

/**
 * Calculates the sum of the specified field across all seasons
 */
const total = (data, fieldName) => {
  const acc = reduce(data, (sum, seasonStats) => sum + seasonStats.memberStats[fieldName], 0);
  return acc > 0 ? acc : null;
};

/**
 * Calculates the mean of the specified field across all seasons
 */
const avg = (data, totalPlayed, fieldName) => {
  const fieldTotal = total(data, fieldName);
  return rounded(fieldTotal > 0 ? fieldTotal / totalPlayed : null);
};

const seasonAvg = (seasonStats, fieldName) =>
  rounded(nonZero(seasonStats.memberStats[fieldName] / seasonStats.memberStats.played));

/**
 * Tabular representation of a member's Playing Record. 
 * 
 * Contains 3 tables:
 * 1) Matches, Goals and Awards
 * 2) Team Representations
 * 3) Success Record
 */
const MemberPlayingRecordTables = ({ data, fixtureType, memberId }) => {
  const allTeams = getAllTeams(data);
  const totalPlayed = total(data, 'played');
  const panelProps = { outlineColor: 'teal', headerColor: 'teal' };
  const tableClass = 'table table-hover u-table--v1 text-center m-0';

  const linkedMatchList = (content, params) => {
    const urlParams = { ...params };
    urlParams.players = memberId;
    if (fixtureType !== NoFilter) {
      urlParams.fixtureType = fixtureType;
    }
    const link = `${Urls.match_list()}?${Urls.buildUrlParams(urlParams)}`;
    return (
      <a target="_blank" title="View match list" href={link}>
        {content}
      </a>
    );
  };

  return (
    <div>
      <Panel title="Matches, Goals and Awards" {...panelProps}>
        <div className="table-responsive">
          <table className={tableClass}>
            <thead>
              <tr>
                <th className="text-left">Season</th>
                <th>
                  <ResponsiveAbbr verbose="Appearances" abbreviated="Apps" />
                </th>
                <th>
                  <ResponsiveAbbr verbose="Goals" abbreviated="Gls" />
                </th>
                <th>
                  <ResponsiveAbbr verbose="Clean Sheets" abbreviated="CS" />
                </th>
                <th>
                  <i className="fas fa-star g-mr-5" />
                  <ResponsiveAbbr verbose="Man of the Match" abbreviated="MOM" />
                </th>
                <th>
                  <i className="fas fa-lemon g-mr-5" />
                  <ResponsiveAbbr verbose="Lemon of the Match" abbreviated="LOM" />
                </th>
              </tr>
            </thead>
            <tbody>
              {data.map(seasonStats => (
                <tr key={seasonStats.season.slug}>
                  <td className="text-left text-nowrap">
                    {linkedMatchList(seasonStats.season.slug, { season: seasonStats.season.slug })}
                  </td>
                  <td>{nonZero(seasonStats.memberStats.played)}</td>
                  <td>{nonZero(seasonStats.memberStats.goals)}</td>
                  <td>{nonZero(seasonStats.memberStats.cleanSheets)}</td>
                  <td>
                    {linkedMatchList(nonZero(seasonStats.memberStats.mom), {
                      season: seasonStats.season.slug,
                      mom: memberId,
                    })}
                  </td>
                  <td>
                    {linkedMatchList(nonZero(seasonStats.memberStats.lom), {
                      season: seasonStats.season.slug,
                      lom: memberId,
                    })}
                  </td>
                </tr>
              ))}
              <tr className="g-bg-secondary g-font-weight-600">
                <td className="text-left text-nowrap">Total</td>
                <td>{linkedMatchList(totalPlayed, {})}</td>
                <td>{total(data, 'goals')}</td>
                <td>{total(data, 'cleanSheets')}</td>
                <td>{linkedMatchList(total(data, 'mom'), { mom: memberId })}</td>
                <td>{linkedMatchList(total(data, 'lom'), { lom: memberId })}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Panel>
      <Panel title="Team Representations" {...panelProps}>
        <div className="table-responsive">
          <table className={tableClass}>
            <thead>
              <tr>
                <th className="text-left">Season</th>
                {allTeams.map(team => <th key={team.slug}>{team.shortName}</th>)}
              </tr>
            </thead>
            <tbody>
              {data.map(seasonStats => (
                <tr key={seasonStats.season.slug}>
                  <td className="text-left text-nowrap">{seasonStats.season.slug}</td>
                  {allTeams.map((t) => {
                    // Find the matching team representation details for this season (if they exist)
                    const matching = seasonStats.memberStats.teamRepresentations.find(
                      tr => tr.team.slug === t.slug,
                    );
                    return (
                      <td key={t.slug}>
                        {matching
                          ? linkedMatchList(matching.appearanceCount, {
                            season: seasonStats.season.slug,
                            team: t.slug,
                          })
                          : null}
                      </td>
                    );
                  })}
                </tr>
              ))}
              <tr className="g-bg-secondary g-font-weight-600">
                <td className="text-left">Total</td>
                {allTeams.map((t) => {
                  // Sum all the matching team representations across all season
                  const teamTotal = reduce(
                    data,
                    (acc, seasonStats) => {
                      // Find the matching team representation details for this season
                      // (if they exist)
                      const matching = seasonStats.memberStats.teamRepresentations.find(
                        tr => tr.team.slug === t.slug,
                      );
                      return matching ? acc + matching.appearanceCount : acc;
                    },
                    0,
                  );
                  return (
                    <td key={t.slug}>
                      {teamTotal ? linkedMatchList(teamTotal, { team: t.slug }) : null}
                    </td>
                  );
                })}
              </tr>
            </tbody>
          </table>
        </div>
      </Panel>
      <Panel title="Success Record" {...panelProps}>
        <div className="table-responsive">
          <table className={tableClass}>
            <thead>
              <tr>
                <th rowSpan="2" className="text-left">
                  Season
                </th>
                <th rowSpan="2">
                  <ResponsiveAbbr verbose="Played" abbreviated="P" />
                </th>
                <th rowSpan="2">
                  <ResponsiveAbbr verbose="Won" abbreviated="W" />
                </th>
                <th rowSpan="2">
                  <ResponsiveAbbr verbose="Drawn" abbreviated="D" />
                </th>
                <th rowSpan="2">
                  <ResponsiveAbbr verbose="Lost" abbreviated="L" />
                </th>
                <th colSpan="3">Average</th>
              </tr>
              <tr>
                <th>
                  <ResponsiveAbbr verbose="Goals For" abbreviated="GF" />
                </th>
                <th>
                  <ResponsiveAbbr verbose="Goals Against" abbreviated="GA" />
                </th>
                <th>
                  <ResponsiveAbbr verbose="Points" abbreviated="Pts" />
                </th>
              </tr>
            </thead>
            <tbody>
              {data.map(seasonStats => (
                <tr key={seasonStats.season.slug}>
                  <td className="text-left text-nowrap">{seasonStats.season.slug}</td>
                  <td>
                    {linkedMatchList(seasonStats.memberStats.played, {
                      season: seasonStats.season.slug,
                    })}
                  </td>
                  <td>
                    {linkedMatchList(seasonStats.memberStats.won, {
                      season: seasonStats.season.slug,
                      result: 'won',
                    })}
                  </td>
                  <td>
                    {linkedMatchList(seasonStats.memberStats.drawn, {
                      season: seasonStats.season.slug,
                      result: 'drawn',
                    })}
                  </td>
                  <td>
                    {linkedMatchList(seasonStats.memberStats.lost, {
                      season: seasonStats.season.slug,
                      result: 'lost',
                    })}
                  </td>
                  <td>{seasonAvg(seasonStats, 'goalsFor')}</td>
                  <td>{seasonAvg(seasonStats, 'goalsAgainst')}</td>
                  <td>{seasonAvg(seasonStats, 'totalPoints')}</td>
                </tr>
              ))}
              <tr className="g-bg-secondary g-font-weight-600">
                <td className="text-left text-nowrap">Total</td>
                <td>{linkedMatchList(total(data, 'played'), {})}</td>
                <td>{linkedMatchList(total(data, 'won'), { result: 'won' })}</td>
                <td>{linkedMatchList(total(data, 'drawn'), { result: 'drawn' })}</td>
                <td>{linkedMatchList(total(data, 'lost'), { result: 'lost' })}</td>
                <td>{avg(data, totalPlayed, 'goalsFor')}</td>
                <td>{avg(data, totalPlayed, 'goalsAgainst')}</td>
                <td>{avg(data, totalPlayed, 'totalPoints')}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Panel>
    </div>
  );
};

MemberPlayingRecordTables.propTypes = {
  data: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  fixtureType: PropTypes.string.isRequired,
  memberId: PropTypes.number.isRequired,
};

export default MemberPlayingRecordTables;
