#!/usr/bin/env bash


if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

dpkg -l "ruby" > /dev/null
if [ $? != 0 ]; then
  apt-get install ruby
  echo "Installed Ruby"
  ruby --version
else
  echo "Ruby already installed"
  ruby --version
fi

gem list bundler | grep "bundler" > /dev/null
if [ $? != 0 ]; then
  gem install bundler
fi
bundler install

echo "Finished"
echo "Press any key to continue"
read -n1
exit 0
