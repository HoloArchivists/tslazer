// m3u8_parser
// written by ef1500

#include <iostream>
#include <cpr/cpr.h>
#include <filesystem>
#include "m3u8_parser.h"
#include "TwitterSpaceAPI.h"

#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <boost/regex.hpp>
#include <boost/locale.hpp>
#include <boost/process.hpp>
#include <boost/asio/post.hpp>
#include <boost/nowide/cstdlib.hpp>
#include <boost/asio/thread_pool.hpp>

m3u8_parser::m3u8_data m3u8_parser::set_m3u8_info(std::string master_url, std::string master_playlist)
{
	m3u8_data m3_data;
	if (master_url.back() == '?') {
		m3_data.url_base = master_url.substr(0, master_url.length() - 21) + "{}";
	}else{ m3_data.url_base = master_url.substr(0, master_url.length() - 20) + "{}"; }//so we can use std::format

	m3_data.playlist_title = master_playlist.substr(master_playlist.length() - 34, master_playlist.length() + 34);

	fstream m3_stream;

	cpr::Response response = cpr::Get(cpr::Url{ master_playlist });
	string response_ = response.text;

	m3_stream.open(m3_data.playlist_title, std::ios_base::out);
	m3_stream << response_;
	m3_stream.close();

	m3_stream.open(m3_data.playlist_title);
	std::string tmp;
	if (m3_stream.is_open())
	{
		while (getline(m3_stream, tmp))
		{
			if (tmp[0] != '#')
			{
				m3_data.chunk_names.push_back(tmp);
			}
		}
	}
	m3_stream.close();
	remove(m3_data.playlist_title.c_str()); //Delete it because we don't need it anymore
	m3_data.chunk_count = m3_data.chunk_names.size();

	// Get the first and last chunknames
	std::string first_chunkname = m3_data.chunk_names.front();
	std::string last_chunkname = m3_data.chunk_names.back();

	long long start = 0;
	long long end = 0; // If I don't set them equal to zero, the compiler gets mad

	boost::regex reg("\\d{19}(?=_)");
	boost::smatch match;

	bool chunk_name = boost::regex_search(first_chunkname, match, reg);
	if (chunk_name == true) { start = stoll(match[0]); } // Regex First Timestamp out

	bool chunk_name_2 = boost::regex_search(last_chunkname, match, reg);
	if (chunk_name_2 == true) { end = stoll(match[0]); } // Regex Last timestamp out

	chrono::nanoseconds duration(end - start);
	m3_data.hours = chrono::duration_cast<chrono::hours>(duration).count();
	m3_data.minutes = chrono::duration_cast<chrono::minutes>(duration).count() % 60;
	m3_data.seconds = chrono::duration_cast<chrono::seconds>(duration).count() % 60;
	m3_data.mils = chrono::duration_cast<chrono::milliseconds>(duration).count() % 1000; 
 	m3_data.micros = chrono::duration_cast<chrono::microseconds>(duration).count() % 1000;
	m3_data.nanosecs = chrono::duration_cast<chrono::nanoseconds>(duration).count() % 1000;

	return m3_data;
}

std::string m3u8_parser::get_master_playlist(std::string master_url)
{
	string domain;
	boost::regex dx("(?<=https://).*?(?=/)");
	boost::smatch match;

	bool domain_rgx = regex_search(master_url, match, dx);
	if (domain_rgx == true) { domain = match[0]; }

	// Get the master playlist
	cpr::Response response_3 = cpr::Get(cpr::Url{ master_url });
	string response_4 = response_3.text;

	// Now Split the response
	// I wanted to use C++ 20's ranges here but they no worky :(
	vector<string> playlist_lines;
	boost::split(playlist_lines, response_4, [](char delim) {return delim == '\n'; });
	string playlist_ = playlist_lines[3];

	std::string master_playlist = "https://" + domain + playlist_; //Just like legos!
	return master_playlist;
}

