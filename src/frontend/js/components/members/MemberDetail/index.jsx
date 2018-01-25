import React from 'react';
import PropTypes from 'prop-types';
import { Route, NavLink, Redirect, Switch } from 'react-router-dom';
import { ListGroup } from 'components/Unify';
import MemberCard from './MemberCard';
import MemberPlayingRecord from './MemberPlayingRecord';
import MemberClubInvolvement from './MemberClubInvolvement';

/**
 * Top-level component within the Member Detail React app
 * 
 * Note that MemberDetail uses react-router to switch between the following routes:
 * 1) Playing Record
 * 2) Club Involvement
 */
const MemberDetail = ({ member }) => (
  <div className="row">
    <div className="col-md-3">
      <MemberCard member={member} />
      <ListGroup>
        <NavLink className="list-group-item" to="/playing-record">
          <span>
            <i className="fa fa-pie-chart g-mr-10" />Playing Record
          </span>
        </NavLink>
        <NavLink className="list-group-item" to="/club-involvement">
          <span>
            <i className="fa fa-users g-mr-10" />Club Involvement
          </span>
        </NavLink>
      </ListGroup>
    </div>
    <div className="col-md-9">
      <Switch>
        <Route
          path="/playing-record"
          render={props => <MemberPlayingRecord {...props} memberId={member.id} />}
        />
        <Route
          path="/club-involvement"
          render={props => <MemberClubInvolvement member={member} />}
        />
        <Redirect from="/" to="/playing-record" />
      </Switch>
    </div>
  </div>
);

MemberDetail.propTypes = {
  member: PropTypes.shape({
    id: PropTypes.number.isRequired,
    firstName: PropTypes.string.isRequired,
    lastName: PropTypes.string.isRequired,
    profilePicUrl: PropTypes.string,
    prefPosition: PropTypes.string,
    squad: PropTypes.shape({
      slug: PropTypes.string,
      name: PropTypes.string,
    }),
  }).isRequired,
};

MemberDetail.defaultProps = {};

export default MemberDetail;
