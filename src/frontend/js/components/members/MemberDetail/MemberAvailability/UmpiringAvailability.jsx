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
 * See PlayingAvailabilty component for a fuller explanation.
 */
const UmpiringAvailability = ({ member }) => (
  <div>
    <Subheading text="Umpiring Availability" />
    <MemberAvailability member={member} availabilityType={AvailabilityType.Umpiring} />
  </div>
);

UmpiringAvailability.propTypes = {
  member: MemberPropType.isRequired,
};

export default UmpiringAvailability;
