import React from 'react';
import PropTypes from 'prop-types';
import { Route, NavLink, Redirect, Switch } from 'react-router-dom';
import { ListGroup } from 'components/Unify';
import { MemberPropType } from './PropTypes';
import MemberCard from './MemberCard';
import MemberPlayingRecord from './MemberPlayingRecord';
import MemberClubInvolvement from './MemberClubInvolvement';
import PlayingAvailability from './MemberAvailability/PlayingAvailability';
import UmpiringAvailability from './MemberAvailability/UmpiringAvailability';

const PageRoute = {
  Home: '/',
  PlayingRecord: '/playing-record',
  ClubInvolvement: '/club-involvement',
  PlayingAvailability: '/playing-availability',
  UmpiringAvailability: '/umpiring-availability',
};

const enableAvailability = window.props.ENABLE_AVAILABILITY;

/**
 * Top-level component within the Member Detail React app
 * 
 * Note that MemberDetail uses react-router to switch between the following routes:
 * 1) Playing Record
 * 2) Club Involvement
 */
const MemberDetail = ({ isMe, member }) => (
  <div className="row">
    <div className="col-md-3">
      <MemberCard member={member} />
      <ListGroup>
        <NavLink className="list-group-item" to={PageRoute.PlayingRecord}>
          <span>
            <i className="fas fa-chart-pie g-mr-10" />Playing Record
          </span>
        </NavLink>
        <NavLink className="list-group-item" to={PageRoute.ClubInvolvement}>
          <span>
            <i className="fas fa-users g-mr-10" />Club Involvement
          </span>
        </NavLink>
      </ListGroup>
      {isMe && enableAvailability ? (
        <ListGroup className="g-mt-40">
          <span className="list-group-item g-bg-gray-light-v4">Member Tools</span>
          <NavLink className="list-group-item" to={PageRoute.PlayingAvailability}>
            <span>
              <i className="far fa-check-square g-mr-10" />Manage Playing Availability
            </span>
          </NavLink>
          {member.isUmpire ? (
            <NavLink className="list-group-item" to={PageRoute.UmpiringAvailability}>
              <span>
                <i className="far fa-check-square g-mr-10" />Manage Umpiring Availability
              </span>
            </NavLink>
          ) : null}
        </ListGroup>
      ) : null}
    </div>
    <div className="col-md-9">
      <Switch>
        <Route
          path={PageRoute.PlayingRecord}
          render={props => <MemberPlayingRecord {...props} memberId={member.id} />}
        />
        <Route
          path={PageRoute.ClubInvolvement}
          render={() => <MemberClubInvolvement member={member} />}
        />
        {enableAvailability && isMe ? (
          <Route
            path={PageRoute.PlayingAvailability}
            render={() => <PlayingAvailability member={member} />}
          />
        ) : null}
        {enableAvailability && isMe ? (
          <Route
            path={PageRoute.UmpiringAvailability}
            render={() => <UmpiringAvailability member={member} />}
          />
        ) : null}
        <Redirect from={PageRoute.Home} to={PageRoute.PlayingRecord} />
      </Switch>
    </div>
  </div>
);

MemberDetail.propTypes = {
  isMe: PropTypes.bool.isRequired,
  member: MemberPropType.isRequired,
};

MemberDetail.defaultProps = {};

export default MemberDetail;
