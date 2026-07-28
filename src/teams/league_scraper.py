""" This module contains functions and classes used to scrape the league's
    website to extract league tables in a format that can be used by our own
    template files to render the league tables on our site.

    WARNING: As the scraping logic relies on the East League's website pages
    sticking to a particular layout, it is prone to go wrong at some point in
    the future when they update their layout! When this breaking change happens,
    you should spot it in the cronjob error report (and in incomplete league
    tables on the CSHC website). You will then need to debug the league scraping
    code and modify it to cope with the new layout of the East League's pages.
"""

import logging
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse
from django.db.models import Q
from competitions.models import DivisionResult
from matches.models import Match
from teams.models import ClubTeam
from opposition.models import Team

LOG = logging.getLogger(__name__)


def parse_url(url):
    """ Reads the contents of specified url and returns a BeautifulSoup object that wraps it"""
    source = urlopen(url).read()
    return BeautifulSoup(source, "html5lib")


def rewrite_team_name(raw_name):
    """
    Applies a series of substitutions to team names.
    Substitutions are applied sequentially and case-insensitively.
    Replacement strings can be empty to remove parts of the name.
    """
    # Define substitutions as (regex_pattern, replacement_string) tuples.
    # Patterns are applied case-insensitively.
    # Use re.escape() for literal strings to ensure special regex characters are handled.
    # Use \b for whole word matching where appropriate (e.g., for "Development").
    substitutions = [
        (re.escape("city of peterborough"), "City of Peterborough"),
        (re.escape("ipswich-east suffolk"), "Ipswich & East Suffolk"),
        (re.escape("blueharts m1"), "Blueharts 1"),
        (r"\bdevelopment\b", ""), # Removes "Development" as a whole word
        # Add more substitutions here as (pattern, replacement) tuples.
    ]

    cleaned_name = raw_name.strip()
    original_name_for_log = cleaned_name

    for pattern, replacement in substitutions:
        # Apply substitution case-insensitively
        new_name = re.sub(pattern, replacement, cleaned_name, flags=re.IGNORECASE)
        if new_name != cleaned_name:
            LOG.debug(f"  Applied substitution '{pattern}' -> '{replacement}': '{cleaned_name}' -> '{new_name}'")
            cleaned_name = new_name

    # Clean up any multiple spaces that might result from removals, and re-strip
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()

    if original_name_for_log != cleaned_name:
        LOG.debug("Team name rewritten: '{}' -> '{}'".format(raw_name, cleaned_name))
    
    return cleaned_name


def get_hockey_east_division(url, division, season):
    existing_teams = DivisionResult.objects.league_table(
        season=season, division=division)
    division_results = []
    soup = parse_url(url)
    table = soup.find(class_='table-standings')
    for row in table.select('tbody tr'):
        dr = DivisionResult()
        dr.division = division
        dr.season = season
        dr.position = int(row.find(class_='team-standings__pos').text)
        name = row.find(class_='team-meta__name').text
        set_team(dr, name, division)
        # HACK: Currently the club column also has the 'team-standings__played' class name
        dr.played = int(row.find_all(class_='team-standings__played')[-1].text) 
        dr.won = int(row.find(class_='team-standings__win').text)
        dr.drawn = int(row.find(class_='team-standings__drawn').text)
        dr.lost = int(row.find(class_='team-standings__lose').text)
        dr.goals_for = int(row.find(class_='team-standings__goals-for').text)
        dr.goals_against = int(row.find(class_='team-standings__goals-against').text)
        dr.goal_difference = int(row.find(class_='team-standings__goals-diff').text)
        dr.points = int(row.find(class_='team-standings__total-points').text)
        dr.notes = row.find(class_='team-standings__points-diff').text
        division_results.append(dr)
        LOG.debug("Parsed team: {}".format(dr))

    # Only replace existing entries if we've got at least as many entries
    if len(division_results) >= len(existing_teams):
        existing_teams.delete()
        for dr in division_results:
            dr.save()
    else:
        LOG.debug("Did not save division results for {}: Only {} teams parsed ({} teams before)".format(
            url, len(division_results), len(existing_teams)))
    return division_results


