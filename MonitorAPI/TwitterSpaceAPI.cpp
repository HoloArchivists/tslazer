// TwitterspaceAPI
// Written by ef1500
// Purpose - To interact with twitter spaces

#include "TwitterSpaceAPI.h"

#include <boost/nowide/iostream.hpp>
#include <boost/range/adaptor/strided.hpp>
#include <boost/range/algorithm/copy.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/assign.hpp>
#include <boost/regex.hpp>
#include <chrono> // for c++ 20's chorono features

using namespace boost::nowide;
using namespace boost;

void TwSpaceAPI::generate_guest_token()
{
	cpr::Response response = cpr::Post(cpr::Url{ (string)guest_token_url }, cpr::Header{ {"authorization", (string)bearer} }); // Cast the string_views as strings
	json response_ = json::parse(response.text);

	TwSpaceAPI::guest_token = response_["guest_token"].get<string>();
}

TwSpaceAPI::TwitterUser TwSpaceAPI::setData(string username)
{
	TwSpaceAPI::TwitterUser twuser;
	cpr::Response response = cpr::Get(cpr::Url{ (string)user_base }, cpr::Parameters{ {"screen_names" , username} });
	json response_ = json::parse(response.text);
	twuser.user_id = response_[0]["id"].get<string>();
	twuser.name = response_[0]["name"].get<string>();
	twuser.username = username;

	return twuser;
}

TwSpaceAPI::TwitterSpace TwSpaceAPI::set_space_data(string Space_ID)
{
	TwSpaceAPI::TwitterUser twuser;      // Host
	TwSpaceAPI::TwitterSpace twspace;    // Current space

	TwSpaceAPI::generate_guest_token();

	string frm = format(metavariables, Space_ID);

	cpr::Response response = cpr::Get(cpr::Url{ (string)meta_url }, cpr::Parameters{ {"variables", json::parse(format(metavariables, Space_ID)).dump()} }, cpr::Header{ {"authorization", (string)bearer }, {"x-guest-token", TwSpaceAPI::guest_token } }); // There might be error here because of the Guest tokens
	json metadata = json::parse(response.text);

	twspace.space_state = metadata["data"]["audioSpace"]["metadata"]["state"].get<string>();
	twspace.space_id = metadata["data"]["audioSpace"]["metadata"]["rest_id"].get<string>();
	twspace.media_key = metadata["data"]["audioSpace"]["metadata"]["media_key"].get<string>();
	twspace.created_at = metadata["data"]["audioSpace"]["metadata"]["created_at"].get<double>();
	twspace.updated_at = metadata["data"]["audioSpace"]["metadata"]["created_at"].get<double>();

	string usertypename = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["__typename"].get<string>();

	if (usertypename != "UserUnavailable") {
		twuser.username = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["screen_name"].get<string>();
		twuser.name = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["name"].get<string>(); // shouldn't raise any issues
		twuser.user_pfp = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["profile_image_url_https"].get<string>();
		auto userid = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["rest_id"];
		string tmp = to_string(userid);
		tmp.erase(remove(tmp.begin(), tmp.end(), '\"'), tmp.end());
		twuser.user_id = tmp;
	}
	else { twuser.name = "Private Account"; twuser.username = "Private Account"; }
	try {
		twspace.space_title = metadata["data"]["audioSpace"]["metadata"]["title"].get<string>();
	}
	catch (...) { twspace.space_title = twuser.name + "'s space"; }

	twspace.Host = twuser;

	// Now Get all of the master links
	// First up - Master Url (This can also be used to get the master playlist url
	cpr::Response response_master = cpr::Get(cpr::Url{ format(dyn_base,twspace.media_key) }, cpr::Header{ {"authorization", (string)bearer}, {"x-guest-token",TwSpaceAPI::guest_token } });
	json response_master_json = json::parse(response_master.text);

	auto master_url_string = response_master_json["source"]["location"].get<string>();

	regex rgx("dynamic_playlist.m3u8");

	string master_url_ = regex_replace(master_url_string, rgx, "master_playlist.m3u8");
	twspace.links.master_url = master_url_.substr(0, master_url_string.length() - 10);

	// Set the Space url (cause I forgot earlier)
	string_view form = "https://twitter.com/i/spaces/{}"; 
	twspace.links.space_url = format(form, Space_ID);

	// Now the master Playlist
	// I didn't wanna use too many regexes but I guess I kinda have to here
	string domain;
	regex dx("(?<=https://).*?(?=/)");
	smatch match;

	bool domain_rgx = regex_search(twspace.links.master_url, match, dx);
	if (domain_rgx == true) { domain = match[0]; }

	// Get the master playlist
	cpr::Response response_master_playlist = cpr::Get(cpr::Url{ twspace.links.master_url });
	string response_master_playlist_JSON = response_master_playlist.text;

	// Now Split the response
	// I wanted to use C++ 20's ranges here but they no worky :(
	vector<string> playlist_lines;
	boost::split(playlist_lines, response_master_playlist_JSON, [](char delim) {return delim == '\n'; });
	string playlist_ = playlist_lines[3];

	twspace.links.master_playlist = "https://" + domain + playlist_; //Just like legos!

	return twspace; // Return the struct
}

