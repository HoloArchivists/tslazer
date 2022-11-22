import os
import twapi.chat.get_chat as chat
import formatters.chat_formatter as chat_formatter

def download_chat(chat_token, download_path, chat_filename, chat_format="%Un | %Mt [%Ac/%At] > %Mb", raw=False):
    chat_tokens = chat.get_chat_access_tokens(chat_token)
    messages = chat.get_chat_messages(chat_tokens[0], chat_tokens[1])
    fmttr = chat_formatter.ChatFormatter
    with open(os.path.join(download_path, chat_filename), mode='w', encoding='utf-8') as chatx:
        for message in chat.parse_all_messages(messages):
            if not raw:
                msg = fmttr.format_chat(chat_format, message)
            else:
                msg = message
            chatx.write(str(msg) + '\n')