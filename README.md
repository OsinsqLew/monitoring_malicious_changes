Application for Monitoring Malicious Changes on Websites
1. Add website links to the tracking database.
2. The application will continuously check the hashes of stored web pages and their associated JavaScripts.
3. If any hash changes, the modifications made to the website will be saved to a file, and an email notification will be sent detailing the specific changes.

Technologies Used:
1. Requests library – for fetching webpage content
2. Difflib library – for file comparison and detecting changes
3. MySQL database – for storing website data
