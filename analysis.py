import pandas as pd

youtube = pd.read_csv("sample_youtube_data.csv")
youtube["publish_time"] = pd.to_datetime(youtube["publish_time"], errors="coerce")
youtube = youtube.dropna().drop_duplicates()

youtube_categories = {
    1: "Film & Animation",
    2: "Autos & Vehicles",
    10: "Music",
    15: "Pets & Animals",
    20: "Gaming",
    22: "People & Blogs",
    23: "Comedy",
    24: "Entertainment"
}

# --- Grouping by Day and Month
youtube["month"] = youtube["publish_time"].dt.month_name()
youtube["day_of_week"] = youtube["publish_time"].dt.day_name()
grouped_by_day = youtube.groupby(by=youtube["day_of_week"]).agg(average_by_day = ("views", "mean"), total_by_day = ("title", "count"))
grouped_by_month = youtube.groupby(by=youtube["month"]).agg(average_by_month = ("views", "mean"), total_by_month = ("title", "count"))
grouped_by_day["average_by_day"] = grouped_by_day["average_by_day"].round()
grouped_by_month["average_by_month"] = grouped_by_month["average_by_month"].round()
best_day = grouped_by_day["average_by_day"].max() 
best_month = grouped_by_month["average_by_month"].max()
most_viewed_day = grouped_by_day.loc[grouped_by_day["average_by_day"] == best_day].index[0]
most_viewed_month = grouped_by_month.loc[grouped_by_month["average_by_month"] == best_month].index[0]


# --- Average Section ---
max_views = youtube.loc[youtube["views"].idxmax(), "title"]
min_views = youtube.loc[youtube["views"].idxmin(), "title"]
average_views = youtube["views"].mean()
average_likes = youtube["likes"].mean()
average_comments = youtube["comment_count"].mean()


youtube["compare_views"] = youtube["views"].apply(
    lambda x: "Above Average" if x > average_views 
    else "Below Average" if x < average_views 
    else "Average"
      )
youtube["compare_likes"] = youtube["likes"].apply(
    lambda x: "Above Average" if x > average_likes 
    else "Below Average" if x < average_likes 
    else "Average"
      )
youtube["compare_comment"] = youtube["comment_count"].apply(
    lambda x: "Above Average" if x > average_comments 
    else "Below Average" if x < average_comments
    else "Average"
      )

above_average = (youtube["views"] > average_views).sum()



# --- Top Performing Videos ---
sorted_views = youtube.sort_values(by=["views"], ascending=False)
top_views = sorted_views.head()
sorted_likes = youtube.sort_values(by=["likes"], ascending=False)
top_likes = sorted_likes.head()
sorted_comments = youtube.sort_values(by=["comment_count"], ascending=False)
top_comments = sorted_comments.head()

# --- Engagement Rate ---
youtube["Engagement_score"] = (((youtube["likes"] + youtube["comment_count"] - youtube["dislikes"]) / youtube["views"]) * 100).round(2)
sorted_engagements = youtube.sort_values(by= ["Engagement_score"], ascending=False)


# --- Grouping by category
youtube["category_id"] = youtube["category_id"].map(youtube_categories)
category_group = youtube.groupby(by= youtube["category_id"]).agg(category_views = ("views", "mean"), category_engage = ("Engagement_score", "mean"), category_count = ("title", "count"))
category_group["category_views"] = category_group["category_views"].round()
category_group["category_engage"] = category_group["category_engage"].round()
best_category_views = category_group["category_views"].max()
best_category_engage = category_group["category_engage"].max()
Most_viewed_category = category_group.loc[category_group["category_views"] == best_category_views].index[0]
most_engaged_category = category_group.loc[category_group["category_engage"] == best_category_engage].index[0]


# ---- Relationship ----

views_likes_relationship = youtube[["views", "likes"]].corr()
views_comments_relationship = youtube[["views", "comment_count"]].corr()
like_comment_relationship = youtube[["likes", "comment_count"]].corr()





print("\n--- CONCLUSION ---")

print(f"\nThe average number of views per video: {average_views}\n")
print(f"Total Number of Videos above average: {above_average}\n")
print(f"Video with Max-Views: {max_views}\n")
print(f"Video with Min-Views: {min_views}\n")
print(f"Most engaged category: {most_engaged_category}\n")
print(f"Most viewed category: {Most_viewed_category}\n")
print(f"Most viewed day: {most_viewed_day}\n")
print(f"Most viewed Month: {most_viewed_month}\n")
