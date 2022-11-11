# PlayerData Quicklinks Extension for Chrome
This project is to show quick links on the new tab and from a special item in Chrome

# Setup
- Copy the js/lists.example.js file and rename to js/lists.js
- Change the links to be more useful links - Note that you can have several rows and custom titles for the areas of links
- If you don't want to use the mergefreeze links then delete that section and ignore the next subheading

# Mergefreeze
To get mergefreeze to work you will need the tokens that correlate to the project in mergefreeze. These are available in last pass. Unfortunately each project has it's own token.

# Pager Duty
To show pager duty incidents that are triggered in the header, you will need to enter an api key into the options screen. To generate an api key you can do this under settings->user settings in PagerDuty. This will create a user token that has the same access as your user does which is enough to see the incidents. Once you have the token you can then add the key into the options from the pop up menu and pressing the cog icon.

# Installation
- Go to `chrome://extensions` in your browswer.
- In the top right choose `Developer Mode`.
- Click the `Load Unpacked` button
- Navigate to the root folder here
- You should now have this plugin installed.

This extension will also work in Firefox by loading a temporary extension (or packaging and loading from a file).

# Updates
- pull the code
- Go to `chrome://extensions` in your browswer.
- Reload the plugin
