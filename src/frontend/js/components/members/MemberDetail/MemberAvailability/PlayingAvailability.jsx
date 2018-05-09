import React from 'react';
import { Subheading } from 'components/Unify';
import { AvailabilityType } from 'util/constants';
import { MemberPropType } from '../PropTypes';
import MemberAvailability from '.';

/**
 * A small wrapper component to ensure that when we switch between 
 * Playing Availability and Umpire Availabilty the wrapped MemberAvailability
 * component is unmounted and remounted. 
 * 
 * Currently we don't update the Apollo cache after a mutation. So without wrapping
 * the MemberAvailability component (which is used for both playing and umpiring 
 * availability), when we switch between playing and umpiring availabilities, the 
 * state of availabilities is just refreshed from the Apollo cache, without refreshing
 * from the server. The better approach would be to update the Apollo cache appropriately
 * with the result of the mutation.
 */
const PlayingAvailability = ({ member }) => (
  <div>
    <Subheading text="Playing Availability" />
    <MemberAvailability member={member} availabilityType={AvailabilityType.Playing} />
  </div>
);

PlayingAvailability.propTypes = {
  member: MemberPropType.isRequired,
};

export default PlayingAvailability;
