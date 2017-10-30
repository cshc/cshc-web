import React from 'react';
import PropTypes from 'prop-types';
import ViewSwitcher from 'components/common/ViewSwitcher';
import { SwitchableView, ViewType } from 'util/constants';
import MatchTable from '../MatchTable';
import MatchTimeline from '../MatchTimeline';

/**
 * Wrapper component for a list of matches. Supports different representations of the matches:
 * - Table
 * - Timeline
 * 
 * Also supports excluding columns by name and setting priorities for columns (for responsive display)
 */
const MatchList = ({
  viewType,
  matches,
  onSelectViewType,
  exclude,
  priorities,
  dateFormat,
  showViewTypeSwitcher,
}) => {
  const views = [
    {
      iconClass: 'fa fa-list',
      label: ViewType.Timeline,
      onSelect: () => onSelectViewType(SwitchableView.MatchList, ViewType.Timeline),
    },
    {
      iconClass: 'fa fa-table',
      label: ViewType.Table,
      onSelect: () => onSelectViewType(SwitchableView.MatchList, ViewType.Table),
    },
  ];
  return (
    <div>
      {showViewTypeSwitcher && <ViewSwitcher currentView={viewType} views={views} />}
      {viewType === ViewType.Timeline ? (
        <MatchTimeline matches={matches} exclude={exclude} dateFormat={dateFormat} />
      ) : (
        <MatchTable
          matches={matches}
          excludeColumns={exclude}
          dateFormat={dateFormat}
          priorities={priorities}
        />
      )}
    </div>
  );
};

MatchList.propTypes = {
  viewType: PropTypes.string.isRequired,
  matches: PropTypes.arrayOf(PropTypes.shape()),
  onSelectViewType: PropTypes.func.isRequired,
  exclude: PropTypes.arrayOf(PropTypes.string),
  priorities: PropTypes.shape(),
  dateFormat: PropTypes.string,
  showViewTypeSwitcher: PropTypes.bool,
};

MatchList.defaultProps = {
  matches: undefined,
  exclude: [],
  priorities: {},
  dateFormat: 'Do MMM',
  showViewTypeSwitcher: true,
};

export default MatchList;
