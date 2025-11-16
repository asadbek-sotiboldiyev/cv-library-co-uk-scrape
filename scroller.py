import time



def scroll_to_end(driver, increment=0.15, pause_time=1):
    try:
        total_height = driver.execute_script("return document.body.scrollHeight")
        current_position = 0
        print('Loading logos')
        while current_position < total_height:
            current_position += total_height * increment
            driver.execute_script(f"window.scrollTo(0, {total_height * increment});")

            time.sleep(pause_time)  # Wait for new content to load, if applicable

            new_total_height = driver.execute_script("return document.body.scrollHeight")
            if new_total_height > total_height:
                print("New content loaded, updating total height.")
                total_height = new_total_height
            elif current_position >= total_height:
                break

    except Exception as e:
        print(f"Error during scrolling: {e}")



