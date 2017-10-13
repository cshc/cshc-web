import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import MatchTable from '../MatchTable';
import MatchTimeline from '../MatchTimeline';
import styles from './style.scss';

export const ViewType = {
  list: 'list',
  grid: 'grid',
};

class MatchList extends React.Component {
  componentDidMount() {
    $('[data-toggle="tooltip"]').tooltip();
  }

  render() {
    const {
      viewType,
      matches,
      onSelectViewType,
      exclude,
      dateFormat,
      showViewTypeSwitcher,
    } = this.props;
    const listClassName = classnames('btn  g-mr-10 g-mb-15', {
      'u-btn-outline-primary': viewType === ViewType.grid,
      'u-btn-primary': viewType === ViewType.list,
    });
    const gridClassName = classnames('btn g-mr-10 g-mb-15', {
      'u-btn-outline-primary': viewType === ViewType.list,
      'u-btn-primary': viewType === ViewType.grid,
    });
    return (
      <div>
        {showViewTypeSwitcher && (
          <div className={styles.viewTypes}>
            <a
              role="button"
              tabIndex={0}
              className={listClassName}
              onClick={() => onSelectViewType(ViewType.list)}
              data-toggle="tooltip"
              data-placement="bottom"
              title="Timeline display"
            >
              <i className="fa fa-list" />
            </a>
            <a
              role="button"
              tabIndex={0}
              className={gridClassName}
              onClick={() => onSelectViewType(ViewType.grid)}
              data-toggle="tooltip"
              data-placement="bottom"
              title="Table display"
            >
              <i className="fa fa-table" />
            </a>
          </div>
        )}
        {viewType === ViewType.list ? (
          <MatchTimeline matches={matches} exclude={exclude} dateFormat={dateFormat} />
        ) : (
          <MatchTable matches={matches} excludeColumns={exclude} dateFormat={dateFormat} />
        )}
      </div>
    );
  }
}

MatchList.propTypes = {
  viewType: PropTypes.string.isRequired,
  matches: PropTypes.arrayOf(PropTypes.shape()),
  onSelectViewType: PropTypes.func.isRequired,
  exclude: PropTypes.arrayOf(PropTypes.string),
  dateFormat: PropTypes.string,
  showViewTypeSwitcher: PropTypes.bool,
};

MatchList.defaultProps = {
  matches: undefined,
  exclude: [],
  dateFormat: 'Do MMM',
  showViewTypeSwitcher: true,
};

export default MatchList;
