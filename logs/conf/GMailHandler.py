import logging
import logging.handlers


class GMailHandler(logging.Handler):
    def __init__(self, fromaddr, subject, toaddrs=None,
                 credentials=None, oauth_path=None):
        logging.Handler.__init__(self)
        if isinstance(credentials, (list, tuple)):
            self.username, self.password = credentials
        else:
            self.username = None
        self.fromaddr = fromaddr
        if isinstance(toaddrs, basestring):
            toaddrs = [toaddrs]
        self.toaddrs = toaddrs
        if self.toaddrs is None:
            self.toaddrs = self.fromaddr
        self.subject = subject
        self.oauth = oauth_path

    def getSubject(self, record):
        """
        Determine the subject for the email.

        If you want to specify a subject line which is record-dependent,
        override this method.
        """
        return self.subject

    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            import yagmail
            if self.username is not None:
                yag = yagmail.SMTP(self.fromaddr, user=self.username, password=self.password)
            elif self.oauth is not None:
                yag = yagmail.SMTP(self.fromaddr, oauth2_file=self.oauth)
            else:
                raise ValueError("You must provide either credentials or oauth_path to yagmail")
            msg = self.format(record)
            yag.send(subject=self.getSubject(record), contents=msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except StandardError:
            self.handleError(record)