void m3u8_parser::print_m3_data(m3u8_data dat)
{
	cout << endl;
	cout << "Url Base: " << dat.url_base << endl;
	cout << "Playlist Title: " << dat.playlist_title << endl;
	cout << "Chunk Count: " << dat.chunk_count << endl;
	cout << "Approximate Duration: " << dat.hours << "hrs : " << dat.minutes << " mins : " << dat.seconds << "s : " << dat.mils << "ms : " << dat.micros << "us : " << dat.nanosecs << "ns " << endl;
}

void chunk_downloader::sonic_request(string filepath, string url_base, string i)
{
	std::string chunk_url = std::format(url_base, i);
	cpr::AsyncResponse rasync = cpr::GetAsync(cpr::Url{ chunk_url });
	cpr::Response response = rasync.get();
	ofstream aacWriter(filepath + "\\" + i, ios::binary);
	aacWriter << response.text;
	aacWriter.close();
}

void download_chunk(string filepath, string url_base, string i)
{
	std::string chunk_url = std::format(url_base, i);
	cpr::AsyncResponse rasync = cpr::GetAsync(cpr::Url{ chunk_url });
	cpr::Response response = rasync.get();
	ofstream aacWriter(filepath + "\\" + i, ios::binary);
	aacWriter << response.text;
	aacWriter.close();
}

void chunk_downloader::downloadSpace(m3u8_data dat)
{
	// Start off by creating a temporary folder for everything.
	// NOTE: THIS IS A POTENTIAL ATTACK VECTOR! - but since this is a simple cli tool
	// it shouldn't be much a harm to use it I suppose.
	boost::filesystem::path tmpPath = boost::filesystem::unique_path();
	const string tmpPathString = filepath + "\\" + tmpPath.string();
	boost::filesystem::path tmpPathFull{ tmpPathString };
	boost::filesystem::create_directory(tmpPathFull);

	// You have no idea how frustrating this is lmao
	// Set up for use with a thread pool using boost. 
	boost::asio::thread_pool pool(thread::hardware_concurrency() * 2);


	for (auto i : dat.chunk_names)
	{
		boost::asio::post(pool, boost::bind(download_chunk, tmpPathString, dat.url_base, i)); // Plug and chug mayhem
	}
	pool.join(); // Wait for all of the threads to complete.
	// Now that all of the chunks are downloaded, we want to clean the files so we can use them with ffmpeg
	// Create List to use with ffmpeg
	fstream fileList;
	string chunklistdir = tmpPathString + "\\" + "chunkList.txt";
	fileList.open(tmpPathString + "\\" + "chunkList.txt", std::ios_base::out);
	for (auto i : dat.chunk_names)
	{
		fileList << "file " + tmpPath.string() + "\\\\" + "cleaned_" + i << '\n';
	}
	fileList.close();

	for (auto i : dat.chunk_names)
	{
		//boost::filesystem::path file_name_{ tmpPathString + "\\" + i };
		clean_file(i, tmpPathString + "\\"); // Clean the file
	}
	// Check for m4a
	if (filename[filename.size()] == 'a' && filename[filename.size() - 1] == '4' && filename[filename.size()-2] == 'm')
	{
		filename = filename + ".m4a";
	}

	filename = boost::locale::conv::to_utf<char>(filename, "UTF-8");

	// And finally, Run the ffmpeg command
	vector<string> argx{ "-f","concat","-safe", "0", "-i",chunklistdir,"-c","copy", filename, "-loglevel", "error" };
	string arg_s;
	for (auto i : argx)
	{
		arg_s += " " + i + " ";
	}
	arg_s = "ffmpeg" + arg_s;
//	boost::process::system(boost::process::search_path("ffmpeg"), argx); 	
	boost::nowide::system(arg_s.c_str());
//	remove(chunklistdir.c_str());
	std::filesystem::remove_all(tmpPathString);
	cout << "Space Downloaded Successfully." << endl;
}