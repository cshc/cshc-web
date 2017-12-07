import MatchListWithData from 'components/matches/MatchList/matchListQuery';
import MatchList from 'components/matches/MatchList';
import { MatchItem } from 'util/constants';

import React from 'react';
import PropTypes from 'prop-types';

const MemberMatchList = ({ data, ...props }) => (
  <MatchList
    exclude={[MatchItem.fixtureType, MatchItem.time, MatchItem.scorers, MatchItem.awards]}
    matches={data.edges.map(m => m.node)}
    {...props}
  />
);

MemberMatchList.propTypes = {
  data: PropTypes.shape().isRequired,
};

export default MatchListWithData(MemberMatchList);
