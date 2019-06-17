import React from 'react';
import PropTypes from 'prop-types';
import { ViewType } from 'util/constants';
import SquadRosterCard from './SquadRosterCard';
import SquadRosterTable from './SquadRosterTable';

/**
 * Represents a list of club members (typically this is filtered by season and team). 
 * 
 * The list of club members can be represented in a table or 'cards' - with a view switcher
 * to switch between these views.
 */
const SquadRoster = ({ data, viewType }) =>
  (data.squad && data.squad.length ? (
    <div>
      {viewType === ViewType.Cards ? (
        <div className="row">
          {data.squad.map(memberStats => (
            <SquadRosterCard
              key={memberStats.member.id}
              memberStats={memberStats}
              teamTotals={data.totals}
            />
          ))}
        </div>
      ) : (
        <SquadRosterTable squadStats={data} />
      )}
    </div>
  ) : (
    <div>
      <p className="lead g-font-style-italic">Squad details not available</p>
    </div>
  ));

SquadRoster.propTypes = {
  data: PropTypes.shape({
    totals: PropTypes.shape(),
    squad: PropTypes.arrayOf(PropTypes.shape()),
  }),
  viewType: PropTypes.string.isRequired,
};

SquadRoster.defaultProps = {
  data: undefined,
};

export default SquadRoster;
