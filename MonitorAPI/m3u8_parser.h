// M3U8 Parser Class
// Written by ef1500 and みこみこみこ (https://github.com/notpeko)
// Purpose: To parse and download the m3u8 of a Twitter Space

#pragma once

#ifndef M3U8_PARSER_H
#define M3U8_PARSER_H

// I HATE COMPILERS
// GOODNESS GRACIOUS
#pragma warning(disable : 4996)

#include "TwitterSpaceAPI.h"

#include <chrono> // Use C++20's new chrono features, Mainly to get the duration of the space.
#include <thread>

#include <boost/asio.hpp>
#include <boost/thread.hpp>
#include <boost/asio/post.hpp>
#include <boost/filesystem.hpp>
#include <boost/asio/thread_pool.hpp>

class m3u8_parser {
	// What's this for? What's the purpose?
	// So we can download twitter spaces, lol
	// Two operation modes: Dynamic and Request mode.
	// Dynamic mode is for ongoing spaces and request mode is for
	// Downloading ended spaces.
	// Request mode first! So we know how to make the dynamic parser properly
protected:
	struct m3u8_data {
		std::string url_base;
		std::string playlist_title;
		int chunk_count;
		int hours; int minutes; int seconds; int mils; int micros; int nanosecs;
		std::vector<std::string> chunk_names;
	};

public:
	std::string get_master_playlist(std::string);
	m3u8_data set_m3u8_info(std::string, std::string);
	void print_m3_data(m3u8_data);
};

// Great. Now that everything here works, we want to be able to 
// Download these bad boys, so we'll need to call in some help
// Luckily, my friend みこみこみこ (https://github.com/notpeko)
// Provided me with some code to make things run nice and smoothly
// I will mention it whenever I use their code.

class chunk_downloader : private m3u8_parser
{
	std::string filepath; // Path for the download
	std::string filename; // Name of the file

public:
	chunk_downloader(std::string file_name, std::string file_path = boost::filesystem::current_path().string()) { filepath = file_path; filename = file_name; }
	void downloadSpace(m3u8_data);
	void sonic_request(std::string, std::string, std::string);

	// Thank you to みこみこみこ (https://github.com/notpeko) for the following code
	bool is_id3v2_tag(const uint8_t* buffer) {return buffer[0] == 0x49 && buffer[1] == 0x44 && buffer[2] == 0x33;}

	int decode_id3v2_size(const uint8_t* buffer, uint32_t* out) {
		//check for magic
		if (!is_id3v2_tag(buffer)) {
			return 1;
		}
		uint8_t version = buffer[3];
		switch (version) {
		case 4: {
			const uint8_t* size_bytes = &buffer[6];
			uint32_t size = 0;
			for (int i = 3; i >= 0; i--) {
				uint8_t b = size_bytes[i];
				size |= ((uint32_t)b) << 7 * (3 - i);
			}
			*out = size + 10 /* header size */;
			return 0;
		}
		}
		//unsupported version
		return 1;
	}

	int strip_leading_id3v2_tags(uint8_t* buffer, size_t size, uint8_t** stripped_start, size_t* stripped_size) {
		size_t stripped_bytes = 0;
		while (stripped_bytes < size && is_id3v2_tag(&buffer[stripped_bytes])) {
			uint32_t chunk_size;
			if (decode_id3v2_size(&buffer[stripped_bytes], &chunk_size)) return 1;
			stripped_bytes += chunk_size;
		}
		*stripped_start = buffer + stripped_bytes;
		*stripped_size = size - stripped_bytes;
		return 0;
	}

	// Slightly modified from the original so it's void
	void clean_file(std::string name, std::string pathbase)
	{
		std::string fullname = pathbase + name;
		std::string file_name_cleaned = pathbase + "cleaned_" + name;
		FILE* in = fopen(fullname.c_str(), "rb");
		fseek(in, 0, SEEK_END);
		size_t size = ftell(in);
		fseek(in, 0, SEEK_SET);

		uint8_t* mem = (uint8_t*)malloc(size);
		fread(mem, size, 1, in); // mem could be zero O_O (mfw)
		fclose(in);

		uint8_t* output_buf;
		size_t output_size;
		if (strip_leading_id3v2_tags(mem, size, &output_buf, &output_size)) {
			fprintf(stderr, "failed to strip id3v2 tags\n");
		//	return 1;
		}
		FILE* out = fopen(file_name_cleaned.c_str(), "wb");
		fwrite(output_buf, output_size, 1, out);
		fclose(out);

		free(mem);

		remove(fullname.c_str()); //Now delete the file, as we no longer need the original
	}
};

#endif