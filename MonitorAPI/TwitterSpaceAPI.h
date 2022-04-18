#ifndef TWITTERSPACEAPI_H
#define TWITTERSPACEAPI_H

// Declare internal libs
#include <string>
#include <format> //C++20 formatting library, used for api operations
#include <chrono> // C++20 Chrono Library, very powerful

// Declare external libs
#include <cpr/cpr.h>
#include <nlohmann/json.hpp>
#include <boost/algorithm/string/replace.hpp>

#include <boost/nowide/iostream.hpp> //debug

#include "m3u8_parser.h"

using namespace std;
using json = nlohmann::json;

// Important URLS for grabbing metadata and other associated things
constexpr string_view bearer = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA";
constexpr string_view dyn_base = "https://twitter.com/i/api/1.1/live_video_stream/status/{}";
constexpr string_view meta_url = "https://twitter.com/i/api/graphql/jyQ0_DEMZHeoluCgHJ-U5Q/AudioSpaceById";
constexpr string_view avatar_url = "https://twitter.com/i/api/fleets/v1/avatar_content";
constexpr string_view user_base = "https://cdn.syndication.twimg.com/widgets/followbutton/info.json";
constexpr string_view guest_token_url = "https://api.twitter.com/1.1/guest/activate.json";
constexpr string_view metavariables = "{{\"id\":\"{}\",\"isMetatagsQuery\":true,\"withSuperFollowsUserFields\":true,\"withDownvotePerspective\":false,\"withReactionsMetadata\":false,\"withReactionsPerspective\":false,\"withSuperFollowsTweetFields\":true,\"withReplays\":true,\"__fs_dont_mention_me_view_api_enabled\":false,\"__fs_interactive_text_enabled\":true,\"__fs_responsive_web_uc_gql_enabled\":false, \"withUserResults\":false, \"withScheduledSpaces\":false, \"withBirdwatchPivots\":false, \"withNftAvatar\":true}}";

class TwSpaceAPI
{
	friend class m3u8_parser;
	string guest_token; // This doesn't need to be refreshed on the hour because this is just the command line-tool.
protected:
	struct TwitterUser {
		string name;     // Twitter display name
		string username; // Twitter username
		string user_id;  // Twitter User ID
		string user_pfp; // Twitter User profile Picture
	};

	struct TwitterSpace_Links {
		string master_url;
		string master_playlist;
		string space_url;
	};

	struct TwitterSpace {
		TwitterUser Host;
		TwitterSpace_Links links;

		string media_key;
		double created_at;
		double updated_at;

		string space_id;
		string space_state;
		string space_title;
	}twspace;
	// TODO -> Add section for speakers, because sometimes there are multiple people that are speaking at the same time
	// And that screws things up big time. Until we get the rest working, this will have to wait.

public:
	// Twitter User operations
	TwitterUser setData(string); //Get user ID from username (we don't need one of these for the user ID because we can capture a space with the user ID alone)

	// Quick note- If the inputted url is a master url, then this entire class is not needed, it can simply be overlooked.
	TwitterSpace set_space_data(string); //Set the space data from the space ID
	TwitterSpace set_space_data_url(string); // set the space data from a url (not master)

	TwitterSpace set_space_data_username(string, string); // set the username from a username (Requires auth, which can be passed via cli)
	TwitterSpace set_space_data_user_id(string, string); // set the space data from the user ID (Requires Auth, which can be passed via cli)

	// Misc Twitter Space functions
	void update_state(); //Update the space state

	void generate_guest_token(); // Generate the guest token
	void print_space_info(TwitterSpace);
};

class Formatter : private TwSpaceAPI
{
	struct timedata {
		int year_;
		int month_;
		int day_;

		int hour;
		int minute;
		int second;

		string time_utc;
		string time_local;
	};

public:
	timedata set_time_data();

	void format_filename(TwitterSpace, std::string&);
};

#endif