def get_east_leagues_division(url, division, season):
    """ Returns a ScrapedDivision object with the scraped league table from the specified
        url who's name matches the division parameter.
    """
    existing_teams = DivisionResult.objects.league_table(
        season=season, division=division)

    soup = parse_url(url)
    division_name = division.name.upper()
    division_element = soup.find(text=division_name)
    current_row = division_element.find_next('tr')
    next_division_element = division_element.find_next('strong')
    blank_row = division_element.find_next(text=u'\xa0')
    bottom_row = next_division_element.find_parent(
        'tr') if next_division_element != None else blank_row.find_parent('tr')
    teams = []
    pos = 0
    while current_row != bottom_row:
        columns = current_row('td')
        pos += 1
        team = DivisionResult()
        team.division = division
        team.season = season
        team.position = pos
        name = columns[0].text.strip()
        if '---' not in name and name != '' and name is not None:
            set_team(team, name, division)
            # The 2nd column is not used!
            team.played = int(columns[2].text) if columns[2].text else 0
            team.won = int(columns[3].text) if columns[3].text else 0
            team.drawn = int(columns[4].text) if columns[4].text else 0
            team.lost = int(columns[5].text) if columns[5].text else 0
            team.goals_for = int(columns[6].text) if columns[6].text else 0
            team.goals_against = int(columns[7].text) if columns[7].text else 0
            team.goal_difference = int(
                columns[8].text) if columns[8].text else 0
            # Some league tables display percentage win instead. In this case calculate the total
            if columns[9].text.endswith('%'):
                team.points = team.won * Match.POINTS_FOR_WIN + team.drawn * Match.POINTS_FOR_DRAW
            else:
                team.points = int(columns[9].text) if columns[9].text else 0
            # The 11th column is not used!
            team.notes = columns[11].text
            teams.append(team)
            LOG.debug("Parsed team: {}".format(team))
        try:
            current_row = current_row.find_next('tr')
        except:
            break

    # Only replace existing entries if we've got at least as many entries
    if len(teams) >= len(existing_teams):
        existing_teams.delete()
        for t in teams:
            t.save()
    else:
        LOG.debug("Did not save division results for {}: Only {} teams parsed ({} teams before)".format(
            url, len(teams), len(existing_teams)))
    return teams


