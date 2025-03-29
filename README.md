# torscan
(c) 2025 Jon Staebell

Program to turn a Google Chromecast into a grandfather clock

## Description

When run, makes a sound like a grandfather clock. Uses simple server to send .wav file from port 8000
of computer to a specified Chromecast using Pychromecast.

### Dependencies

Requires crontab set up to run at 15/30/45 minutes during desired times. e.g.:
0,15,30,45 * 7-21 * * /path/to/python /path/to/grandfather.py

Set the following parameters in grandfather.ini: 
   device_friendly_name
   clockvolume
   webhook_url (optional, set to "" to disable Discord webhook calls on errors)
(if program is renamed, need to rename the .ini file. E.g. if renamed "foo.py" it looks for "foo.ini")

Requires simple server running on port 8000 on same computer

### Executing program

* install in same directory as grandfather.ini
* python3 grandfather.py 

## Authors

Jon Staebell
jonstaebell@gmail.com

## Version History

* v2 rewrite to use chrontab, code cleanup 3/29/2025
* V1
    * Initial Release 2018

## License

torscan Copyright (C) 2025 Jon Staebell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Acknowledgments



