#include <string>

#include "m3u8_parser.h"
#include "TwitterSpaceAPI.h"

#include <boost/tokenizer.hpp>
#include <boost/nowide/iostream.hpp>
#include <boost/token_functions.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/program_options/parsers.hpp>
#include <boost/program_options/variables_map.hpp>
#include <boost/program_options/options_description.hpp>

using namespace std;

using namespace boost::nowide;
using namespace boost::program_options;

int main(int ac, char* av[])
{
	TwSpaceAPI twspace;
	m3u8_parser m3p;
	string auth_token;
	Formatter fmttr;
	try {
		// Declare the option Groups
		options_description required_args("Required Arguments");
		required_args.add_options()
			("auth,a", value<string>(), "Your twitter account's auth token") // Don't forget to add the filename format!!
			("filename,f", value<string>(), "File Format (see Format options)\n NOTE: The File Formatting Options are not comaptible with Master URLs.\nFormat options\n%Ud Host Display Name          %Dd Day\n%Un Host Username              %Dt Time (UTC)\n%Ui Host User ID               %Dl Time (Local)\n%St Space Title                %Si Space ID\n%Dy Year                       %Dm Month");
		options_description link_args("Link Arguments");
		link_args.add_options()
			("master_url", value<string>(), "Input Master URL")
			("space_url", value<string>(), "Input Space URL")
			("space_id", value<string>(), "Input Space ID");
		options_description user_args("User-Related Arguments");
		user_args.add_options()
			("username", value<string>(), "Input Username")
			("user_id", value<string>(), "Input User ID");
		options_description help("Special Arguments");
		help.add_options()
			("help,h", "Displays the help page");

		options_description all("Allowed Options");
		all.add(help).add(required_args).add(link_args).add(user_args);

		options_description link_help("Allowed Options");
		link_help.add(required_args).add(link_args);

		options_description user_help("Allowed Options");
		link_help.add(required_args).add(user_args);

		variables_map vm;
		store(parse_command_line(ac, av, all), vm);
		if (vm.count("help"))
		{
			cout << all;
			return 0;
		}
		if (vm.count("auth"))
		{
			string username;
			string user_id;
			string filename;
			auth_token = vm["auth"].as<string>();
			filename = vm["filename"].as<string>();
			if (vm.count("username"))
			{
				if (vm.count("filename")) {
					user_id = vm["username"].as<string>();
	//				string filename = vm["filename"].as<string>();
					auto data = twspace.set_space_data_user_id(user_id, auth_token);
					fmttr.format_filename(data, filename);
					auto m3dat = m3p.set_m3u8_info(data.links.master_url, data.links.master_playlist);
					twspace.print_space_info(data);
					m3p.print_m3_data(m3dat);
					chunk_downloader chd(filename);
					chd.downloadSpace(m3dat);
					return 0;
				}
			}
			if (vm.count("user_id"))
			{
				if (vm.count("filename")) {
					user_id = vm["user_id"].as<string>();
	//				string filename = vm["filename"].as<string>();
					auto data = twspace.set_space_data_user_id(user_id, auth_token);
					fmttr.format_filename(data, filename);
					auto m3dat = m3p.set_m3u8_info(data.links.master_url, data.links.master_playlist);
					twspace.print_space_info(data);
					m3p.print_m3_data(m3dat);
					chunk_downloader chd(filename);
					chd.downloadSpace(m3dat);
					return 0;
				}
			}
			if (vm.count("master_url") || vm.count("space_url") || vm.count("space_id"))
			{
				cout << "There is no need to pass the auth token when using a direct space link" << endl;
				cout << link_help;
				return 0;
			}
			else { cout << "Invalid argument passed" << endl;  cout << all; return 0; }
		}
		if (vm.count("master_url"))
		{
			string filename;
			if (vm.count("filename")) {
				string master_url = vm["master_url"].as<string>();
				filename = vm["filename"].as<string>();
				auto data = m3p.set_m3u8_info(master_url, m3p.get_master_playlist(master_url));
				m3p.print_m3_data(data);
				chunk_downloader chd(filename);
				chd.downloadSpace(data);
				return 0;
			}
			else { cout << "Filename Argument Missing"; return 0;}
		}
		if (vm.count("space_id"))
		{
			string file_name;
			if (vm.count("filename")) {
				auto data = twspace.set_space_data(vm["space_id"].as<string>());
				file_name = vm["filename"].as<string>();
				auto m3dat = m3p.set_m3u8_info(data.links.master_url, data.links.master_playlist);
				twspace.print_space_info(data);
				m3p.print_m3_data(m3dat);
				fmttr.format_filename(data, file_name);
				chunk_downloader chd(file_name);
				chd.downloadSpace(m3dat);
				return 0;
			}
			else { cout << "No Filename Supplied" << endl; return 0; }
		}
		if (vm.count("space_url"))
		{
			string filename;
			if (vm.count("filename")) {
				auto data = twspace.set_space_data(vm["space_url"].as<string>());
				filename = vm["filename"].as<string>();
				fmttr.format_filename(data, filename);
				auto m3dat = m3p.set_m3u8_info(data.links.master_url, data.links.master_playlist);
				twspace.print_space_info(data);
				m3p.print_m3_data(m3dat);
				chunk_downloader chd(filename);
				chd.downloadSpace(m3dat);
				return 0;
			}
		}
	}
	catch (std::exception& e)
	{
		cout << "Invalid Argument Passed" << endl;
		cout << e.what() << endl;
		return 0;
	}
}