import reduce from 'lodash/reduce';

/**
 * Unify CSS breakpoints
 */
const Breakpoints = {
  s: 576,
  m: 768,
  l: 992,
  xl: 1200,
};

const toDict = keys =>
  reduce(
    keys,
    (acc, key) => {
      acc[key] = key;
      return acc;
    },
    {},
  );

const Gender = {
  Either: '',
  Male: 'MALE',
  Female: 'FEMALE',
  Mixed: 'MIXED',
  Mens: 'MENS',
  Ladies: 'LADIES',
};

const FixtureType = toDict(['Friendly', 'Cup', 'League']);

const HomeAway = {
  Home: 'HOME',
  Away: 'AWAY',
};

const MatchAward = {
  MOM: 'Man of the Match',
  LOM: 'Lemon of the Match',
};

const AltOutcome = toDict(['Postponed', 'Cancelled', 'BYE', 'Walkover', 'Abandoned']);

/**
 * Identifiers for particular views. The 'viewTypes' Redux store object uses
 * these identifiers as keys.
 */
const SwitchableView = toDict(['SquadRoster', 'MatchList', 'VenueList', 'MemberList']);

/**
 * Identifiers for various view types. Used by the ViewSwitcher component. The 
 * 'viewTypes' Redux store object uses these identifiers as values.
 */
const ViewType = toDict(['Table', 'Timeline', 'Cards', 'List', 'Map', 'Chart']);

/**
 * Identifiers for items related to a match. Used for specifying visibility/behaviour of
 * particular items.
 */
const MatchItem = toDict([
  'fixtureType',
  'date',
  'ourTeam',
  'opposition',
  'time',
  'venue',
  'result',
  'scorers',
  'awards',
  'report',
]);

/**
 * Identifying names for filters. These form the keys within the 'activeFilters' Redux store object.
 */
const FilterName = {
  HomeGround: 'homeGround',
  HomeAway: 'homeAway',
  Season: 'season',
  CurrentSeason: 'currentSeason',
  TextSearch: 'textSearch',
  Team: 'team',
  Division: 'division',
  Current: 'current',
  Captains: 'captains',
  Coaches: 'coaches',
  Umpires: 'umpires',
  Gender: 'gender',
  Position: 'position',
  GoalKingGender: 'goalKingGender',
  FixtureType: 'fixtureType',
  Opposition: 'opposition',
  Venue: 'venue',
  Member: 'member',
  MOM: 'mom',
  LOM: 'lom',
  ReportAuthor: 'reportAuthor',
  Players: 'players',
  Date: 'date',
  Result: 'result',
  Award: 'award',
};

/**
 * Playing positions - used as filter values 
 * 
 * See core/models/utils.py for the definitions of Preferred Positions.
 */
const Position = toDict(['Goalkeeper', 'Defence', 'Midfield', 'Forward', 'Unknown']);

/**
 * Mapping of positions to the set of 'pref_position' values that they relate to.
 * 
 * See core/models/utils.py for the definitions of Preferred Positions.
 */
const PositionOptions = {
  [Position.Goalkeeper]: [0, 1, 2, 3],
  [Position.Defence]: [1, 4, 5],
  [Position.Midfield]: [2, 5, 6, 7],
  [Position.Forward]: [3, 7, 8],
  [Position.Unknown]: [9],
};

/**
 * Mapping of positions to position value (allows sorting by preferred position)
 * 
 * See core/models/utils.py for the definitions of Preferred Positions.
 */
const PositionValue = {
  Goalkeeper: 0,
  'Goalkeeper/Defender': 1,
  'Goalkeeper/Midfielder': 2,
  'Goalkeeper/Forward': 3,
  Defender: 4,
  'Defender/Midfielder': 5,
  Midfielder: 6,
  'Midfielder/Forward': 7,
  Forward: 8,
  'Not known': 9,
};

/**
 * These coordinatees represent the approximate center of Cambridge.
 * Used as the default center of Google Maps.
 */
const DefaultMapCenter = {
  lat: 52.206133926014665,
  lng: 0.12531280517578125,
};

/** 
 * Enumeration of match availability values. 
 * 
 * Ref: availability.models.AVAILABILITY python object
*/
const MatchAvailability = {
  AwaitingResponse: 'AWAITING_RESPONSE',
  Available: 'AVAILABLE',
  NotAvailable: 'NOT_AVAILABLE',
  Unsure: 'UNSURE',
};

/**
 * A constant value to represent the absense of a filter. 
 * 
 * Used for the value of a default option in a list of options.
 */
const NoFilter = 'None';

/**
 * The default size for a page of paginated results
 */
const DefaultPageSize = 10;

/**
 * The default page size options for paginated results
 */
const DefaultPageSizeOptions = [10, 20, 25, 50];

module.exports = {
  Gender,
  FixtureType,
  HomeAway,
  MatchAward,
  ViewType,
  SwitchableView,
  MatchItem,
  FilterName,
  DefaultMapCenter,
  Position,
  PositionOptions,
  NoFilter,
  DefaultPageSize,
  DefaultPageSizeOptions,
  AltOutcome,
  MatchAvailability,
  PositionValue,
  Breakpoints,
};
