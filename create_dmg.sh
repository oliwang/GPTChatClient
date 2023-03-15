#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/GPTChatClient.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/GPTChatClient.dmg" && rm "dist/GPTChatClient.dmg"
create-dmg \
  --volname "GPTChatClient" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "GPTChatClient.app" 175 120 \
  --hide-extension "GPTChatClient.app" \
  --app-drop-link 425 120 \
  "dist/GPTChatClient.dmg" \
  "dist/dmg/"