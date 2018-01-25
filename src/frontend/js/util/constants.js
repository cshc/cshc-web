import reduce from 'lodash/reduce';

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
  Season: 'season',
  CurrentSeason: 'currentSeason',
  TextSearch: 'textSearch',
  Team: 'team',
  Division: 'division',
  Current: 'current',
  Captains: 'captains',
  Gender: 'gender',
  Position: 'position',
  GoalKingGender: 'goalKingGender',
  FixtureType: 'fixtureType',
  Opposition: 'opposition',
  Venue: 'venue',
  MOM: 'mom',
  LOM: 'lom',
  ReportAuthor: 'reportAuthor',
  Players: 'players',
  Date: 'date',
  Result: 'result',
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
 * These coordinatees represent the approximate center of Cambridge.
 * Used as the default center of Google Maps.
 */
const DefaultMapCenter = {
  lat: 52.206133926014665,
  lng: 0.12531280517578125,
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
};
