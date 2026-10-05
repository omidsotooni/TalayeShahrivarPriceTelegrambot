import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import time
from configs.app_config import (WP_MEDIA_URL, WP_USER, WP_APP_PASS, EXCEL_FILE, FEATURED_MEDIA_NEWS)
from utilities.utils import log_message

df = pd.read_excel(EXCEL_FILE)

def update_single_media(media_id: int) -> bool:
    row = df[df['Id_pic'] == media_id]
    if row.empty:
        log_message(f"⚠️ Media ID {media_id} not found in Excel.")
        return False
    row_data = row.iloc[0]
    url = f"{WP_MEDIA_URL}{media_id}"
    data = {
        "title": row_data['Title'],
        "alt_text": row_data['Alt Text'],
        "caption": row_data['Excerpt'],
        "description": row_data['Description']
    }
    try:
        response = requests.post(
            url,
            auth=HTTPBasicAuth(WP_USER, WP_APP_PASS),
            json=data,
            timeout=10
        )
        if response.status_code in [200, 201]:
            log_message(f"✅ Media {media_id} updated successfully.")
            return True
        else:
            log_message(f"❌ Failed to update media {media_id}: {response.text}")
            return False
    except Exception as e:
        log_message(f"❌ Exception updating media {media_id}: {e}")
        return False

def update_media(media_id, alt_text, title, excerpt, description):
    url = f"{WP_MEDIA_URL}{media_id}"
    data = {
        "title": title,
        "alt_text": alt_text,
        "caption": excerpt,
        "description": description
    }
    try:
        response = requests.post(url, auth=HTTPBasicAuth(WP_USER, WP_APP_PASS), json=data, timeout=10)
        if response.status_code in [200, 201]:
            # log_message(f"✅ Media {media_id} updated successfully.")
            return True
        else:
            log_message(f"❌ Failed to update media {media_id}: {response.text}")
            return False
    except Exception as e:
        log_message(f"❌ Exception while updating media {media_id}: {e}")
        return False

def update_featured_media(retries: int = 3, delay: float = 0.2):
    failed_media = []
    successful_media = []

    for day, media_ids in FEATURED_MEDIA_NEWS.items():
        for media_id in media_ids:
            row = df[df['Id_pic'] == media_id]
            if row.empty:
                log_message(f"⚠️ Media ID {media_id} not found in Excel.")
                failed_media.append(media_id)
                continue
            row_data = row.iloc[0]
            success = update_media(
                media_id=media_id,
                alt_text=row_data['Alt Text'],
                title=row_data['Title'],
                excerpt=row_data['Excerpt'],
                description=row_data['Description']
            )
            if success:
                successful_media.append(media_id)
            else:
                failed_media.append(media_id)
            time.sleep(delay)

    for attempt in range(1, retries + 1):
        if not failed_media:
            break
        log_message(f"⏳ Retry attempt {attempt} for {len(failed_media)} failed media...")
        retry_ids = failed_media.copy()
        failed_media.clear()
        for media_id in retry_ids:
            row = df[df['Id_pic'] == media_id].iloc[0]
            success = update_media(
                media_id=media_id,
                alt_text=row['Alt Text'],
                title=row['Title'],
                excerpt=row['Excerpt'],
                description=row['Description']
            )
            if success:
                successful_media.append(media_id)
            else:
                failed_media.append(media_id)
            time.sleep(delay)

    log_message("✅ Successfully updated media IDs:\n" + str(successful_media))
    if failed_media:
        log_message("⚠️ Failed to update media IDs:\n" + str(failed_media))
    else:
        log_message("✅ All media items were updated successfully!")

if __name__ == "__main__":
    update_featured_media()
    # update_single_media(8081)
