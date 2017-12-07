import React from 'react';
import PropTypes from 'prop-types';
import { ViewType } from 'util/constants';
import MemberPlayingRecordTables from './MemberPlayingRecordTables';
import MemberPlayingRecordCharts from './MemberPlayingRecordCharts';

/**
 * Wrapper class for the Playing Record views (tables/charts)
 */
const MemberPlayingRecordDisplay = ({ viewType, clubTeams, data, ...props }) =>
  (viewType === ViewType.Table ? (
    <MemberPlayingRecordTables data={data} {...props} />
  ) : (
    <MemberPlayingRecordCharts data={data} {...props} clubTeams={clubTeams} />
  ));

MemberPlayingRecordDisplay.propTypes = {
  clubTeams: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  data: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  viewType: PropTypes.string.isRequired,
};

export default MemberPlayingRecordDisplay;
