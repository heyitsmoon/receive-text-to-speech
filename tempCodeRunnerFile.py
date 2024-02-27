command_retrieve = ["curl", "-X", "GET", "-H", f"Authorization: Bearer {access_token}", "http://127.0.0.1:5000/curl_messages"]

    process_retrieve = subprocess.Popen(command_retrieve, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = process_retrieve.communicate()