def get_east_england_hockey_division(page_url, division, season_obj, team_name=None):
    """
    Scrapes the league table data directly from the England Hockey API,
    following a structured sequence of API calls.

    Args:
        page_url (str): The initial URL to scrape for the API base URL and key.
        division (competitions.models.Division): The Division object, containing
                                                 name, short_name, and gender.
        season_obj (competitions.models.Season): The local Season object for which
                                                  to scrape data. Its slug (e.g., "2024-2025")
                                                  will be used for API matching.

    Returns:
        list[DivisionResult]: A list of DivisionResult objects parsed from the API.
    """
    # Use the passed-in season_obj directly
    existing_teams = DivisionResult.objects.league_table(
        season=season_obj, division=division)
    division_results = []
    api_base_url = None
    api_key = None

    request_timeout = 10
    request_verify = True

    try:
        # Step 1: Call the full URL to get the API key and base URL, and filter IDs
        LOG.debug(f"Step 1: Fetching main page to extract API details and filter IDs from {page_url}")
        main_page_response = requests.get(page_url, timeout=request_timeout, verify=request_verify)
        main_page_response.raise_for_status()
        soup = BeautifulSoup(main_page_response.text, "html5lib")

        competition_table_div = soup.find('div', {'data-module': 'competitions-table'})
        if not competition_table_div:
            LOG.error(f"Could not find data-module='competitions-table' div on {page_url}")
            return []

        api_base_url = competition_table_div.get('data-url')
        api_key = competition_table_div.get('data-url-key')

        if not api_base_url or not api_key:
            LOG.error(f"Could not extract API base URL or API key from {page_url}")
            return []
        LOG.debug(f"API Base URL: {api_base_url}, API Key: {api_key[:5]}...") # Log partial key for security

        # Extract IDs directly from the HTML select elements
        season_select = soup.find('select', {'id': 'season'})
        extracted_season_id = season_select.get('data-selected-id') if season_select else None

        comp_group_select = soup.find('select', {'id': 'competition-group'})
        extracted_competition_group_id = comp_group_select.get('data-selected-id') if comp_group_select else None
        extracted_area_id = comp_group_select.get('data-area-id') if comp_group_select else None

        if not all([extracted_season_id, extracted_competition_group_id, extracted_area_id]):
            LOG.error(f"Could not extract all required IDs from {page_url}. "
                      f"Season ID: {extracted_season_id}, Comp Group ID: {extracted_competition_group_id}, Area ID: {extracted_area_id}")
            return []
        LOG.debug(f"Extracted IDs from HTML: Season={extracted_season_id}, CompGroup={extracted_competition_group_id}, Area={extracted_area_id}")

        headers = {"x-api-key": api_key, "Accept": "application/json"}

        # Step 2: Construct and call the competitionGroups URL directly using extracted IDs
        full_competition_groups_url = f"{api_base_url}/seasons/{extracted_season_id}/areas/{extracted_area_id}/competitiongroups"
        LOG.debug(f"Step 2: Fetching competition groups from {full_competition_groups_url}")
        competition_groups_response = requests.get(full_competition_groups_url, headers=headers, timeout=request_timeout, verify=request_verify)
        competition_groups_response.raise_for_status()
        competition_groups_data = competition_groups_response.json()

        target_competition_group = None
        for cg in competition_groups_data:
            if not isinstance(cg, dict):
                LOG.warning(f"Skipping non-dictionary competition group entry: {cg} (Type: {type(cg)})")
                continue
            # Match by the extracted competition group ID
            if cg.get('id') == extracted_competition_group_id:
                target_competition_group = cg
                LOG.debug(f"Matched competition group by ID: '{extracted_competition_group_id}'")
                break
        
        if not target_competition_group:
            all_cg_ids = [cg.get('id', 'N/A') for cg in competition_groups_data if isinstance(cg, dict)]
            LOG.error(f"Could not find competition group with ID '{extracted_competition_group_id}' in API response. "
                      f"Available IDs: {all_cg_ids}")
            return []
        
        # The 'links' field is a list, not a dictionary. Iterate to find the correct one.
        competition_group_links = target_competition_group.get('links', [])
        tables_link = None
        for link_item in competition_group_links:
            if link_item.get('href') and link_item['href'].endswith('/tables'):
                tables_link = link_item['href']
                break

        if not tables_link: # Check if we found the link
            LOG.error(f"Competition group '{target_competition_group.get('name')}' found but missing 'tables' link in its 'links' list.")
            return []

        LOG.debug(f"Found competition group '{target_competition_group.get('name')}' with API ID: {target_competition_group.get('id')}")

        # Step 3: Get the 'tables' URL from the competition group and use that to pull in the data
        # The tables_link from the API is already a full URL, no need to prepend api_base_url
        full_tables_url = tables_link
        LOG.debug(f"Step 3: Fetching tables data from {full_tables_url}")
        tables_response = requests.get(full_tables_url, headers=headers, timeout=request_timeout, verify=request_verify)
        tables_response.raise_for_status()
        api_response_for_tables_endpoint = tables_response.json()

        if not api_response_for_tables_endpoint:
            LOG.warning(f"API returned no data for tables endpoint {full_tables_url}.")
            return []

        # Expecting api_response_for_tables_endpoint to be a dictionary with a 'data' key
        if not isinstance(api_response_for_tables_endpoint, dict) or 'data' not in api_response_for_tables_endpoint:
            LOG.error(f"Unexpected API tables response format. Expected a dictionary with a 'data' key. Got: {type(api_response_for_tables_endpoint)}. "
                      f"Keys: {list(api_response_for_tables_endpoint.keys()) if isinstance(api_response_for_tables_endpoint, dict) else 'N/A'}")
            return []
        
        # This is the list of division table dictionaries from the API's 'data' field
        # Each item in this list is a dictionary representing a division's full table data
        division_tables_from_api_data = api_response_for_tables_endpoint['data']
        if not isinstance(division_tables_from_api_data, list):
            LOG.error(f"Expected 'data' field to be a list, but got {type(division_tables_from_api_data)}")
            return []

        # Extract the entityUrlSlug from the page_url to match against API response
        parsed_page_url = urlparse(page_url)
        # The slug is typically the second to last segment of the path
        page_url_slug = parsed_page_url.path.split('/')[-2]
        LOG.debug(f"Derived page_url_slug from database URL: '{page_url_slug}'")

        target_division_table_entry = None
        all_available_division_table_slugs = [] # For better error logging

        # Iterate directly through the list of division table entries
        for current_division_entry in division_tables_from_api_data:
            if not isinstance(current_division_entry, dict):
                LOG.warning(f"Skipping non-dictionary division table entry: {current_division_entry} (Type: {type(current_division_entry)})")
                continue
            
            current_division_table_slug = current_division_entry.get('entityUrlSlug')
            if current_division_table_slug:
                all_available_division_table_slugs.append(current_division_table_slug) # Collect all slugs for error message

            # This is the direct match we're looking for
            if current_division_table_slug == page_url_slug:
                target_division_table_entry = current_division_entry
                LOG.debug(f"Matched specific division table by entityUrlSlug: '{current_division_table_slug}'")
                break # Found the specific table, break the loop
        
        if not target_division_table_entry:
            LOG.error(f"Could not find division table matching entityUrlSlug '{page_url_slug}' "
                      f"within the API's 'data' list. "
                      f"Available division table slugs: {', '.join(all_available_division_table_slugs) if all_available_division_table_slugs else 'None'}")
            return []
        
        # Now that we have the correct division entry, extract the 'table' (list of teams) from it
        eh_division_name = target_division_table_entry.get('name')
        team_list = target_division_table_entry.get('table', []) # <--- Correctly accessing 'table' key which holds the list of teams
        if not isinstance(team_list, list):
            LOG.error(f"Expected 'table' field within matched division entry to be a list, but got {type(team_list)}")
            return []

        if not team_list:
            LOG.warning(f"No teams found in the target table for division '{division.name}'.")
            return []
        LOG.debug(f"Found table data for division '{division.name}' with {len(team_list)} teams.")

        # Step 4: Parse the data we get to scrape the results
        for i, team_data in enumerate(team_list):
            if not isinstance(team_data, dict):
                LOG.warning(f"Skipping non-dictionary team data entry: {team_data} (Type: {type(team_data)})")
                continue

            dr = DivisionResult()
            dr.division = division
            dr.season = season_obj
            dr.position = i + 1 # Assign position based on 1-indexed list order
                                                     
            name = team_data.get('teamName')
            # Removed: name = _clean_team_name(name)
            set_team(dr, name, division)

            dr.played = team_data.get('gamesPlayed', 0)
            dr.won = team_data.get('gamesWon', 0)
            dr.drawn = team_data.get('gamesDrawn', 0)
            dr.lost = team_data.get('gamesLost', 0)
            dr.goals_for = team_data.get('goalsFor', 0)
            dr.goals_against = team_data.get('goalsAgainst', 0)
            dr.goal_difference = team_data.get('goalsDifference', 0)
            dr.points = team_data.get('totalPoints', 0)
            dr.notes = team_data.get('pointsAdjustmentNotes', '')

            division_results.append(dr)
            LOG.debug(f"Parsed team from API: {dr}")

    except requests.exceptions.RequestException as e:
        LOG.error(f"API request failed for {division.name} ({season_obj.slug}): {e}", exc_info=True)
        return []
    except (KeyError, TypeError, AttributeError) as e:
        LOG.error(f"API response structure unexpected for {division.name} ({season_obj.slug}). Error: {e}. "
                  f"Context: api_base_url={api_base_url}, api_key={api_key[:5] if api_key else 'N/A'}...", exc_info=True)
        return []
    except Exception as e:
        LOG.error(f"An unexpected error occurred during API scraping for {division.name} ({season_obj.slug}): {e}", exc_info=True)
        return []

    # Only replace existing entries if we've got at least as many entries
    # This is a safeguard against partial scrapes due to API issues or incomplete data.
    if len(division_results) >= len(existing_teams) and len(division_results) > 0:
        existing_teams.delete()
        for dr in division_results:
            dr.save()
        LOG.info(f"Successfully updated {team_name}'s results for '{eh_division_name}' ({season_obj.slug}) from API.")
    else:
        LOG.warning(f"Did not save division results for {eh_division_name} ({season_obj.slug}) from API: "
                    f"Only {len(division_results)} teams parsed (previously {len(existing_teams)} teams). "
                    "This might indicate a problem with the API or an empty response, or that the new data is less complete.")
    return division_results


def set_team(team, name, division):
    """ Works out whether the team should be a CSHC team (ClubTeam) or
        an opposition team (Team). Also handles the lack of the text 'Ladies'
        in the team name.
    """
    name = rewrite_team_name(name)

    try:
        if name.startswith('Cambridge South '):
            ordinal = name.lstrip('Cambridge South ')
            slug = division.gender[0] + ordinal
            team.our_team = ClubTeam.objects.get(slug=slug.lower())
            team.opp_team = None
        else:
            # Build the full name by inserting either 'Mens' or 'Ladies' into the name
            # before the ordinal number
            words = name.split()
            if division.gender not in words:
                words.insert(-1, division.gender)
            full_name = " ".join(words)
            # Build the short name by prepending the ordinal number with either 'M' or 'L'
            words = name.split()
            if division.gender in words:
                words.remove(division.gender)
            words[-1] = division.gender[0] + words[-1]
            short_name = " ".join(words)
            name_q = Q(name=full_name) | Q(short_name=short_name)
            team.opp_team = Team.objects.get(name_q)
            team.our_team = None
    except (Team.DoesNotExist, ClubTeam.DoesNotExist):
        LOG.error("Could not find team '{}'".format(name))
