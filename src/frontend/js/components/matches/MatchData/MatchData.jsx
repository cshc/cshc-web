import React from 'react';
import PropTypes from 'prop-types';
import { ViewSwitcher, ViewSwitcherView } from 'components/common/ViewSwitcher';
import { ViewType } from 'util/constants';
import MatchTable from '../MatchTable';
import MatchTimeline from '../MatchTimeline';

/**
 * Wrapper component for a list of matches. Supports different representations of the matches:
 * - Table
 * - Timeline
 * 
 * Also supports excluding columns by name and setting priorities for columns (for responsive display)
 */
class MatchData extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
    };
  }

  componentDidCatch(error) {
    console.error('Unhandled exception caught by component', error);
    this.setState({ error });
  }

  render() {
    const {
      viewType,
      matches,
      onSelectViewType,
      exclude,
      priorities,
      dateFormat,
      showViewTypeSwitcher,
      fillBlankSaturdays,
    } = this.props;
    const { error } = this.state;
    if (error) {
      return (
        <div>
          <p className="lead g-font-style-italic">Sorry - match data not available</p>
        </div>
      );
    }
    return (
      <div>
        {showViewTypeSwitcher && (
          <ViewSwitcher currentView={viewType} onSelectViewType={onSelectViewType}>
            <ViewSwitcherView iconClass="fas fa-list" label={ViewType.Timeline} />
            <ViewSwitcherView iconClass="fas fa-table" label={ViewType.Table} />
          </ViewSwitcher>
        )}
        {viewType === ViewType.Timeline ? (
          <MatchTimeline matches={matches} exclude={exclude} dateFormat={dateFormat} />
        ) : (
          <MatchTable
            matches={matches}
            excludeColumns={exclude}
            dateFormat={dateFormat}
            priorities={priorities}
            fillBlankSaturdays={fillBlankSaturdays}
          />
        )}
      </div>
    );
  }
}

MatchData.propTypes = {
  viewType: PropTypes.string.isRequired,
  matches: PropTypes.arrayOf(PropTypes.shape()),
  onSelectViewType: PropTypes.func.isRequired,
  exclude: PropTypes.arrayOf(PropTypes.string),
  priorities: PropTypes.shape(),
  dateFormat: PropTypes.string,
  showViewTypeSwitcher: PropTypes.bool,
  fillBlankSaturdays: PropTypes.bool,
};

MatchData.defaultProps = {
  matches: undefined,
  exclude: [],
  priorities: {},
  dateFormat: 'Do MMM',
  showViewTypeSwitcher: false,
  fillBlankSaturdays: false,
};

export default MatchData;
