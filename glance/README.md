# Glance

[Link to the main Glance repo](https://github.com/glanceapp/glance)

Glance is a customisable, themeable application ran in docker which provides a local web app housing a multitude of widgets.

The aim here is to have sometime similar to the legacy chrome extension without having to worry about the boilerplate and styling. We can freely create widgets for any services we desire.

# Setup

- Pull the repo
- Copy and rename the `.env.dev` file to `.env` and change the keys to your personal ones
  - Mergefreeze uses token per each app
- Run `docker compose up -d`
- Install this [Chrome extension](https://chromewebstore.google.com/detail/custom-new-tab-url/mmjbdbjnoablegbkcklggeknkfcjkjia)
- Set the new tab url to `localhost:8085`