TwSpaceAPI::TwitterSpace TwSpaceAPI::set_space_data_url(string Space_url)
{
	string Space_ID = Space_url.substr(Space_url.length() - 13, Space_url.length());
	TwSpaceAPI::TwitterUser twuser;      // Host
	TwSpaceAPI::TwitterSpace twspace;    // Current space

	TwSpaceAPI::generate_guest_token();

	string frm = format(metavariables, Space_ID);

	cpr::Response response = cpr::Get(cpr::Url{ (string)meta_url }, cpr::Parameters{ {"variables", json::parse(format(metavariables, Space_ID)).dump()} }, cpr::Header{ {"authorization", (string)bearer }, {"x-guest-token", TwSpaceAPI::guest_token } }); // There might be error here because of the Guest tokens
	json metadata = json::parse(response.text);

	twspace.space_state = metadata["data"]["audioSpace"]["metadata"]["state"].get<string>();
	twspace.space_id = metadata["data"]["audioSpace"]["metadata"]["rest_id"].get<string>();
	twspace.media_key = metadata["data"]["audioSpace"]["metadata"]["media_key"].get<string>();
	twspace.created_at = metadata["data"]["audioSpace"]["metadata"]["created_at"].get<double>();
	twspace.updated_at = metadata["data"]["audioSpace"]["metadata"]["created_at"].get<double>();

	string usertypename = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["__typename"].get<string>();

	if (usertypename != "UserUnavailable") {
		twuser.username = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["screen_name"].get<string>();
		twuser.name = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["name"].get<string>(); // shouldn't raise any issues
		twuser.user_pfp = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["legacy"]["profile_image_url_https"].get<string>();
		auto userid = metadata["data"]["audioSpace"]["metadata"]["creator_results"]["result"]["rest_id"];
		string tmp = to_string(userid);
		tmp.erase(remove(tmp.begin(), tmp.end(), '\"'), tmp.end());
		twuser.user_id = tmp;

	}
	else { twuser.name = "Private Account"; twuser.username = "Private Account"; }

	// Handle space names with no usernames
	try {
		twspace.space_title = metadata["data"]["audioSpace"]["metadata"]["title"].get<string>();
	}
	catch (...) { twspace.space_title = twuser.name + "'s space"; }

	twspace.Host = twuser;

	// Now Get all of the master links

	// First up - Master Url (This can also be used to get the master playlist url
	cpr::Response response_1 = cpr::Get(cpr::Url{ format(dyn_base,twspace.media_key) }, cpr::Header{ {"authorization", (string)bearer}, {"x-guest-token",TwSpaceAPI::guest_token} });
	json response_2 = json::parse(response_1.text);

	auto master_url = response_2["source"]["location"].get<string>();

	regex rgx("dynamic_playlist.m3u8");

	string master_url_ = regex_replace(master_url, rgx, "master_playlist.m3u8");
	twspace.links.master_url = master_url_.substr(0, master_url_.length() - 10);

	// Set the Space url (cause I forgot earlier)
	string_view form = "https://twitter.com/i/spaces/{}";
	twspace.links.space_url = format(form, Space_ID);

	// Now the master Playlist
	// I didn't wanna use too many regexes but I guess I kinda have to here
	string domain;
	regex dx("(?<=https://).*?(?=/)");
	smatch match;

	bool domain_rgx = regex_search(twspace.links.master_url, match, dx);
	if (domain_rgx == true) { domain = match[0]; }

	// Get the master playlist
	cpr::Response response_3 = cpr::Get(cpr::Url{ twspace.links.master_url });
	string response_4 = response_3.text;

	// Now Split the response
	// I wanted to use C++ 20's ranges here but they no worky :(
	vector<string> playlist_lines;
	boost::split(playlist_lines, response_4, [](char delim) {return delim == '\n'; });
	string playlist_ = playlist_lines[3];

	twspace.links.master_playlist = "https://" + domain + playlist_; //Just like legos!

	return twspace; // Return the struct
}

TwSpaceAPI::TwitterSpace TwSpaceAPI::set_space_data_username(string username, string auth)
{
	TwitterUser twuser = setData(username);
	cpr::Response response = cpr::Get(cpr::Url{ (string)avatar_url }, cpr::Parameters{{"user_ids", twuser.user_id} , {"only_spaces", "true"}}, cpr::Header{{"authorization", (string)bearer}, {"cookie", "auth_token=" + auth}});
	try {
		json response_ = json::parse(response.text);
		auto broadcast_id = response_["users"][twuser.user_id]["spaces"]["live_content"]["audiospace"]["broadcast_id"].get<string>();
		TwitterSpace twspace = set_space_data(broadcast_id);
		return twspace;
	}
	catch (...)
	{
		cout << "User is not live or Invalid auth token" << endl;
		TwitterSpace twspace;
		twspace.space_state = "ERROR";
		return twspace;
	}
}

