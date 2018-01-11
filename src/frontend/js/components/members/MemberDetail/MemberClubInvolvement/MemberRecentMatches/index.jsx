import MatchDataWithData from 'components/matches/MatchData/matchDataQuery';
import MatchData from 'components/matches/MatchData';
import { MatchItem } from 'util/constants';

import React from 'react';
import PropTypes from 'prop-types';

const MemberMatchData = ({ data, ...props }) => (
  <MatchData
    exclude={[MatchItem.fixtureType, MatchItem.time, MatchItem.scorers, MatchItem.awards]}
    matches={data.results}
    {...props}
  />
);

MemberMatchData.propTypes = {
  data: PropTypes.shape().isRequired,
};

export default MatchDataWithData(MemberMatchData);
