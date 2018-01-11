import React from 'react';
import PropTypes from 'prop-types';
import { format as dateFormat } from 'date-fns';
import Urls from 'util/urls';

/**
 * Tabular representation of a list of match reports
 */
const MemberRecentReports = ({ matches }) => (
  <div className="table-responsive">
    <table className="table table-sm table-hover">
      <tbody>
        {matches.results.map(match => (
          <tr>
            <td>{dateFormat(match.date, 'Do MMM YY')}</td>
            <td>
              <a href={Urls.match_detail(match.id)} title="Read report">
                {match.matchTitleText}
              </a>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

MemberRecentReports.propTypes = {
  matches: PropTypes.shape().isRequired,
};

export default MemberRecentReports;