TwSpaceAPI::TwitterSpace TwSpaceAPI::set_space_data_user_id(string userID, string auth)
{
	TwitterUser twuser;
	twuser.user_id = userID;
	cpr::Response response = cpr::Get(cpr::Url{ (string)avatar_url }, cpr::Parameters{ {"user_ids", twuser.user_id} , {"only_spaces", "true"} }, cpr::Header{ {"authorization", (string)bearer}, {"cookie", "auth_token=" + auth} });
	try {
		json response_ = json::parse(response.text);
		auto broadcast_id = response_["users"][twuser.user_id]["spaces"]["live_content"]["audiospace"]["broadcast_id"].get<string>();
		TwitterSpace twspace = set_space_data(broadcast_id);
		return twspace;
	}
	catch (...)
	{
		cout << "User is not live or Invalid auth token" << endl;
		TwitterSpace twspace;
		twspace.space_state = "ERROR";
		return twspace;
	}
}

void TwSpaceAPI::print_space_info(TwitterSpace twspace)
{
	cout << "Twitter Space Title: " << twspace.space_title << endl;
	cout << "Twitter Space ID: " << twspace.space_id << endl;
	cout << "Twitter Space Host Username: " << twspace.Host.username << endl;
	cout << "Twitter Space Host Name: " << twspace.Host.name << endl;
	cout << "Twitter Space Host User ID: " << twspace.Host.user_id << endl;
	cout << endl;
	cout << endl;
	cout << "Twitter Space Master URL: " << twspace.links.master_url << endl;
	cout << endl;
	cout << "Twitter Space Master Playlist: " << twspace.links.master_playlist << endl;
	cout << endl;
	cout << "Twitter Space URL: " << twspace.links.space_url << endl;
}

Formatter::timedata Formatter::set_time_data()
{
	timedata time_data;
	// Here we want to get the time
	auto now = std::chrono::zoned_time{ std::chrono::current_zone(), std::chrono::system_clock::now() }.get_local_time(); // This declares a local time point with system_clock::duration precision

	// Get a local_time point with days precision
	auto ld = floor<std::chrono::days>(now);

	// Convert local days-precision time_point to a local {y, m, d} calendar
	std::chrono::year_month_day ymd{ ld }; // YES MY DARK

	std::chrono::hh_mm_ss hms{ now - ld };

	time_data.year_ = (int)std::chrono::year{ ymd.year() }; // Cast
	time_data.month_ = unsigned{ ymd.month() };
	time_data.day_ = unsigned{ ymd.day() };

	constexpr string_view unf_time = "{}_{}_{}";
	time_data.hour = hms.hours().count();
	time_data.minute = hms.minutes().count();
	time_data.second = hms.seconds().count();
	time_data.time_local = format(unf_time, time_data.hour, time_data.minute, time_data.second);

	const auto now1 = std::chrono::utc_clock::now();
	int hour_utc = duration_cast<std::chrono::hours>(now1.time_since_epoch()).count();
	time_data.time_utc = format(unf_time, hour_utc, time_data.minute, time_data.second);

	//Return the struct
	return time_data;
}

void Formatter::format_filename(TwitterSpace twspace, std::string &filename)
{
	// Format options
	//	%Ud	Host Display Name	%Dd	Day
	//	%Un	Host Username		%Dt	Time(UTC)
	//	%Ui	Host User ID		%Dl	Time(Local)
	//	%Dy	Year				%Si	Space ID
	//	%Dm	Month				%St	Space Title
	auto time_dat = set_time_data();
	boost::replace_first(filename, "%Dd", to_string(time_dat.day_));
	boost::replace_first(filename, "%Dy", to_string(time_dat.year_));
	boost::replace_first(filename, "%Dm", to_string(time_dat.month_));
	boost::replace_first(filename, "%Si", twspace.space_id);
	boost::replace_first(filename, "%Ud", twspace.Host.name);
	boost::replace_first(filename, "%Dt", time_dat.time_utc);
	boost::replace_first(filename, "%Dl", time_dat.time_local);
	boost::replace_first(filename, "%St", twspace.space_title);
	//boost::replace_first(filename, "%Ui", twspace.Host.user_id);
	boost::replace_first(filename, "%Un", twspace.Host.username);

	// illegal filename chars
	// #<>$+%!`&*'!|{}?"=/:\@
	vector<char> illegals = { '#', '<', '>', '$', '+', '%', '!', '`', '&', '*','\'', '!', '|', '{', '}', '?', '\"', '/','\\', ':', '@', ' '};

	for (auto i : illegals)
	{
		std::erase(filename, i);
	}

	filename += ".m4a";
}