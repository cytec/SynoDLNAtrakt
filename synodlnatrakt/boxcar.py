# Author: Marvin Pinto <me@marvinp.ca>
# Author: Dennis Lutter <lad1337@gmail.com>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.

import urllib, urllib2
import time
from synodlnatrakt import config
from synodlnatrakt.logger import logger

API_URL = "https://boxcar.io/devices/providers/MH0S7xOFSwVLNvNhTpiC/notifications"

class BoxcarNotifier:

    def test_notify(self, email, title="Test"):
        return self._sendBoxcar("This is a test notification from SynoDLNAtrakt", title, email)

    def _sendBoxcar(self, msg, title, email, subscribe=False):
        msg = msg.strip()
        curUrl = API_URL
        data = urllib.urlencode({
                'email': email,
                'notification[from_screen_name]': title,
                'notification[message]': msg.encode('utf-8'),
                'notification[from_remote_service_id]': int(time.time())
                })
        if subscribe: # subscription notification
            data = urllib.urlencode({'email': email})
            curUrl = curUrl + "/subscribe"

        req = urllib2.Request(curUrl)
        try:
            handle = urllib2.urlopen(req, data)
            handle.close()
        except urllib2.URLError, e:
            if not hasattr(e, 'code'):
                logger.error("Boxcar notification failed. {0}".format(ex(e)))
                return False
            else:
                logger.warning("Boxcar notification failed. Error code: {0}".format(str(e.code)))

            if e.code == 404: #HTTP status 404 if the provided email address isn't a Boxcar user.
                logger.warning("Username is wrong/not a boxcar email. Boxcar will send an email to it")
                return False
            elif e.code == 401: #For HTTP status code 401's, it is because you are passing in either an invalid token, or the user has not added your service.
                if subscribe: #If the user has already added your service, we'll return an HTTP status code of 401.
                    logger.error("Already subscribed to service")
                    # i dont know if this is true or false ... its neither but i also dont know how we got here in the first place
                    return False
                else: #HTTP status 401 if the user doesn't have the service added
                    subscribeNote = self._sendBoxcar(msg, title, email, True)
                    if subscribeNote:
                        logger.debug("Subscription send")
                        return True
                    else:
                        logger.error("Subscription could not be send")
                        return False
            elif e.code == 400: #If you receive an HTTP status code of 400, it is because you failed to send the proper parameters
                logger.error("Wrong data send to boxcar")
                return False
        else:# 200
            logger.debug("Boxcar notification successful.")
            return True


    def _notifyBoxcar(self, title, message=None, username=None, force=False):
        if not config.use_boxcar and not force:
            logger.debug("Notification for Boxcar not enabled, skipping this notification")
            return False

        if not username:
            username = config.boxcar_username

        logger.debug("Sending notification for {0}".format(message))

        self._sendBoxcar(message, title, username)
        return True

notifier = BoxcarNotifier
