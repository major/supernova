#!/usr/bin/env python
#
# Copyright 2012 Major Hayden
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import ConfigParser
import logging
import supernova


def setup_logging():
    # Defaults
    filename = 'supernova.log'
    level = 'INFO'
    handler = 'FileHandler'  # NullHandler to disable

    # Get log config from super config
    try:
        config = supernova.SuperNova().get_nova_creds().items("log")
    except ConfigParser.NoSectionError:
        config = {}
    for param, value in config:
        if param.lower() == 'level':
            level = value.upper()
        if param.lower() == 'filename':
            filename = value
        if param.lower() == 'handler':
            handler = value

    # Set up a specific logger with our desired output level
    log = logging.getLogger('supernova')
    log.setLevel(getattr(logging, level))

    # Add the log message handler to the logger
    if handler == 'FileHandler':
        log_handler = getattr(logging, handler)(filename)
    else:
        log_handler = getattr(logging, handler)()

    # create a logging format
    format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - \
            %(message)s')
    log_handler.setFormatter(format)
    log_handler.setLevel(getattr(logging, level))
    log.addHandler(log_handler)
